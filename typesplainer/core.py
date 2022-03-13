from typing import Any, Generator


from mypy.nodes import AssignmentStmt, FuncDef, ClassDef, Decorator
from mypy.options import Options
from mypy.parse import parse
from mypy.types import Type, AnyType, UnionType


def pluralize(word: str) -> str:
    if word[-1] in "sx" or word[-2:] in ["sh", "ch"]:
        return word + "es"
    return word + "s"


def _describe(thing: Type, a: bool = True, plural=False) -> str:
    if isinstance(thing, UnionType):
        if len(thing.items) == 2 and any(i.name == "None" for i in thing.items):
            return f"optional {_describe(thing.items[0])}"
        return " or ".join(_describe(i) for i in thing.items)
    if isinstance(thing, AnyType):
        if plural:
            return "objects of any type"
        else:
            return "a object of any type" if a else "object of any type"

    try:
        name = thing.name.lower()
    except AttributeError:
        return thing.__class__.__name__
    if name == "callable":
        if plural:
            return f"callables that accept {_describe(thing.args[0])}" f" and return {_describe(thing.args[1])}"
        else:
            return (
                f"{'a ' if a else ''}callable that accepts {_describe(thing.args[0])}"
                f" and returns {_describe(thing.args[1])}"
            )
    elif name == "optional":
        return f"{'a ' if a else ''}optional {_describe(thing.args[0], a=False, plural=plural)}"
    elif name in {"generator", "coroutine"}:
        if plural:
            return (
                f"{name}s that yield {_describe(thing.args[0])},"
                f" send {_describe(thing.args[1])}, and return {_describe(thing.args[2])}"
            )
        else:
            return (
                f"{'a ' if a else ''}{name} that yields {_describe(thing.args[0])},"
                f" sends {_describe(thing.args[1])}, and returns {_describe(thing.args[2])}"
            )
    elif name == "asyncgenerator":
        if plural:
            return f"async generators that yield {_describe(thing.args[0])}" + (
                f", and send {_describe(thing.args[1])}" if len(thing.args) > 1 else ""
            )
        else:
            return f"{'an ' if a else ''}async generator that yields {_describe(thing.args[0])}" + (
                f", sends {_describe(thing.args[1])}" if len(thing.args) > 1 else ""
            )
    elif name in {"dict", "mapping", "ordereddict", "defaultdict"}:
        proper_names = {
            "dict": "dictionary",
            "mapping": "mapping",
            "ordereddict": "ordered dictionary",
            "defaultdict": "default dictionary",
        }
        name = proper_names[name]

        if plural:
            return (
                f"{pluralize(name)} that map {_describe(thing.args[0], a=False, plural=True)}"
                f" onto {_describe(thing.args[1])}"
            )
        else:
            return (
                f"{'a ' if a else ''}{name} that maps {_describe(thing.args[0], a=False, plural=True)}"
                f" onto {_describe(thing.args[1])}"
            )
    elif name in {"list", "set", "tuple", "namedtuple", "frozenset", "sequence", "iterable"}:
        if plural:
            return f"{name}s of {_describe(thing.args[0], a=False, plural=True)}"
        else:
            return f"{'a ' if a else ''}{name} of {_describe(thing.args[0], a=False, plural=True)}"
    elif name == "str":
        if plural:
            return f"strings"
        else:
            return f"{'a ' if a else ''}string"
    elif name == "int":
        if plural:
            return f"integers"
        else:
            return f"{'a ' if a else ''}integer"
    elif name == "bool":
        if plural:
            return f"booleans"
        else:
            return f"{'a ' if a else ''}boolean"
    elif name == "none":
        if plural:
            return "None values"
        else:
            return "nothing/None"
    elif name == "any":
        if plural:
            return "objects of any type"
        else:
            return "a object of any type" if a else "object of any type"
    elif name == "union":
        if len(thing.args) == 2 and any(i.name == "None" for i in thing.args):
            return f"optional {_describe(thing.args[0], a=False, plural=False)}"
        return " or ".join(_describe(i) for i in thing.args)
    elif name == "final":
        return f"{'a ' if a else ''}final {_describe(thing.args[0], plural=plural)}"
    elif name == "anystr":
        if plural:
            return f"strings of any kind"
        else:
            return f"any kind of string"
    elif name == "awaitable":
        if plural:
            return f"awaitables that return {_describe(thing.args[0],)}"
        else:
            return f"{'a ' if a else ''}awaitable that returns {_describe(thing.args[0])}"
    elif name == "literal":
        return (
            f"only expressions that have literally the {'values' if len(thing.args) > 1 else 'value'}"
            f" {' or '.join(map(str, thing.args))}"
        )
    elif name == "annotated":
        if plural:
            return (
                f"annotated expressions with the {'values' if len(thing.args) > 1 else 'value'}"
                f" {' and '.join(map(str, thing.args))}"
            )
        else:
            return (
                f"{'an' if a else ''} annotated expression with the {'values' if len(thing.args) > 1 else 'value'}"
                f" {' and '.join(map(str, thing.args))}"
            )
    elif name.startswith("supports"):
        supports_what = name[8:]
        if plural:
            return f"objects that support {supports_what}"
        else:
            return f"a object that supports {supports_what}" if a else f"objects that support {supports_what}"
    else:
        return (
            (("a " if a else "") if not plural else "")
            + (pluralize(thing.name) if plural else thing.name)
            + (" " + _describe(thing.args[0], a=False) if len(thing.args) > 0 else "")
        )


def describe(thing: Type) -> str:
    return _describe(thing).capitalize()


def _parse_def(def_):
    if isinstance(def_, AssignmentStmt):
        yield def_.type
    elif isinstance(def_, FuncDef):
        for argument in def_.arguments:
            if argument.type_annotation:
                yield argument.type_annotation
        if def_.type and def_.type.ret_type:
            yield def_.type.ret_type
    elif isinstance(def_, ClassDef):
        for thing in def_.defs.body:
            yield from _parse_def(thing)
    elif isinstance(def_, Decorator):
        yield from _parse_def(def_.func)


def parse_code(code: str) -> Generator[Type, None, None]:
    defs = parse(code, "<code>", module=None, errors=None, options=Options()).defs
    for def_ in defs:
        yield from _parse_def(def_)


def get_json(defs):
    data = []
    for def_ in defs:
        if not def_:
            continue
        typehint_text = str(def_).replace("?", "")
        line = def_.line
        end_line = def_.end_line
        column = def_.column + 1
        end_column = column + len(typehint_text)
        description = describe(def_)

        data.append(
            {
                "typehint_text": typehint_text,
                "description": description,
                "line": line,
                "end_line": end_line,
                "column": column,
                "end_column": end_column,
            }
        )

    return data
