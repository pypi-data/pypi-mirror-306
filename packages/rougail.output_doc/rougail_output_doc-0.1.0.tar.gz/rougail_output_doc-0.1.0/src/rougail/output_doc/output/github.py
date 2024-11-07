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
    name = "github"
    level = 50

    def __init__(self):
        self._yaml = YAML()
        self._yaml.indent(mapping=2, sequence=4, offset=2)
        self.header_setted = False

    def header(self):
        if self.header_setted:
            return ""
        self.header_setted = True
        return "---\ngitea: none\ninclude_toc: true\n---\n"

    def title(
        self,
        title: str,
        level: int,
    ) -> str:
        char = "#"
        return f"{char * level} {title}\n\n"

    def yaml(self, dump):
        return f"```yaml\n---\n{self.dump(dump)}\n```\n"

    def table(self, table):
        return table

    def link(
        self,
        comment: str,
        link: str,
    ) -> str:
        return f"[`{comment}`]({link})"

    def prop(
        self,
        prop: str,
    ) -> str:
        return f"`{prop}`"

    def list(
        self,
        choices,
    ):
        prefix = "<br/>- "
        char = "<br/>- "
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
        return "<br/>".join(lst)

    def to_string(
        self,
        text: str,
    ) -> str:
        return text.strip().replace("\n", "<br/>")

    def table_header(self, lst):
        return lst[0] + "&nbsp;" * (self.max_line - len(lst[0])), lst[1] + "&nbsp;" * (
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
        return f"*{msg}*"

    def dump(self, dico):
        with BytesIO() as ymlfh:
            self._yaml.dump(dico, ymlfh)
            ret = ymlfh.getvalue().decode("utf-8").strip()
        if ret.endswith("..."):
            ret = ret[:-3].strip()
        return ret
