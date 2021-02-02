from dataclasses import dataclass
from typing import List


@dataclass
class Pokemon:
    name: str
    link: str
    image_link: str
    number: int
    generation: int
    poke_type: List[str]
    weight: float
    height: float
    species: str

