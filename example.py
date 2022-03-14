from typing import *

class Text:
  pass

def life(
  f: Callable[[str, int], Generator[int, str, bool]],
  g: Awaitable[Sequence[Text]]
) -> Dict[List[Set[FrozenSet[int]]], str]:
  return {[{frozenset(42)}]: "Hello World!"}

fromkeys: Callable[[List[int]], Dict[int, List[Union[Segment, None]]]]