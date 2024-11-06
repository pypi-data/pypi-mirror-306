import ast
from abc import abstractmethod
from itertools import chain
from typing import TYPE_CHECKING, TypeVar, Union

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.type_name import TypeName
from classiq.interface.generator.visitor import NodeType, Transformer
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.control import Control
from classiq.interface.model.handle_binding import (
    FieldHandleBinding,
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
    QuantumExpressionOperation,
)
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    QuantumType,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol
from classiq.model_expansions.visitors.variable_references import VarRefCollector

ExpressionOperationT = TypeVar("ExpressionOperationT", bound=QuantumExpressionOperation)
AST_NODE = TypeVar("AST_NODE", bound=NodeType)


class ExpressionOperationEmitter(Emitter[ExpressionOperationT]):
    @abstractmethod
    def emit(self, op: ExpressionOperationT, /) -> None:
        pass

    def _emit_with_split(
        self,
        op: ExpressionOperationT,
        expression: Expression,
        symbols_to_split: dict[QuantumSymbol, set[HandleBinding]],
    ) -> None:
        symbols_parts, bind_ops = self._get_bind_ops(symbols_to_split)

        for symbol_parts in symbols_parts:
            for symbol, symbol_part_var_name in symbol_parts:
                if symbol.handle.identifier not in self._current_scope:
                    self._interpreter.emit_statement(
                        VariableDeclarationStatement(
                            name=symbol_part_var_name,
                            quantum_type=symbol.quantum_type,
                        )
                    )

        symbol_mapping = {
            symbol.handle: (symbol_part_var_name, symbol.quantum_type)
            for symbol, symbol_part_var_name in chain.from_iterable(symbols_parts)
        }
        new_expression = self._update_op_expression(symbol_mapping, expression)
        new_op = op.model_copy(update=dict(expression=new_expression))
        new_op = self._get_updated_op_split_symbols(new_op, symbol_mapping)

        self._interpreter.emit_statement(
            WithinApply(
                compute=bind_ops,
                action=[new_op],
                source_ref=op.source_ref,
            )
        )

    def _get_updated_op_split_symbols(
        self,
        op: ExpressionOperationT,
        symbol_mapping: dict[HandleBinding, tuple[str, QuantumType]],
    ) -> ExpressionOperationT:
        return op

    def _update_op_expression(
        self,
        symbol_mapping: dict[HandleBinding, tuple[str, QuantumType]],
        expression: Expression,
    ) -> Expression:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))

        new_expr_str = expression.expr
        for handle in vrc.var_handles:
            collapsed_handle = handle.collapse()
            if collapsed_handle in symbol_mapping:
                new_expr_str = new_expr_str.replace(
                    str(handle), symbol_mapping[collapsed_handle][0]
                )
        self._check_all_handles_were_replaced(new_expr_str)

        new_expr = Expression(expr=new_expr_str)
        new_expr._evaluated_expr = EvaluatedExpression(
            value=self._interpreter.evaluate(new_expr).value
        )
        return new_expr

    def _check_all_handles_were_replaced(self, new_expr_str: str) -> None:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(new_expr_str))
        for handle in self._get_handles(vrc):
            if isinstance(
                handle,
                (SubscriptHandleBinding, SlicedHandleBinding, FieldHandleBinding),
            ):
                raise ClassiqInternalExpansionError(f"Did not replace handle {handle}")

    def _get_bind_ops(
        self,
        symbols_to_split: dict[QuantumSymbol, set[HandleBinding]],
    ) -> tuple[list[list[tuple[QuantumSymbol, str]]], list[BindOperation]]:
        bind_ops = []
        symbols_parts = []
        for symbol, target_parts in symbols_to_split.items():
            symbol_parts = self._get_symbol_parts(symbol, target_parts)
            symbols_parts.append(symbol_parts)
            bind_ops.append(
                BindOperation(
                    in_handles=[symbol.handle],
                    out_handles=[
                        HandleBinding(name=symbol_part_var_name)
                        for _, symbol_part_var_name in symbol_parts
                    ],
                )
            )
        return symbols_parts, bind_ops

    def _get_symbol_parts(
        self, symbol: QuantumSymbol, target_parts: set[HandleBinding]
    ) -> list[tuple[QuantumSymbol, str]]:
        quantum_type = symbol.quantum_type

        if all(
            symbol.handle == target_part or symbol.handle not in target_part.prefixes()
            for target_part in target_parts
        ) or isinstance(quantum_type, (QuantumBit, QuantumNumeric)):
            return [
                (
                    symbol,
                    self._counted_name_allocator.allocate(symbol.handle.identifier),
                )
            ]

        if isinstance(quantum_type, QuantumBitvector):
            if not quantum_type.has_length:
                raise ClassiqExpansionError(
                    f"Could not determine the length of quantum array "
                    f"{symbol.handle}."
                )
            return list(
                chain.from_iterable(
                    self._get_symbol_parts(symbol[idx], target_parts)
                    for idx in range(quantum_type.length_value)
                )
            )

        if TYPE_CHECKING:
            assert isinstance(quantum_type, TypeName)

        return list(
            chain.from_iterable(
                self._get_symbol_parts(field_symbol, target_parts)
                for field_symbol in symbol.fields.values()
            )
        )

    def _get_symbols_to_split(
        self, expression: Expression
    ) -> dict[QuantumSymbol, set[HandleBinding]]:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))
        symbol_names_to_split = dict.fromkeys(
            handle.name
            for handle in self._get_handles(vrc)
            if isinstance(handle, (SubscriptHandleBinding, FieldHandleBinding))
        )
        return {
            symbol: {
                handle.collapse()
                for handle in vrc.var_handles
                if handle.name == symbol.handle.name
            }
            for symbol_name in symbol_names_to_split
            if isinstance(
                symbol := self._current_scope[symbol_name].value,
                QuantumSymbol,
            )
        }

    def _evaluate_op_expression(self, op: ExpressionOperationT) -> Expression:
        return self._evaluate_expression(op.expression)

    def _evaluate_types_in_expression(
        self, op: ExpressionOperationT, expression: Expression
    ) -> ExpressionOperationT:
        op_with_evaluated_types = op.model_copy(update={"expression": expression})
        vrc = VarRefCollector()
        vrc.visit(ast.parse(op_with_evaluated_types.expression.expr))
        handles = vrc.var_handles
        op_with_evaluated_types.set_var_handles(handles)
        op_with_evaluated_types.initialize_var_types(
            {
                handle.name: self._interpreter.evaluate(handle)
                .as_type(QuantumSymbol)
                .quantum_type
                for handle in handles
            },
            self._machine_precision,
        )
        return op_with_evaluated_types

    @staticmethod
    def _all_vars_boolean(op: QuantumExpressionOperation) -> bool:
        if not all(
            var_type.has_size_in_bits and var_type.size_in_bits == 1
            for var_type in op.var_types.values()
        ):
            return False
        return not any(
            isinstance(var_type, QuantumNumeric)
            and (var_type.sign_value or var_type.fraction_digits_value > 0)
            for var_type in op.var_types.values()
        )

    @staticmethod
    def _is_res_boolean(op: Union[QuantumAssignmentOperation, Control]) -> bool:
        if not (op.result_type.has_size_in_bits and op.result_type.size_in_bits == 1):
            return False
        return not (
            isinstance(op.result_type, QuantumNumeric)
            and (op.result_type.sign_value or op.result_type.fraction_digits_value > 0)
        )

    def _get_handles(self, collector: VarRefCollector) -> list[HandleBinding]:
        return [
            handle
            for handle in collector.var_handles
            if isinstance(self._interpreter.evaluate(handle.name).value, QuantumSymbol)
        ]

    def _rewrite(
        self,
        subject: AST_NODE,
        symbol_mapping: dict[HandleBinding, tuple[str, QuantumType]],
    ) -> AST_NODE:
        class ReplaceSplitVars(Transformer):
            @staticmethod
            def visit_HandleBinding(handle: HandleBinding) -> HandleBinding:
                handle = handle.collapse()
                for handle_to_replace, replacement in symbol_mapping.items():
                    handle = handle.replace_prefix(
                        handle_to_replace, HandleBinding(name=replacement[0])
                    )
                return handle

            @staticmethod
            def visit_Expression(expr: Expression) -> Expression:
                return self._update_op_expression(symbol_mapping, expr)

        return ReplaceSplitVars().visit(subject)
