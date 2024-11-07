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

from typing import Optional
from tiramisu.error import PropertiesOptionError, ConfigError
from .config import OutPuts
from .i18n import _


class RougailOutputExporter:
    def __init__(
        self,
        config: "Config",
        rougailconfig: "RougailConfig" = None,
        user_data_errors: Optional[list] = None,
        user_data_warnings: Optional[list] = None,
    ) -> None:
        if rougailconfig is None:
            from rougail import RougailConfig

            rougailconfig = RougailConfig
        outputs = OutPuts().get()
        output = rougailconfig["exporter.output_format"]
        if output not in outputs:
            raise Exception(
                f'cannot find output "{output}", available outputs: {list(outputs)}'
            )
        self.rougailconfig = rougailconfig
        self.config = config
        self.read_write = self.rougailconfig["exporter.read_write"]
        self.errors = []
        self.warnings = []
        if user_data_errors is None:
            user_data_errors = []
        self.user_data_errors = user_data_errors
        if user_data_warnings is None:
            user_data_warnings = []
        self.user_data_warnings = user_data_warnings
        self.formater = outputs[output](self.rougailconfig)
        self.root = self.formater.root()

    def mandatory(self):
        if not self.rougailconfig["exporter.mandatory"]:
            return
        title = False
        options_with_error = []
        try:
            mandatories = self.config.value.mandatory()
        except (ConfigError, PropertiesOptionError) as err:
            self.errors.append(f"Error in config: {err}")
            return
        for option in mandatories:
            try:
                option.value.get()
                if not title:
                    # self.errors.append("Les variables suivantes sont obligatoires mais n'ont pas de valeur :")
                    self.errors.append(
                        _("The following variables are mandatory but have no value:")
                    )
                    title = True
                self.errors.append(f"  - {option.description()}")
            except PropertiesOptionError:
                options_with_error.append(option)
        if not title:
            for idx, option in enumerate(options_with_error):
                if not idx:
                    # self.errors.append("Les variables suivantes sont inaccessibles mais sont vides et obligatoires :")
                    self.errors.append(
                        _(
                            "The following variables are inaccessible but are empty and mandatory :"
                        )
                    )
                self.errors.append(f"  - {option.description()}")

    def exporter(self) -> bool:
        self.config.property.read_write()
        self.mandatory()
        if self.read_write:
            self.config.property.read_write()
        else:
            self.config.property.read_only()
        errors = self.user_data_errors + self.errors
        if errors:
            self.formater.errors(errors)
        if self.errors:
            return False
        warnings = self.user_data_warnings + self.warnings
        if warnings:
            self.formater.warnings(warnings)
        self.formater.header()
        self.parse_options(
            self.config,
            self.root,
        )
        self.formater.end()
        return True

    def print(self) -> None:
        return self.formater.print()

    def run(self) -> None:
        self.exporter()
        return self.print()

    def parse_options(
        self,
        conf,
        parent,
    ):
        for option in conf:
            if option.isoptiondescription():
                family = parent.add_family(option)
                if option.isleadership():
                    self.parse_leadership(
                        option,
                        family,
                    )
                else:
                    self.parse_options(
                        option,
                        family,
                    )
            else:
                parent.add_variable(option)

    def parse_leadership(
        self,
        conf,
        parent,
    ):
        leader, *followers = list(conf)
        leader_values = leader.value.get()
        for idx, leader_value in enumerate(leader_values):
            leader_obj = parent.add_family(leader)
            leader_obj.add_variable(
                leader,
                value=leader_value,
                leader_index=idx,
            )
            for follower in followers:
                if follower.index() != idx:
                    continue
                leader_obj.add_variable(follower)


RougailOutput = RougailOutputExporter


__all__ = ("RougailOutputExporter",)
