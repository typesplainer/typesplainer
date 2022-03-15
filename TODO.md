# Todo

- [ ] Implement things such as

    ```python
    SomeRandomType = Union[
        Tuple[str, int],
        Tuple[str, int, Optional[int]],
        Tuple[str, int, Optional[int], Optional[Callable[[str], Any]]],
    ]
    ```