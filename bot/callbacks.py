from typing import Iterable


def unpack_history(callback_data: str) -> tuple[str]:
    return tuple(callback_data.split('/'))


def pack_history(history: Iterable[str]) -> str:
    return '/'.join(history)

NEXT = "N"
PAY = "P"
EXAMPLES = "E"
PRICE = "Pr"

CARD = "Crd"
STRIPE = "Stp"
LAVA = "Lv"
STARS = "St"