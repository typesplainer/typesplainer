import unittest

from typesplainer.core import SUPPORTED_TYPES, describe, parse_code


SAMPLE_ALIAS_EXPRESSIONS = {
    "Callable": "Callable[[str], int]",
    "Optional": "Optional[int]",
    "Generator": "Generator[int, None, str]",
    "Coroutine": "Coroutine[int, None, str]",
    "AsyncGenerator": "AsyncGenerator[int, None]",
    "Dict": "Dict[str, int]",
    "dict": "dict[str, int]",
    "Mapping": "Mapping[str, int]",
    "OrderedDict": "OrderedDict[str, int]",
    "DefaultDict": "DefaultDict[str, int]",
    "List": "List[int]",
    "list": "list[int]",
    "Set": "Set[int]",
    "Tuple": "Tuple[str, int]",
    "NamedTuple": "NamedTuple[str, int]",
    "namedtuple": "namedtuple[str, int]",
    "FrozenSet": "FrozenSet[int]",
    "frozenset": "frozenset[int]",
    "Sequence": "Sequence[int]",
    "Iterable": "Iterable[int]",
    "str": "str",
    "int": "int",
    "bool": "bool",
    "none": "none",
    "Any": "Any",
    "Union": "Union[int, str]",
    "Final": "Final[int]",
    "AnyStr": "AnyStr",
    "Awaitable": "Awaitable[int]",
    "Literal": "Literal[1]",
    "IO": "IO[str]",
    "BytesIO": "BytesIO",
    "TextIO": "TextIO",
    "StringIO": "StringIO",
    "Match": "Match[str]",
    "Pattern": "Pattern[str]",
    "Reversible": "Reversible[int]",
    "Hashable": "Hashable",
    "Iterator": "Iterator[int]",
    "AsyncIterator": "AsyncIterator[int]",
    "ContextManager": "ContextManager[str]",
    "AsyncContextManager": "AsyncContextManager[str]",
    "Annotated": "Annotated[int, 'meta']",
    "SupportsAbs": "SupportsAbs",
    "SupportsBytes": "SupportsBytes",
    "SupportsComplex": "SupportsComplex",
    "SupportsFloat": "SupportsFloat",
    "SupportsIndex": "SupportsIndex",
    "SupportsInt": "SupportsInt",
    "SupportsRound": "SupportsRound",
    "MutableMapping": "MutableMapping[str, int]",
    "MutableSet": "MutableSet[int]",
    "MutableSequence": "MutableSequence[int]",
}


class TypeAliasParsingTests(unittest.TestCase):
    def test_all_supported_types_have_alias_test_coverage(self):
        self.assertEqual(set(SUPPORTED_TYPES), set(SAMPLE_ALIAS_EXPRESSIONS))

    def test_parse_code_supports_aliases_for_all_supported_types(self):
        code = "\n".join(
            f"Alias_{index} = {SAMPLE_ALIAS_EXPRESSIONS[type_name]}"
            for index, type_name in enumerate(SUPPORTED_TYPES, start=1)
        )

        parsed_types = list(parse_code(code))

        self.assertEqual(
            {parsed_type.line for parsed_type in parsed_types},
            set(range(1, len(SUPPORTED_TYPES) + 1)),
        )

    def test_parse_code_ignores_regular_object_indexing_assignments(self):
        code = "\n".join(
            [
                "ListVar = [1, 2, 3]",
                "item = ListVar[0]",
                "IntegerList = List[int]",
            ]
        )

        parsed_types = list(parse_code(code))

        self.assertEqual(len(parsed_types), 1)
        self.assertEqual(parsed_types[0].line, 3)

    def test_any_description_uses_correct_article(self):
        parsed_types = list(parse_code("thing: Any"))

        self.assertEqual(describe(parsed_types[0]), "An object of any type.")


if __name__ == "__main__":
    unittest.main()
