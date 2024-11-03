from typing import Sequence, Union, Iterable, Optional
from queue import LifoQueue
import re

__all__ = [
    "evalToBasicType",
    "startswith",
    "LineIterator",
]


def evalToBasicType(s: str) -> Union[str, int, float]:
    """
    Evaluate a string to a basic type (str, int, float)
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    s = s.strip()
    if re.fullmatch(r"\"[^\"]*\"", s):
        # "string"
        value = s[1:-1]
    elif re.fullmatch(r"\'[^']*\'", s):
        # 'string'
        value = s[1:-1]
    elif re.fullmatch(r"\d+", s):
        # 123
        value = int(s)
    elif re.fullmatch(r"\d*\.\d+|\d+\.", s):
        # 1.23
        # .23
        # 1.
        value = float(s)
    else:
        value = s
    return value


def startswith(
    string: str,
    patterns: Sequence[str],
    regex: bool = False,
    case: bool = False,
) -> Union[re.Match, bool]:
    if regex:
        flags = re.IGNORECASE if case else 0
        for ptn in patterns:
            obj = re.match(ptn, string, flags)
            if obj:
                return obj
    else:
        string = string.strip()
        for ptn in patterns:
            if string.startswith(str(ptn)):
                return True
    return False


class LineIterator:
    def __init__(
        self,
        data: Iterable[str],
        partition: Optional[str] = None,
        chomp: bool = False,
    ) -> None:
        if not isinstance(data, Iterable):
            raise TypeError(f"data should be an iterable - {repr(data)}")
        self.last: list = []
        self.last1: str = ""
        self.line: int = 0
        self.partition = partition
        self.chomp = chomp
        self.__reg: LifoQueue = LifoQueue()
        self.__data_iter = iter(data)

    def __str__(self) -> str:
        return self.last1

    @property
    def next(self) -> str:
        if not self.__reg.empty():
            data = self.__reg.get()
        else:
            data = next(self.__data_iter)
            if self.chomp:
                data = re.sub(r"\n$", "", data)
        self.last.append(data)
        self.last1 = data
        self.line += 1
        if self.partition:
            data = data.partition(self.partition)[0]
        return data

    @property
    def peek_next(self) -> str:
        data = self.next
        self.revert(1)
        return data

    def revert(self, count: int = 1) -> None:
        if count > len(self.last):
            raise ValueError(
                f"Revert count {count} is greater than last line count {len(self.last)}"
            )
        for _ in range(count):
            self.__reg.put(self.last1)
            self.last.pop()
            self.last1 = self.last[-1]
            self.line -= 1

    def __next__(self) -> str:
        return self.next

    def __iter__(self) -> "LineIterator":
        return self
