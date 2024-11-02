from typing import Union, Optional, List, Generator, Dict
from edsl.questions import QuestionBase

from edsl.utilities.decorators import add_edsl_version, remove_edsl_version


class Instruction:
    def __init__(
        self, name, text, preamble="You were given the following instructions:"
    ):
        self.name = name
        self.text = text
        self.preamble = preamble

    def __str__(self):
        return self.text

    def __repr__(self):
        return """Instruction(name="{}", text="{}")""".format(self.name, self.text)

    def _to_dict(self):
        return {
            "name": self.name,
            "text": self.text,
            "edsl_class_name": "Instruction",
            "preamble": self.preamble,
        }

    def add_question(self, question) -> "Survey":
        from edsl import Survey

        return Survey([self, question])

    @add_edsl_version
    def to_dict(self):
        return self._to_dict()

    def __hash__(self) -> int:
        """Return a hash of the question."""
        from edsl.utilities.utilities import dict_hash

        return dict_hash(self._to_dict())

    @classmethod
    @remove_edsl_version
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["text"],
            data.get("preamble", "You were given the following instructions:"),
        )
