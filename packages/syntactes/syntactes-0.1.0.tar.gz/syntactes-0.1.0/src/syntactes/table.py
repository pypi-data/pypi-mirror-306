from typing import Iterable, Optional, TypeAlias

from syntactes._action import Action
from syntactes._state import State
from syntactes.grammar import Grammar
from syntactes.token import Token

Row: TypeAlias = dict[Token, list[Action]]


class Entry:
    """
    An entry of the parsing table. Holds the information of a transition from
    a state to another state via a symbol.
    """

    def __init__(self, from_state: State, token: Token, action: Action) -> None:
        self.from_state = from_state
        self.token = token
        self.action = action

    def __repr__(self) -> str:
        return f"<Entry: {str(self)}>"

    def __str__(self) -> str:
        return f"{self.from_state.number}, {self.action}, {self.token}"

    def __hash__(self) -> int:
        return hash((self.from_state, self.token, self.action))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entry):
            return False

        return (
            self.from_state == other.from_state
            and self.token == other.token
            and self.action == other.action
        )


class ParsingTable:
    """
    Table that contains all the transitions from state to state with a symbol.
    """

    def __init__(self, grammar: Grammar) -> None:
        self.rows: dict[State, Row] = dict()
        self._grammar = grammar

    def get_actions(self, state: State, token: Token) -> Optional[list[Action]]:
        """
        Get the actions from state with given number with `token`.
        If there are no actions, returns None.
        """
        return self.rows.get(state, {}).get(token, None)

    def get(self, state: State) -> Optional[Row]:
        """
        Get the mapping of tokens to actions for the given state number.
        Returns None if the state is not found.
        """
        return self.rows.get(state, None)

    def add_entry(self, entry: Entry) -> None:
        """
        Adds an entry to the parsing table.
        """
        self.rows.setdefault(entry.from_state, {}).setdefault(
            entry.token, list()
        ).append(entry.action)

    @staticmethod
    def from_entries(
        entries: Iterable[Entry], tokens: Iterable[Token]
    ) -> "ParsingTable":
        """
        Create a parsing table from the given entries.
        """
        table = ParsingTable(tokens)
        {table.add_entry(entry) for entry in entries}
        return table

    def pretty_str(self) -> str:
        """
        Returns a pretty-formatted string representation of the table.
        """
        return self._rules_pretty_str() + "\n\n" + self._table_pretty_str()

    def _rules_pretty_str(self) -> str:
        rules = [str(i) + ". " + str(r) for i, r in enumerate(self._grammar.rules)]
        rules_str = "\n".join(rules)
        rules_str = "GRAMMAR RULES\n" + "-" * max(map(len, rules)) + "\n" + rules_str
        rules_str += "\n" + "-" * max(map(len, rules))

        return rules_str

    def _table_pretty_str(self) -> str:
        rows = []
        tokens = sorted(self._grammar.tokens)
        for number, row in sorted(
            map(lambda tpl: (tpl[0].number, tpl[1]), self.rows.items())
        ):
            r = [str(number)]
            for token in sorted(tokens):
                actions = row.get(token, [])
                if len(actions) >= 1:
                    actions_str = ",".join(map(str, actions))
                else:
                    actions_str = "--"

                r.append(actions_str)

            rows.append(r)

        table = "|     |  "
        table += "   |  ".join(str(token) for token in tokens) + "  |\n"

        header = self._header_str() + "\n" + "-" * len(table) + "\n"
        table += "-" * len(table) + "\n"

        for row in rows:
            new_row = "|  " + "  |  ".join(row) + " |" + "\n"
            table += new_row
            table += "-" * len(new_row) + "\n"

        return header + table

    def _header_str(self) -> str:
        return "LR0 PARSING TABLE"
