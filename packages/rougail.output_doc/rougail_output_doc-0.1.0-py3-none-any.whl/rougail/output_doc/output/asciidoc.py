"""
Silique (https://www.silique.fr)
Copyright (C) 2024

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from io import BytesIO
from typing import List
from itertools import chain
from ruamel.yaml import YAML


class Formater:
    name = "asciidoc"
    level = 40

    def __init__(self):
        self._yaml = YAML()
        self._yaml.indent(mapping=2, sequence=4, offset=2)

    def header(self):
        return ""

    def title(
        self,
        title: str,
        level: int,
    ) -> str:
        char = "="
        return f"{char * (level + 1)} {title}\n\n"

    def yaml(self, dump: dict) -> str:
        return f"[,yaml]\n----\n{self.dump(dump)}\n----\n"

    def table(self, table: str) -> str:
        # add 'a' option in cols to display list
        stable = table.split("\n", 1)
        return stable[0].replace("<", "a") + "\n" + stable[1]

    def link(
        self,
        comment: str,
        link: str,
    ) -> str:
        return f"`{link}[{comment}]`"

    def prop(
        self,
        prop: str,
    ) -> str:
        return f"`{prop}`"

    def list(
        self,
        choices: list,
    ) -> str:
        prefix = "\n\n* "
        char = "\n* "
        return prefix + char.join([self.dump(choice) for choice in choices])

    def is_list(
        self,
        txt: str,
    ) -> str:
        return txt.startswith("* ")

    def columns(
        self,
        col1: List[str],
        col2: List[str],
    ) -> None:
        self.max_line = 0
        for params in chain(col1, col2):
            for param in params.split("\n"):
                self.max_line = max(self.max_line, len(param))
        self.max_line += 1

    def join(
        self,
        lst: List[str],
    ) -> str:
        string = ""
        previous = ""
        for line in lst:
            if string:
                if self.is_list(previous.split("\n")[-1]):
                    string += "\n\n"
                else:
                    string += " +\n"
            string += line

            previous = line
        return "\n" + string

    def to_string(
        self,
        text: str,
    ) -> str:
        return text

    def table_header(
        self,
        lst,
    ):
        return lst[0] + " " * (self.max_line - len(lst[0])), lst[1] + " " * (
            self.max_line - len(lst[1])
        )

    def bold(
        self,
        msg: str,
    ) -> str:
        return f"**{msg}**"

    def italic(
        self,
        msg: str,
    ) -> str:
        return f"_{msg}_"

    def dump(self, dico):
        with BytesIO() as ymlfh:
            self._yaml.dump(dico, ymlfh)
            ret = ymlfh.getvalue().decode("utf-8").strip()
        if ret.endswith("..."):
            ret = ret[:-3].strip()
        return ret
