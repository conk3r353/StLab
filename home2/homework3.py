import dataclasses
import typing


@dataclasses.dataclass(order=True)
class Student:
    name: str = dataclasses.field(repr=True, compare=False)
    average_mark: float = dataclasses.field(repr=True, compare=True)
    age: int = dataclasses.field(repr=False, default=18, compare=False)
    subjects: typing.List[str] = dataclasses.field(repr=False, default_factory=lambda: [], compare=False)

    def __post_init__(self):
        if self.name == '':
            self.first_letter = None
        else:
            self.first_letter = self.name[0]
