from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    title: str
    year: int
    rating: float
    genre: str

    @classmethod
    def from_tuple(cls, row: tuple):
        if not row:
            return None
        return cls(id=row[0], title=row[1], year=row[2], rating=row[3], genre=row[4])