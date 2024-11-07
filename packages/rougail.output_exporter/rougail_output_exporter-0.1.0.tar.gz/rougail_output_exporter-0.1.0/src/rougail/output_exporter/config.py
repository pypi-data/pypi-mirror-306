"""
Config file for Rougail-exporter

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
    module_name = "rougail.output_exporter.output"
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
                f'duplicated level rougail-exporter for output "{level}": {module.Formater.name} and {outputs[level].name}'
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
    outputs = tuple(OutPuts().get())
    options = """
exporter:
  description: Configuration rougail-exporter
  disabled:
    type: jinja
    jinja: |
      {% if step.output != 'exporter' %}
      disabled
      {% endif %}
  read_write:
    description: Display variables available in read_write mode
    negative_description: Display variables available in read_only mode
    alternative_name: er
    default: false
  show_secrets:
    description: Show secrets instead of obscuring them
    negative_description: Obscuring secrets instead of show them
    alternative_name: es
    default: false
  mandatory:
    description: Test mandatories variable before export
    negative_description: Do not test mandatories variable before export
    alternative_name: em
    default: true
  output_format:
    description: Generate document in format
    alternative_name: eo
    default: DEFAULT
    choices:
""".replace(
        "DEFAULT", outputs[0]
    )
    for output in outputs:
        options += f"      - {output}\n"
    return {
        "name": "exporter",
        "process": "output",
        "options": options,
        "level": 40,
    }


__all__ = ("OutPuts", "get_rougail_config")
