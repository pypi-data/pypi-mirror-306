from io import TextIOWrapper
from typing import Callable, Iterator, Optional, Union, Any
from dataclasses import dataclass

from ply.lex import (
    LexToken as _LexToken,
    TOKEN,
    Lexer,
    lex,
)


__all__ = [
    "TOKEN",
    "LexToken",
    "MetaLexer",
    "BaseLexer",
    # "tokensToDict",
]


@dataclass
class LexToken(_LexToken):
    lexer: Lexer
    type: str
    value: Any
    lineno: int
    lexpos: int

    def __repr__(self) -> str:
        return super().__repr__()


class MetaLexer:
    def __new__(cls, *args, **kwargs):
        if cls is MetaLexer:
            raise TypeError("BaseLexer cannot be instantiated")
        return super().__new__(cls)

    t_ignore = " \t"

    def t_error(self, t):
        t.lexer.skip(1)

    def __init__(
        self,
        data: Optional[str] = None,
        *,
        cb_input: Optional[Callable] = None,
        cb_token: Optional[Callable] = None,
    ):
        self.lexer = lex(module=self, debug=False)
        self.lexer.callback = {
            "input": cb_input if callable(cb_input) else None,
            "token": cb_token if callable(cb_token) else None,
        }
        if data is not None:
            self.input(data)

    def input(self, data: Union[str, TextIOWrapper]):
        if isinstance(data, str):
            pass
        elif isinstance(data, TextIOWrapper):
            data = data.read()
        else:
            raise TypeError("data must be str or TextIOWrapper")
        self.lexer.input(data)
        if self.lexer.callback["input"] is not None:
            self.lexer.callback["input"](lexer=self.lexer)

    def token(self) -> Optional[LexToken]:
        t = self.lexer.token()
        if t is None:
            return None
        t = LexToken(
            lexer=self.lexer,
            type=t.type,
            value=t.value,
            lineno=t.lineno,
            lexpos=t.lexpos,
        )
        if self.lexer.callback["token"] is not None:
            self.lexer.callback["token"](lexer=self.lexer, token=t)
        return t

    def __iter__(self) -> Iterator[LexToken]:
        return self

    def __next__(self) -> LexToken:
        t = self.token()
        if t is None:
            raise StopIteration
        return t


class BaseLexer(MetaLexer):
    tokens = [
        "ID",  # abc
        "FLOAT",  # 1.23
        "INT",  # 10
    ]

    literals = """()[]{}<>+-*/=~!@#$%^&\\|;:'",.?_"""

    def t_ID(self, t: LexToken):
        r"[a-zA-Z_]\w*"
        return t

    def t_FLOAT(self, t: LexToken):
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    def t_INT(self, t: LexToken):
        r"\d+(?!\.)"
        t.value = int(t.value)
        return t

    def t_newline(self, t: LexToken):
        r"\n+"
        t.lexer.lineno += len(t.value)
