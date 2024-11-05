from typing import Union

from classiq.interface.exceptions import ClassiqError

from classiq.qmod.quantum_function import ExternalQFunc, GenerativeQFunc, QFunc


def synthesize_separately(qfunc: Union[QFunc, GenerativeQFunc, ExternalQFunc]) -> QFunc:
    if isinstance(qfunc, QFunc):
        qfunc.should_synthesize_separately = True
        return qfunc
    if isinstance(qfunc, GenerativeQFunc):
        raise ClassiqError("Generative functions can not be synthesized separately")
    if isinstance(qfunc, ExternalQFunc):
        raise ClassiqError("External functions can not be synthesized separately")
