from typing import Dict

__all__ = [
    "getSubClassDict",
]


def getSubClassDict(cls, cls_dict: Dict[str, object] = {}) -> Dict[str, object]:
    for subclass in cls.__subclasses__():
        cls_dict[subclass.__name__] = subclass
        getSubClassDict(subclass, cls_dict)
    return cls_dict
