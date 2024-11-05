import re

from classiq.interface.generator.compiler_keywords import CAPTURE_SUFFIX
from classiq.interface.model.handle_binding import HANDLE_ID_SEPARATOR, HandleBinding

IDENTIFIER_PATTERN = r"[a-zA-Z_][a-zA-Z0-9_]*"
CAPTURE_PATTERN = re.compile(
    rf"({IDENTIFIER_PATTERN}){CAPTURE_SUFFIX}{IDENTIFIER_PATTERN}__"
)
ARRAY_CAST_SUFFIX = HANDLE_ID_SEPARATOR + "array_cast"


def mangle_captured_var_name(var_name: str, defining_function: str) -> str:
    return f"{var_name}{CAPTURE_SUFFIX}{defining_function}__"


def demangle_name(name: str) -> str:
    match = re.match(CAPTURE_PATTERN, name)
    return match.group(1) if match else name


def demangle_handle(handle: HandleBinding) -> HandleBinding:
    name = handle.name
    if HANDLE_ID_SEPARATOR not in name:
        return handle
    if ARRAY_CAST_SUFFIX in name:
        return HandleBinding(name=name.split(ARRAY_CAST_SUFFIX)[0])
    name = re.sub(r"_\d+$", "", name)
    name_parts = name.split(HANDLE_ID_SEPARATOR)
    new_name = name_parts[0]
    for part in name_parts[1:]:
        if re.fullmatch(r"\d+", part):
            new_name += f"[{part}]"
        elif re.fullmatch(r"\d+_\d+", part):
            part_left, part_right = part.split("_")
            new_name += f"[{part_left}:{part_right}]"
        else:
            new_name += f".{part}"
    return handle.rename(new_name)
