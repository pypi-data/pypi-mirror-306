"""Annotate for documentation

Silique (https://www.silique.fr)
Copyright (C) 2024

distribued with GPL-2 or later license

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from tiramisu import undefined
from rougail.annotator.variable import Walk

from rougail.i18n import _
from rougail.error import DictConsistencyError
from rougail.object_model import (
    Calculation,
    JinjaCalculation,
    VariableCalculation,
    VariablePropertyCalculation,
    IdentifierCalculation,
    IdentifierPropertyCalculation,
    InformationCalculation,
    IndexCalculation,
    CONVERT_OPTION,
    PROPERTY_ATTRIBUTE,
)


class Annotator(Walk):
    """Annotate for documentation"""

    level = 95

    def __init__(
        self,
        objectspace,
        *args,
    ) -> None:
        if not objectspace.paths:
            return
        self.objectspace = objectspace
        self.populate_family()
        self.populate_variable()

    def get_examples_values(self, variable):
        values = self.objectspace.informations.get(variable.path).get("examples", None)
        if not values:
            values = self.objectspace.informations.get(variable.path).get("test", None)
        if isinstance(values, tuple):
            values = list(values)
        return values

    def add_default_value(
        self,
        family,
        value,
        *,
        inside_list=False,
    ) -> None:
        if isinstance(value, Calculation):
            default_values = "example"
            if not inside_list:
                default_values = [default_values]
            if isinstance(value, (VariableCalculation, VariablePropertyCalculation)):
                variable, identifier = self.objectspace.paths.get_with_dynamic(
                    value.variable,
                    value.path_prefix,
                    family.path,
                    value.version,
                    value.namespace,
                    value.xmlfiles,
                )
                values = self.get_examples_values(variable)
                if values:
                    if inside_list:
                        default_values = list(values)
                    else:
                        default_values = values
            value.default_values = default_values

    def populate_family(self) -> None:
        """Set doc, path, ... to family"""
        for family in self.get_families():
            self.objectspace.informations.add(
                family.path, "dictionaries", family.xmlfiles
            )
            self.convert_variable_property(family)
            if family.type != "dynamic":
                continue
            if not isinstance(family.dynamic, list):
                self.add_default_value(family, family.dynamic)
            else:
                for value in family.dynamic:
                    self.add_default_value(family, value, inside_list=True)
            self.calculation_to_information(
                family.path,
                "dynamic",
                family.dynamic,
                family.version,
            )

    def populate_variable(self) -> None:
        """convert variables"""
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            if variable.type == "choice":
                self.calculation_to_information(
                    variable.path,
                    "choice",
                    variable.choices,
                    variable.version,
                )
            self.calculation_to_information(
                variable.path,
                "default",
                variable.default,
                variable.version,
            )
            self.calculation_to_information(
                variable.path,
                "validators",
                variable.validators,
                variable.version,
            )
            if variable.path in self.objectspace.leaders and not variable.default:
                values = self.get_examples_values(variable)
                if values:
                    variable.default = list(values)
                else:
                    variable.default = [CONVERT_OPTION[variable.type]["example"]]
                self.objectspace.informations.add(variable.path, "fake_default", True)
            self.objectspace.informations.add(
                variable.path, "dictionaries", variable.xmlfiles
            )
            self.convert_variable_property(variable)

    def convert_variable_property(
        self,
        variable: dict,
    ) -> None:
        """convert properties"""
        for prop in ["hidden", "disabled", "mandatory"]:
            prop_value = getattr(variable, prop, None)
            if not prop_value:
                continue
            self.calculation_to_information(
                variable.path,
                prop,
                prop_value,
                variable.version,
            )

    def calculation_to_information(
        self,
        path: str,
        prop: str,
        values,
        version: str,
    ):
        self._calculation_to_information(
            path,
            prop,
            values,
            version,
        )
        if isinstance(values, list):
            for idx, val in enumerate(values):
                self._calculation_to_information(
                    path,
                    prop,
                    val,
                    version,
                    identifier=f"_{idx}",
                )

    def _calculation_to_information(
        self,
        path: str,
        prop: str,
        values,
        version: str,
        *,
        identifier: str = "",
    ):
        if not isinstance(values, Calculation):
            return
        values_calculation = True
        if isinstance(values, JinjaCalculation):
            if values.description:
                values_calculation = values.description
            values_calculation_type = "jinja"
        elif isinstance(values, (VariableCalculation, VariablePropertyCalculation)):
            values_calculation = values.variable
            paths = self.objectspace.paths
            if version != "1.0" and paths.regexp_relative.search(values_calculation):
                calculation_path = paths.get_full_path(
                    values_calculation,
                    path,
                )
                if prop in PROPERTY_ATTRIBUTE:
                    if values.when is not undefined:
                        values_calculation = f'when the variable "{calculation_path}" has the value "{values.when}"'
                    elif values.when_not is not undefined:
                        values_calculation = f'when the variable "{calculation_path}" hasn\'t the value "{values.when_not}"'
                    else:
                        values_calculation = f'when the variable "{calculation_path}" has the value "True"'
                else:
                    values_calculation = calculation_path
            values_calculation_type = "variable"
        elif isinstance(values, InformationCalculation):
            values_calculation_type = "information"
        elif isinstance(values, (IdentifierCalculation, IdentifierPropertyCalculation)):
            if version != "1.0" and prop in PROPERTY_ATTRIBUTE:
                if values.when is not undefined:
                    values_calculation = f'when the identifier is "{values.when}"'
                elif values.when_not is not undefined:
                    values_calculation = (
                        f'when the identifier is not "{values.when_not}"'
                    )
            values_calculation_type = "identifier"
        elif isinstance(values, IndexCalculation):
            values_calculation_type = "index"
        self.objectspace.informations.add(
            path,
            f"{prop}_calculation_type{identifier}",
            values_calculation_type,
        )
        self.objectspace.informations.add(
            path,
            f"{prop}_calculation{identifier}",
            values_calculation,
        )
