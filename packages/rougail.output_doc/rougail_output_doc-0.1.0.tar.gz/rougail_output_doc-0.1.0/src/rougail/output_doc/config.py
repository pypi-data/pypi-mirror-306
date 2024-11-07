"""
Config file for Rougail-doc

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

from pathlib import Path
from rougail.utils import load_modules


OUTPUTS = None


def get_outputs() -> None:
    module_name = "rougail.doc.output"
    outputs = {}
    for path in (Path(__file__).parent / "output").iterdir():
        name = path.name
        if not name.endswith(".py") or name.endswith("__.py"):
            continue
        module = load_modules(module_name + "." + name, str(path))
        if "Formater" not in dir(module):
            continue
        level = module.Formater.level
        if level in outputs:
            raise Exception(
                f'duplicated level rougail-doc for output "{level}": {module.Formater.name} and {outputs[level].name}'
            )
        outputs[module.Formater.level] = module.Formater
    return {outputs[level].name: outputs[level] for level in sorted(outputs)}


class OutPuts:  # pylint: disable=R0903
    """Transformations applied on a object instance"""

    def __init__(
        self,
    ) -> None:
        global OUTPUTS
        if OUTPUTS is None:
            OUTPUTS = get_outputs()

    def get(self) -> dict:
        return OUTPUTS


def get_rougail_config(
    *,
    backward_compatibility=True,
) -> dict:
    outputs = list(OutPuts().get())
    output_format_default = outputs[0]
    rougail_options = """
doc:
  description: Configuration rougail-doc
  disabled:
    type: jinja
    jinja: |
      {% if step.output != 'doc' %}
      disabled
      {% endif %}
  title_level:
    description: Start title level
    alternative_name: dt
    default: 1
  with_example:
    description: Display example in documentation
    negative_description: Hide example in documentation
    alternative_name: de
    default: false
  output_format:
    description: Generate document in format
    alternative_name: do
    default: output_format_default
    choices:
""".replace(
        "output_format_default", output_format_default
    )
    for output in outputs:
        rougail_options += f"      - {output}\n"
    return {
        "name": "doc",
        "process": "output",
        "options": rougail_options,
        "allow_user_data": False,
        "level": 50,
    }


__all__ = ("OutPuts", "get_rougail_config")
