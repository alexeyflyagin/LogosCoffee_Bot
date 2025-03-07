import random
from typing import Type


def b(it: str) -> str:
    return f"<b>{it}</b>"

def code(it: str) -> str:
    return f"<code>{it}</code>"

def i(it: str) -> str:
    return f"<i>{it}</i>"

def quote(it: str) -> str:
    return f"<blockquote>{it}</blockquote>"

class StrGroup:
    pass

def random_str(str_group: Type[StrGroup], **kwargs) -> str:
    ignore_items = '__doc__', '__module__'
    items = str_group.__dict__.items()
    strings = [y for x, y in items if x not in ignore_items if isinstance(y, str)]
    if not strings:
        return ""
    return (random.choice(strings)).format(**kwargs)



