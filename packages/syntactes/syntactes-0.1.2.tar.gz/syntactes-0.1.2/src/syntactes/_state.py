from typing import Iterable, Protocol

from syntactes._item import LR0Item


class State(Protocol):
    """
    State of parser automaton. A state is a set of items.
    """

    items: set

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self) -> bool: ...


class LR0State:
    """
    State of LR0 parser. A LR0 state is a set of LR0 items.
    """

    def __init__(self) -> None:
        self.number = None
        self.items = set()

    @staticmethod
    def from_items(items: Iterable[LR0Item]) -> "LR0State":
        """
        Create an LR0 state from a set of LR0 items.
        """
        state = LR0State()
        {state.add_item(item) for item in items}

        return state

    def add_item(self, item: LR0Item) -> None:
        """
        Adds an item to the state.
        """
        self.items.add(item)

    def set_number(self, number: int) -> None:
        self.number = number

    def __repr__(self) -> str:
        return f"<LR0State: {self.number}>"

    def __str__(self) -> str:
        return f"{self.number}:" + "(" + ", ".join(map(str, self.items)) + ")"

    def __hash__(self) -> int:
        return hash(frozenset(self.items))

    def __eq__(self, other) -> bool:
        if not isinstance(other, LR0State):
            return False

        return self.items == other.items
