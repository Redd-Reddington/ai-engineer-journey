"""Plain data classes: Book, EBook, Member."""

from dataclasses import dataclass, field
from datetime import date
from typing import ClassVar


@dataclass(frozen=True)
class Book:
    isbn: str
    title: str
    author: str
    year: int

    def __post_init__(self):
        if not self.isbn.strip():
            raise ValueError("ISBN cannot be empty")
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.year > date.today().year:
            raise ValueError("Publication year cannot be in the future")

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


@dataclass(frozen=True)
class EBook(Book):
    file_size_mb: float

    def __post_init__(self):
        super().__post_init__()
        if self.file_size_mb <= 0:
            raise ValueError("File size must be positive")

    def __str__(self):
        return f"{super().__str__()} [eBook, {self.file_size_mb} MB]"


@dataclass
class Member:
    member_id: int
    name: str
    email: str = field(repr=False)
    borrowed: list[Book] = field(default_factory=list)
    joined: date = field(default_factory=date.today)

    MAX_LOANS: ClassVar[int] = 3

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

    @property
    def can_borrow(self) -> bool:
        return len(self.borrowed) < self.MAX_LOANS
