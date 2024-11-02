class Report:
    notes: list[str]

    def __init__(self) -> None:
        self.notes = []

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}: ' f'({", ".join(str(v) for v in self.__dict__.values())})'
        )

    def add_note(self, note: str) -> None:
        self.notes.append(note)
