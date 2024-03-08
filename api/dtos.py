from dataclasses import dataclass, field
import uuid
from typing import List
from .models import OffenseTrait, Joke


@dataclass
class Jokometian:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    traits: List[OffenseTrait] = field(default_factory=list)
    jokes: List[Joke] = field(default_factory=list)
    name: str = ""
    description: str = ""
    image_url: str = ""
