from dataclasses import dataclass, field
from enum import Flag, auto
from typing import List


class TargetGender(Flag):
    MALE = auto()
    FEMALE = auto()


@dataclass
class GiftItem:
    id: int
    name: str
    url: str
    photo: str
    price_rub: int
    categories: List[str] = field(default_factory=list)
    gender: TargetGender = field(default=TargetGender.MALE & TargetGender.FEMALE)
