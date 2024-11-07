"""
Silique (https://www.silique.fr)
Copyright (C) 2022-2024
            
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

from typing import Any, List, Optional

from rich.tree import Tree
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from tiramisu import undefined
from ...i18n import _


class Formater:
    name = "console"
    level = 10
    variable_hidden_color = "orange1"
    variable_advanced_color = "bright_blue"
    variable_advanced_and_modified_color = "red1"
    value_unmodified_color = "gold1"
    value_default_color = "green"

    def __init__(
        self,
        rougailconfig: "RougailConfig",
    ) -> None:
        self.console = Console(force_terminal=True)
        self.rougailconfig = rougailconfig
        self.read_write = self.rougailconfig["exporter.read_write"]
        self.show_secrets = self.rougailconfig["exporter.show_secrets"]
        self.out = []

    def header(self):
        header_variable = "Variable\n"
        # header_variable += f'[{self.variable_advanced_color}]Variable non documentée[/{self.variable_advanced_color}]\n'
        # header_variable += f'[{self.variable_advanced_and_modified_color}]Variable non documentée mais modifiée[/{self.variable_advanced_and_modified_color}]'
        header_variable += f'[{self.variable_advanced_color}]{_("Undocumented variable")}[/{self.variable_advanced_color}]\n'
        header_variable += f'[{self.variable_advanced_and_modified_color}]{_("Undocumented but modified variable")}[/{self.variable_advanced_and_modified_color}]'
        if not self.read_write:
            # header_variable += f'\n[{self.variable_hidden_color}]Variable non modifiable[/{self.variable_hidden_color}]'
            header_variable += f'\n[{self.variable_hidden_color}]{_("Unmodifiable variable")}[/{self.variable_hidden_color}]'
        # header_value = f'[{self.value_unmodified_color}]Valeur par défaut[/{self.value_unmodified_color}]\n'
        # header_value += 'Valeur modifiée\n'
        # header_value += f'([{self.value_default_color}]Valeur par défaut originale[/{self.value_default_color}])'
        header_value = f'[{self.value_unmodified_color}]{_("Default value")}[/{self.value_unmodified_color}]\n'
        header_value += _("Modified value") + "\n"
        header_value += f'([{self.value_default_color}]{_("Original default value")}[/{self.value_default_color}])'
        header = Table.grid(padding=1, collapse_padding=True)
        header.pad_edge = False
        header.add_row(header_variable, header_value)
        self.out.append(Panel.fit(header, title=_("Caption")))

    def errors(
        self,
        errors,
    ) -> None:
        tree = Tree(
            ":stop_sign: ERRORS",
            guide_style="bold bright_red",
        )
        for error in errors:
            tree.add(error)
        self.out.append(tree)

    def warnings(
        self,
        warnings: list,
    ) -> None:
        tree = Tree(":warning: WARNINGS")
        for warning in warnings:
            tree.add(warning)
        self.out.append(tree)

    def root(self) -> None:
        self.output = OutputFamily(
            _("Variables:"),
            None,
            self,
            no_icon=True,
        )
        return self.output

    def end(self):
        self.out.append(self.output.tree)

    def print(self):
        for out in self.out:
            self.console.print(out)


class OutputFamily:
    def __init__(
        self, family, parent, root, *, is_leader: bool = False, no_icon: bool = False
    ) -> None:
        if parent is None:
            tree = Tree
        else:
            tree = parent.add
        if is_leader:
            self.tree = tree(
                f":notebook: {family} :",
                guide_style="bold bright_blue",
            )
        elif no_icon:
            self.tree = tree(
                f"{family}",
                guide_style="bold bright_blue",
            )
        else:
            self.tree = tree(
                f":open_file_folder: {family}",
                guide_style="bold bright_blue",
            )
        self.root = root

    #
    #    def parse_option(self,
    #                     option,
    #                     value,
    #                     variables,
    #                     ):
    #        if '.' in line:
    #            # it's a dict
    #            family, variable = line.split('.', 1)
    #            current_path = parent_path
    #            if current_path:
    #                current_path += '.'
    #            current_path += family
    #            if for_doc:
    #                if 'hidden' in self.conf.option(current_path).property.get() or family_hidden:
    #                    family_hidden = True
    #                    family = f'[orange1]{family}[/orange1]'
    #                elif 'advanced' in self.conf.option(current_path).property.get():
    #                    family = f'[bright_blue]{family}[/bright_blue]'
    #            if '.' not in variable and self.conf.option(full_path.rsplit('.', 1)[0]).isleadership():
    #                dico.setdefault(family, [])
    #                leadership = True
    #            else:
    #                dico.setdefault(family, {})
    #                leadership = False
    #            self.parse_option(full_path,
    #                              variable,
    #                              value,
    #                              )
    #        elif leadership:
    #            # it's a leadership
    #            for idx, val in enumerate(value):
    #                dic = {k.rsplit('.', 1)[-1]: v for k, v in val.items()}
    #                if for_doc:
    #                    leader = True
    #                    for k, v in val.items():
    #                        if leader:
    #                            is_default = self.conf.option(k).owner.isdefault()
    #                            properties = self.conf.option(k).property.get()
    #                        else:
    #                            is_default = self.conf.option(k, idx).owner.isdefault()
    #                            properties = self.conf.option(k, idx).property.get()
    #                        if self.conf.option(k).type() == _('password') and not self.args.show_secrets:
    #                            v = "*" * 10
    #                        subpath = k.rsplit('.', 1)[-1]
    #                        if 'hidden' in properties or family_hidden:
    #                            subpath = f'[orange1]{subpath}[/orange1]'
    #                        elif 'advanced' in properties:
    #                            if isdefault:
    #                                subpath = f'[bright_blue]{subpath}[/bright_blue]'
    #                            else:
    #                                subpath = f'[red1]{subpath}[/red1]'
    #                        if is_default:
    #                            v = '[gold1]' + str(v) + '[/gold1]'
    #                        dico.append(f'{subpath}: {v}')
    #                        leader = False
    #                else:
    #                    dico.append(dic)
    #        else:
    #            # it's a variable
    #            self.parse_variable(option, value)
    #
    def add_family(
        self,
        option,
    ) -> None:
        properties = option.property.get()
        if "hidden" in properties:
            color = self.root.variable_hidden_color
        elif "advanced" in properties:
            color = self.root.variable_advanced_color
        else:
            color = None
        return OutputFamily(
            self.colorize(
                None,
                option.name(),
                color,
                None,
            ),
            self.tree,
            self.root,
        )

    def add_variable(
        self, option, value: Any = undefined, leader_index: Optional[int] = None
    ):
        properties = option.property.get()
        variable_color = None
        if option.owner.isdefault():
            if "hidden" in properties:
                variable_color = self.root.variable_hidden_color
            elif "advanced" in properties:
                variable_color = self.root.variable_advanced_color
            color = self.root.value_unmodified_color
            default_value = None
        else:
            if "hidden" in properties:
                variable_color = self.root.variable_hidden_color
            elif "advanced" in properties:
                variable_color = self.root.variable_advanced_and_modified_color
            color = None
            default_value = option.value.default()
            if leader_index is not None and len(default_value) > leader_index:
                default_value = default_value[leader_index]
        if value is undefined:
            value = option.value.get()
        key = self.colorize(
            None,
            option.name(),
            variable_color,
            None,
        )
        value = self.colorize(
            option,
            value,
            color,
            default_value,
        )
        if isinstance(value, list):
            subtree = self.tree.add(
                f":notebook: {key} :",
                guide_style="bold bright_blue",
            )
            for val in value:
                subtree.add(str(val))
        else:
            self.tree.add(f":notebook: {key}: {value}")

    def colorize(
        self,
        option,
        value,
        color: str,
        default_value,
    ) -> str:
        if isinstance(value, list):
            if default_value is None:
                default_value = []
            len_value = len(value)
            len_default_value = len(default_value)
            len_values = max(len_value, len_default_value)
            ret = []
            for idx in range(len_values):
                if idx < len_value:
                    val = value[idx]
                else:
                    val = ""
                if idx < len_default_value:
                    if val:
                        val += " "
                    default = default_value[idx]
                else:
                    default = None
                ret.append(
                    self.colorize(
                        option,
                        val,
                        color,
                        default,
                    )
                )
            return ret
        if option and value is not None:
            value = self.convert_value(
                option,
                value,
            )
        else:
            value = str(value)
        if color is not None:
            ret = f"[{color}]{value}[/{color}]"
        else:
            ret = value
        if default_value and "force_store_value" not in option.property.get():
            default_value_color = self.root.value_default_color
            ret += f" ([{default_value_color}]{default_value}[/{default_value_color}])"
        return ret

    def convert_value(
        self,
        option,
        value,
    ):
        if not self.root.show_secrets and option.type() == "password":
            return "*" * 10
        return str(value)
