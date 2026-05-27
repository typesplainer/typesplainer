import unittest

from typesplainer.core import SUPPORTED_TYPES, describe, parse_code


BASE_CASES_BY_TYPE = {
    "Callable": ("Callable[[str], int]", "A callable that accepts a string and returns a integer."),
    "Optional": ("Optional[int]", "A optional integer."),
    "Generator": ("Generator[int, None, str]", "A generator that yields a integer, sends nothing/none, and returns a string."),
    "Coroutine": ("Coroutine[int, None, str]", "A coroutine that yields a integer, sends nothing/none, and returns a string."),
    "AsyncGenerator": ("AsyncGenerator[int]", "An async generator that yields a integer."),
    "Dict": ("Dict[str, int]", "A dictionary that maps strings onto a integer."),
    "dict": ("dict[str, int]", "A dictionary that maps strings onto a integer."),
    "Mapping": ("Mapping[str, int]", "A mapping that maps strings onto a integer."),
    "OrderedDict": ("OrderedDict[str, int]", "A ordered dictionary that maps strings onto a integer."),
    "DefaultDict": ("DefaultDict[str, int]", "A default dictionary that maps strings onto a integer."),
    "List": ("List[int]", "A list of integers."),
    "list": ("list[int]", "A list of integers."),
    "Set": ("Set[int]", "A set of integers."),
    "Tuple": ("Tuple[str, int]", "A tuple of strings."),
    "NamedTuple": ("NamedTuple[str]", "A namedtuple of strings."),
    "namedtuple": ("namedtuple[str]", "A namedtuple of strings."),
    "FrozenSet": ("FrozenSet[int]", "A frozenset of integers."),
    "frozenset": ("frozenset[int]", "A frozenset of integers."),
    "Sequence": ("Sequence[int]", "A sequence of integers."),
    "Iterable": ("Iterable[int]", "A iterable of integers."),
    "str": ("str", "A string."),
    "int": ("int", "A integer."),
    "float": ("float", "A float."),
    "bytes": ("bytes", "A byte string."),
    "complex": ("complex", "A complex number."),
    "object": ("object", "An object."),
    "bool": ("bool", "A boolean."),
    "none": ("none", "Nothing/none."),
    "Any": ("Any", "An object of any type."),
    "Union": ("Union[int, str]", "A integer or a string."),
    "Final": ("Final[int]", "A final a integer."),
    "AnyStr": ("AnyStr", "Any kind of string."),
    "Awaitable": ("Awaitable[int]", "A awaitable that returns a integer."),
    "Literal": ("Literal[1]", "Only expressions that have literally the value 1."),
    "IO": ("IO", "An i/o stream."),
    "BytesIO": ("BytesIO", "An i/o stream of bytes."),
    "TextIO": ("TextIO", "An i/o stream of text."),
    "StringIO": ("StringIO", "An i/o stream of string."),
    "Match": ("Match[str]", "A regex match object."),
    "Pattern": ("Pattern[str]", "A regex pattern object."),
    "Reversible": ("Reversible[int]", "A iterable object with a __reversed__() method."),
    "Hashable": ("Hashable", "A object with a __hash__() method."),
    "Iterator": ("Iterator[int]", "A iterable object with a __iter__() and a __next__() method."),
    "AsyncIterator": ("AsyncIterator[int]", "A object with a __aiter__() and a __anext__() method."),
    "ContextManager": ("ContextManager[str]", "A  context manager."),
    "AsyncContextManager": ("AsyncContextManager[str]", "A asynchronous  context manager."),
    "Annotated": ("Annotated[int]", "An annotated expression with the value int?."),
    "SupportsAbs": ("SupportsAbs", "An object that supports abs."),
    "SupportsBytes": ("SupportsBytes", "An object that supports bytes."),
    "SupportsComplex": ("SupportsComplex", "An object that supports complex."),
    "SupportsFloat": ("SupportsFloat", "An object that supports float."),
    "SupportsIndex": ("SupportsIndex", "An object that supports index."),
    "SupportsInt": ("SupportsInt", "An object that supports int."),
    "SupportsRound": ("SupportsRound", "An object that supports round."),
    "MutableMapping": ("MutableMapping[str, int]", "A mutable mapping object."),
    "MutableSet": ("MutableSet[int]", "A mutable set object."),
    "MutableSequence": ("MutableSequence[int]", "A mutable sequence object."),
}

NUANCE_CASES_BY_TYPE = {
    "AsyncGenerator": [
        ("AsyncGenerator[int, str]", "An async generator that yields a integer, sends a string."),
    ],
    "Dict": [
        ("Dict", "A dictionary of any object."),
    ],
    "dict": [
        ("dict", "A dictionary of any object."),
    ],
    "Mapping": [
        ("Mapping", "A mapping of any object."),
    ],
    "OrderedDict": [
        ("OrderedDict", "A ordered dictionary of any object."),
    ],
    "DefaultDict": [
        ("DefaultDict", "A default dictionary of any object."),
    ],
    "List": [
        ("List", "A list of any object."),
    ],
    "list": [
        ("list", "A list of any object."),
    ],
    "Set": [
        ("Set", "A set of any object."),
    ],
    "Tuple": [
        ("Tuple", "A tuple of any object."),
    ],
    "NamedTuple": [
        ("NamedTuple", "A namedtuple of any object."),
    ],
    "namedtuple": [
        ("namedtuple", "A namedtuple of any object."),
    ],
    "FrozenSet": [
        ("FrozenSet", "A frozenset of any object."),
    ],
    "frozenset": [
        ("frozenset", "A frozenset of any object."),
    ],
    "Sequence": [
        ("Sequence", "A sequence of any object."),
    ],
    "Iterable": [
        ("Iterable", "A iterable of any object."),
    ],
    "Union": [
        ("Union[int, None]", "Optional integer."),
        ("Union[None, int]", "Optional integer."),
        ("Union[int, str, bool]", "A integer or a string or a boolean."),
    ],
    "Awaitable": [
        ("Awaitable", "A awaitable."),
    ],
    "Literal": [
        ("Literal[1, 2]", "Only expressions that have literally the values 1 or 2."),
    ],
    "bytes": [
        ("bytes", "A byte string."),
    ],
    "IO": [
        ("IO[str]", "An i/o stream."),
    ],
    "Annotated": [
        ("Annotated[int, \"meta\", \"tag\"]", "An annotated expression with the values int? and meta? and tag?."),
    ],
}


def _describe_annotation(expression: str) -> str:
    parsed = list(parse_code(f"value: {expression}"))
    assert len(parsed) == 1
    return describe(parsed[0])


def _describe_alias(expression: str) -> str:
    parsed = list(parse_code(f"Alias = {expression}"))
    assert len(parsed) == 1
    return describe(parsed[0])


class AnnotationDescriptionCoverageTests(unittest.TestCase):
    def test_every_supported_type_has_a_base_output_test(self):
        self.assertEqual(set(SUPPORTED_TYPES), set(BASE_CASES_BY_TYPE))

    def test_base_outputs_match_expected_explanations(self):
        for supported_type in SUPPORTED_TYPES:
            expression, expected = BASE_CASES_BY_TYPE[supported_type]
            with self.subTest(type=supported_type, expression=expression):
                self.assertEqual(_describe_annotation(expression), expected)

    def test_nuance_outputs_match_expected_explanations(self):
        for supported_type, nuance_cases in NUANCE_CASES_BY_TYPE.items():
            for expression, expected in nuance_cases:
                with self.subTest(type=supported_type, expression=expression):
                    self.assertEqual(_describe_annotation(expression), expected)


class AliasDescriptionCoverageTests(unittest.TestCase):
    def test_alias_outputs_match_expected_explanations_for_each_supported_type(self):
        for supported_type in SUPPORTED_TYPES:
            expression, expected = BASE_CASES_BY_TYPE[supported_type]
            with self.subTest(type=supported_type, expression=expression):
                self.assertEqual(_describe_alias(expression), expected)


if __name__ == "__main__":
    unittest.main()
