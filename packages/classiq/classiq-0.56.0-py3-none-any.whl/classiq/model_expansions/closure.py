import json
import uuid
from collections import defaultdict
from collections.abc import Collection, Sequence
from dataclasses import dataclass, field
from functools import cached_property, singledispatch
from symtable import Symbol
from typing import Any, Optional, Union

from typing_extensions import Self

from classiq.interface.exceptions import (
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.builtins.internal_operators import (
    All_BUILTINS_OPERATORS,
)
from classiq.interface.generator.visitor import Visitor
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    PositionalArg,
)
from classiq.interface.model.quantum_statement import QuantumStatement
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq import ClassicalParameterDeclaration
from classiq.model_expansions.expression_renamer import ExpressionRenamer
from classiq.model_expansions.scope import (
    Evaluated,
    QuantumSymbol,
    Scope,
    evaluated_to_str as evaluated_classical_param_to_str,
)
from classiq.qmod.builtins.functions import permute
from classiq.qmod.quantum_function import GenerativeQFunc


@dataclass(frozen=True)
class Closure:
    name: str
    blocks: dict[str, Sequence[QuantumStatement]]
    scope: Scope
    positional_arg_declarations: Sequence[PositionalArg] = tuple()

    @property
    def port_declarations(self) -> dict[str, PortDeclaration]:
        return {
            param.name: param
            for param in self.positional_arg_declarations
            if isinstance(param, PortDeclaration)
        }


@dataclass(frozen=True)
class GenerativeClosure(Closure):
    generative_blocks: dict[str, GenerativeQFunc] = None  # type:ignore[assignment]


@dataclass(frozen=True)
class FunctionClosure(Closure):
    is_lambda: bool = False
    is_atomic: bool = False
    signature_scope: Scope = field(default_factory=Scope)

    # creates a unique id for the function closure based on the arguments values.
    # The closure is changing across the interpreter flow so it's closure_id may change
    @property
    def closure_id(self) -> str:
        # builtins operators have side effects, so  generate a unique id for than
        # may create a bugs. Therefore, with each call to closure_id a new id is
        # created
        if self.is_lambda or self.name in All_BUILTINS_OPERATORS:
            signature = str(uuid.uuid4())
        else:
            signature = _generate_closure_id(
                self.positional_arg_declarations, self.scope.data.values()
            )
        return f"{self.name}__{signature}"

    @property
    def body(self) -> Sequence[QuantumStatement]:
        if self.name == permute.func_decl.name:
            # permute is an old Qmod "generative" function that doesn't have a body
            return []
        return self.blocks["body"]

    @cached_property
    def colliding_variables(self) -> set[str]:
        # Note that this has to be accessed after adding the parameters from the signature and not during
        # initialization
        return VariableCollector(self.scope).get_colliding_variables(self.body)

    @classmethod
    def create(
        cls,
        name: str,
        scope: Scope,
        body: Optional[Sequence[QuantumStatement]] = None,
        positional_arg_declarations: Sequence[PositionalArg] = tuple(),
        expr_renamer: Optional[ExpressionRenamer] = None,
        is_lambda: bool = False,
        is_atomic: bool = False,
        **kwargs: Any,
    ) -> Self:
        if expr_renamer:
            positional_arg_declarations = (
                expr_renamer.rename_positional_arg_declarations(
                    positional_arg_declarations
                )
            )
            if body is not None:
                body = expr_renamer.visit(body)

        blocks = {"body": body} if body is not None else {}
        return cls(
            name,
            blocks,
            scope,
            positional_arg_declarations,
            is_lambda,
            is_atomic,
            **kwargs,
        )

    def with_new_declaration(
        self, declaration: NamedParamsQuantumFunctionDeclaration
    ) -> Self:
        fields: dict = self.__dict__ | {
            "name": declaration.name,
            "positional_arg_declarations": declaration.positional_arg_declarations,
        }
        fields.pop("colliding_variables", 0)
        return type(self)(**fields)


@dataclass(frozen=True)
class GenerativeFunctionClosure(GenerativeClosure, FunctionClosure):
    pass


NestedFunctionClosureT = Union[FunctionClosure, list["NestedFunctionClosureT"]]


class VariableCollector(Visitor):
    def __init__(self, function_scope: Scope) -> None:
        self._function_scope = function_scope
        self._variables: defaultdict[str, set[Optional[str]]] = defaultdict(set)
        for var in self._function_scope.data:
            defining_function = self._function_scope[var].defining_function
            if defining_function is not None:
                self._variables[var].add(defining_function.name)

    def get_colliding_variables(self, body: Sequence[QuantumStatement]) -> set[str]:
        self.visit(body)
        return {
            var
            for var, defining_functions in self._variables.items()
            if len(defining_functions) > 1
        }

    def visit_VariableDeclarationStatement(
        self, node: VariableDeclarationStatement
    ) -> None:
        self._variables[node.name].add(None)

    def visit_QuantumFunctionCall(self, node: QuantumFunctionCall) -> None:
        # The else case corresponds to operand identifiers. In case of operand identifiers, we scan
        # the whole list of operands because we can't evaluate the index yet.
        identifier = (
            node.function if isinstance(node.function, str) else node.function.name
        )
        self._add_variables(self._function_scope[identifier].value)

    def _add_variables(self, evaluated: NestedFunctionClosureT) -> None:
        if isinstance(evaluated, list):
            for elem in evaluated:
                self._add_variables(elem)
            return
        if not isinstance(evaluated, FunctionClosure):
            raise ClassiqInternalExpansionError
        self._add_variables_from_closure(evaluated)

    def _add_variables_from_closure(self, closure: FunctionClosure) -> None:
        if not closure.is_lambda:
            return
        lambda_environment = closure.scope.parent
        if lambda_environment is None:
            raise ClassiqInternalExpansionError

        for var in lambda_environment.iter_without_top_level():
            defining_function = lambda_environment[var].defining_function
            if defining_function is not None:
                self._variables[var].add(defining_function.name)


def _generate_closure_id(
    args_declaration: Sequence[PositionalArg], evaluated_args: Collection[Evaluated]
) -> str:
    args_signature: dict = {}
    for arg_declara, eval_arg in zip(args_declaration, evaluated_args):
        args_signature |= _generate_arg_id(arg_declara, eval_arg)
    return json.dumps(args_signature)


def _generate_arg_id(
    arg_declaration: PositionalArg, evaluated_arg: Evaluated
) -> dict[str, str]:
    arg_value = evaluated_arg.value
    arg_name = arg_declaration.name
    if isinstance(arg_declaration, ClassicalParameterDeclaration):
        return {arg_name: evaluated_classical_param_to_str(arg_value)}
    return {arg_name: _evaluated_arg_to_str(arg_value)}


@singledispatch
def _evaluated_arg_to_str(arg: Any) -> str:
    if isinstance(arg, str):
        return arg
    return str(uuid.uuid4())


@_evaluated_arg_to_str.register
def _evaluated_quantum_symbol_to_str(port: QuantumSymbol) -> str:
    return port.quantum_type.model_dump_json(exclude_none=True, exclude={"name"})


@_evaluated_arg_to_str.register
def _evaluated_symbol_to_str(port: Symbol) -> str:
    return repr(port)


@_evaluated_arg_to_str.register
def _evaluated_operand_to_str(operand: FunctionClosure) -> str:
    return operand.closure_id
