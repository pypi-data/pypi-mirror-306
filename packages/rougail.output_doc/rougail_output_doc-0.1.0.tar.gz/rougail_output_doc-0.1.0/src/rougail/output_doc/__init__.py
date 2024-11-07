#!/usr/bin/env python3
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
# FIXME si plusieurs example dont le 1er est none tester les autres : tests/dictionaries/00_8test_none
from tiramisu import Calculation
from tiramisu.error import display_list
import tabulate as tabulate_module
from tabulate import tabulate
from warnings import warn
from typing import Optional

from rougail.error import display_xmlfiles
from rougail import RougailConfig, Rougail, CONVERT_OPTION
from rougail.object_model import PROPERTY_ATTRIBUTE

from .config import OutPuts
from .i18n import _

ENTER = "\n\n"


DocTypes = {
    "domainname": {
        "params": {
            "allow_startswith_dot": _("the domain name can starts by a dot"),
            "allow_without_dot": _("the domain name can be a hostname"),
            "allow_ip": _("the domain name can be an IP"),
            "allow_cidr_network": _("the domain name can be network in CIDR format"),
        },
    },
    "number": {
        "params": {
            "min_number": _("the minimum value is {0}"),
            "max_number": _("the maximum value is {0}"),
        },
    },
    "ip": {
        "msg": "IP",
        "params": {
            "cidr": _("IP must be in CIDR format"),
            "private_only": _("private IP are allowed"),
            "allow_reserved": _("reserved IP are allowed"),
        },
    },
    "hostname": {
        "params": {
            "allow_ip": _("the host name can be an IP"),
        },
    },
    "web_address": {
        "params": {
            "allow_ip": _("the domain name in web address can be an IP"),
            "allow_without_dot": _(
                "the domain name in web address can be only a hostname"
            ),
        },
    },
    "port": {
        "params": {
            "allow_range": _("can be range of port"),
            "allow_protocol": _("can have the protocol"),
            "allow_zero": _("port 0 is allowed"),
            "allow_wellknown": _("ports 1 to 1023 are allowed"),
            "allow_registred": _("ports 1024 to 49151 are allowed"),
            "allow_private": _("ports greater than 49152 are allowed"),
        },
    },
}


ROUGAIL_VARIABLE_TYPE = (
    "https://rougail.readthedocs.io/en/latest/variable.html#variables-types"
)


class RougailOutputDoc:
    def __init__(
        self,
        *,
        config: "Config" = None,
        rougailconfig: RougailConfig = None,
        **kwarg,
    ):
        if rougailconfig is None:
            rougailconfig = RougailConfig
            if rougailconfig["step.output"] != "doc":
                rougailconfig["step.output"] = "doc"
        if rougailconfig["step.output"] != "doc":
            raise Exception("doc is not set as step.output")
        self.rougailconfig = rougailconfig
        outputs = OutPuts().get()
        output = self.rougailconfig["doc.output_format"]
        if output not in outputs:
            raise Exception(
                f'cannot find output "{output}", available outputs: {list(outputs)}'
            )
        if config is None:
            rougail = Rougail(self.rougailconfig)
            rougail.converted.plugins.append("output_doc")
            config = rougail.get_config()
        self.conf = config
        self.conf.property.setdefault(frozenset({"advanced"}), "read_write", "append")
        self.conf.property.read_write()
        self.conf.property.remove("cache")
        self.dynamic_paths = {}
        self.formater = outputs[output]()
        self.level = self.rougailconfig["doc.title_level"]
        # self.property_to_string = [('mandatory', 'obligatoire'), ('hidden', 'cachée'), ('disabled', 'désactivée'), ('unique', 'unique'), ('force_store_value', 'modifié automatiquement')]
        self.property_to_string = [
            ("mandatory", _("mandatory")),
            ("hidden", _("hidden")),
            ("disabled", _("disabled")),
            ("unique", _("unique")),
            ("force_store_value", _("auto modified")),
        ]

    def run(self):
        print(self.gen_doc())

    def gen_doc(self):
        tabulate_module.PRESERVE_WHITESPACE = True
        examples_mini = {}
        examples_all = {}
        return_string = self.formater.header()
        if self.rougailconfig["main_namespace"]:
            for namespace in self.conf.unrestraint.list():
                name = namespace.name()
                examples_mini[name] = {}
                examples_all[name] = {}
                doc = (
                    self._display_doc(
                        self.display_families(
                            namespace,
                            self.level + 1,
                            examples_mini[name],
                            examples_all[name],
                        ),
                        [],
                    )
                    + "\n"
                )
                if not examples_mini[name]:
                    del examples_mini[name]
                if not examples_all[name]:
                    del examples_all[name]
                else:
                    return_string += self.formater.title(
                        _('Variables for "{0}"').format(namespace.name()), self.level
                    )
                    return_string += doc
        else:
            doc = (
                self._display_doc(
                    self.display_families(
                        self.conf.unrestraint,
                        self.level + 1,
                        examples_mini,
                        examples_all,
                    ),
                    [],
                )
                + "\n"
            )
            if examples_all:
                return_string += self.formater.title(_("Variables"), self.level)
                return_string += doc
        if not examples_all:
            return ""
        if self.rougailconfig["doc.with_example"]:
            if examples_mini:
                return_string += self.formater.title(
                    _("Example with mandatory variables not filled in"), self.level
                )
                return_string += self.formater.yaml(examples_mini)
            if examples_all:
                return_string += self.formater.title(
                    "Example with all variables modifiable", self.level
                )
                return_string += self.formater.yaml(examples_all)
        return return_string

    def _display_doc(self, variables, add_paths):
        return_string = ""
        for variable in variables:
            typ = variable["type"]
            path = variable["path"]
            if path in add_paths:
                continue
            if typ == "family":
                return_string += variable["title"]
                return_string += self._display_doc(variable["objects"], add_paths)
            else:
                for idx, path in enumerate(variable["paths"]):
                    if path in self.dynamic_paths:
                        paths_msg = display_list(
                            [
                                self.formater.bold(path_)
                                for path_ in self.dynamic_paths[path]["paths"]
                            ],
                            separator="or",
                        )
                        variable["objects"][idx][0] = variable["objects"][idx][
                            0
                        ].replace("{{ ROUGAIL_PATH }}", paths_msg)
                        identifiers = self.dynamic_paths[path]["identifiers"]
                        description = variable["objects"][idx][1][0]
                        if "{{ identifier }}" in description:
                            if description.endswith("."):
                                description = description[:-1]
                            comment_msg = self.to_phrase(
                                display_list(
                                    [
                                        description.replace(
                                            "{{ identifier }}",
                                            self.formater.italic(identifier),
                                        )
                                        for identifier in identifiers
                                    ],
                                    separator="or",
                                    add_quote=True,
                                )
                            )
                            variable["objects"][idx][1][0] = comment_msg
                    variable["objects"][idx][1] = self.formater.join(
                        variable["objects"][idx][1]
                    )
                return_string += (
                    self.formater.table(
                        tabulate(
                            variable["objects"],
                            headers=self.formater.table_header(
                                ["Variable", "Description"]
                            ),
                            tablefmt=self.formater.name,
                        )
                    )
                    + "\n\n"
                )
            add_paths.append(path)
        return return_string

    def is_hidden(self, child):
        properties = child.property.get(uncalculated=True)
        for hidden_property in ["hidden", "disabled", "advanced"]:
            if hidden_property in properties:
                return True
        return False

    def display_families(
        self,
        family,
        level,
        examples_mini,
        examples_all,
    ):
        variables = []
        for child in family.list():
            if self.is_hidden(child):
                continue
            if not child.isoptiondescription():
                if child.isfollower() and child.index() != 0:
                    # only add to example
                    self.display_variable(
                        child,
                        examples_mini,
                        examples_all,
                    )
                    continue
                path = child.path(uncalculated=True)
                if child.isdynamic():
                    self.dynamic_paths.setdefault(
                        path, {"paths": [], "identifiers": []}
                    )["paths"].append(child.path())
                    self.dynamic_paths[path]["identifiers"].append(
                        child.identifiers()[-1]
                    )
                if not variables or variables[-1]["type"] != "variables":
                    variables.append(
                        {
                            "type": "variables",
                            "objects": [],
                            "path": path,
                            "paths": [],
                        }
                    )
                variables[-1]["objects"].append(
                    self.display_variable(
                        child,
                        examples_mini,
                        examples_all,
                    )
                )
                variables[-1]["paths"].append(path)
            else:
                name = child.name()
                if child.isleadership():
                    examples_mini[name] = []
                    examples_all[name] = []
                else:
                    examples_mini[name] = {}
                    examples_all[name] = {}
                variables.append(
                    {
                        "type": "family",
                        "title": self.display_family(
                            child,
                            level,
                        ),
                        "path": child.path(uncalculated=True),
                        "objects": self.display_families(
                            child,
                            level + 1,
                            examples_mini[name],
                            examples_all[name],
                        ),
                    }
                )
                if not examples_mini[name]:
                    del examples_mini[name]
                if not examples_all[name]:
                    del examples_all[name]
        return variables

    def display_family(
        self,
        family,
        level,
    ):
        if family.name() != family.description(uncalculated=True):
            title = f"{family.description(uncalculated=True)}"
        else:
            warning = f'No attribute "description" for family "{family.path()}" in {display_xmlfiles(family.information.get("dictionaries"))}'
            warn(warning)
            title = f"{family.path()}"
        isdynamic = family.isdynamic(only_self=True)
        if isdynamic:
            identifiers = family.identifiers(only_self=True)
            if "{{ identifier }}" in title:
                title = display_list(
                    [
                        title.replace(
                            "{{ identifier }}", self.formater.italic(identifier)
                        )
                        for identifier in identifiers
                    ],
                    separator="or",
                    add_quote=True,
                )
        msg = self.formater.title(title, level)
        subparameter = []
        self.manage_properties(family, subparameter)
        if subparameter:
            msg += self.subparameter_to_string(subparameter) + ENTER
        comment = []
        self.subparameter_to_parameter(subparameter, comment)
        if comment:
            msg += "\n".join(comment) + ENTER
        help = self.to_phrase(family.information.get("help", ""))
        if help:
            msg += "\n" + help + ENTER
        if family.isleadership():
            # help = "Cette famille contient des listes de bloc de variables."
            help = "This family contains lists of variable blocks."
            msg += "\n" + help + ENTER
        if isdynamic:
            identifiers = family.identifiers(only_self=True, uncalculated=True)
            if isinstance(identifiers, Calculation):
                identifiers = self.to_string(family, "dynamic")
            if isinstance(identifiers, list):
                for idx, val in enumerate(identifiers):
                    if not isinstance(val, Calculation):
                        continue
                    identifiers[idx] = self.to_string(family, "dynamic", f"_{idx}")
                identifiers = self.formater.list(identifiers)
            # help = f"Cette famille construit des familles dynamiquement.\n\n{self.formater.bold('Identifiers')}: {identifiers}"
            help = f"This family builds families dynamically.\n\n{self.formater.bold('Identifiers')}: {identifiers}"
            msg += "\n" + help + ENTER
        return msg

    def manage_properties(
        self,
        variable,
        subparameter,
    ):
        properties = variable.property.get(uncalculated=True)
        for mode in self.rougailconfig["modes_level"]:
            if mode in properties:
                subparameter.append((self.formater.prop(mode), None, None))
                break
        for prop, msg in self.property_to_string:
            if prop in properties:
                subparameter.append((self.formater.prop(msg), None, None))
            elif variable.information.get(f"{prop}_calculation", False):
                subparameter.append(
                    (self.formater.prop(msg), msg, self.to_string(variable, prop))
                )

    def subparameter_to_string(
        self,
        subparameter,
    ):
        subparameter_str = ""
        for param in subparameter:
            if param[1]:
                subparameter_str += f"_{param[0]}_ "
            else:
                subparameter_str += f"{param[0]} "
        return subparameter_str[:-1]

    def subparameter_to_parameter(
        self,
        subparameter,
        comment,
    ):
        for param in subparameter:
            if not param[1]:
                continue
            msg = param[2]
            comment.append(f"{self.formater.bold(param[1].capitalize())}: {msg}")

    def to_phrase(self, msg):
        if not msg:
            return ""
        msg = str(msg).strip()
        if not msg.endswith("."):
            msg += "."
        return msg[0].upper() + msg[1:]

    def display_variable(
        self,
        variable,
        examples_mini,
        examples_all,
    ):
        if variable.isdynamic():
            parameter = ["{{ ROUGAIL_PATH }}"]
        else:
            parameter = [f"{self.formater.bold(variable.path())}"]
        subparameter = []
        description = variable.description(uncalculated=True)
        comment = [self.to_phrase(description)]
        help_ = self.to_phrase(variable.information.get("help", ""))
        if help_:
            comment.append(help_)
        self.type_to_string(
            variable,
            subparameter,
            comment,
        )
        self.manage_properties(
            variable,
            subparameter,
        )
        if variable.ismulti():
            multi = not variable.isfollower() or variable.issubmulti()
        else:
            multi = False
        if multi:
            subparameter.append((self.formater.prop("multiple"), None, None))
        if subparameter:
            parameter.append(self.subparameter_to_string(subparameter))
        if variable.name() == description:
            warning = f'No attribute "description" for variable "{variable.path()}" in {display_xmlfiles(variable.information.get("dictionaries"))}'
            warn(warning)
        default = self.get_default(
            variable,
            comment,
        )
        default_in_choices = False
        if variable.information.get("type") == "choice":
            choices = variable.value.list(uncalculated=True)
            if isinstance(choices, Calculation):
                choices = self.to_string(variable, "choice")
            if isinstance(choices, list):
                for idx, val in enumerate(choices):
                    if not isinstance(val, Calculation):
                        if default is not None and val == default:
                            choices[idx] = str(val) + " ← " + _("(default)")
                            default_in_choices = True
                        continue
                    choices[idx] = self.to_string(variable, "choice", f"_{idx}")
                choices = self.formater.list(choices)
            comment.append(f'{self.formater.bold(_("Choices"))}: {choices}')
            # choice
        if default is not None and not default_in_choices:
            comment.append(f"{self.formater.bold(_('Default'))}: {default}")
        self.manage_exemples(
            multi,
            variable,
            examples_all,
            examples_mini,
            comment,
        )
        self.subparameter_to_parameter(subparameter, comment)
        self.formater.columns(parameter, comment)
        return [self.formater.join(parameter), comment]

    def get_default(
        self,
        variable,
        comment,
    ):
        if variable.information.get("fake_default", False):
            default = None
        else:
            default = variable.value.get(uncalculated=True)
        if default in [None, []]:
            return
        if isinstance(default, Calculation):
            default = self.to_string(variable, "default")
        if isinstance(default, list):
            for idx, val in enumerate(default):
                if not isinstance(val, Calculation):
                    continue
                default[idx] = self.to_string(variable, "default", f"_{idx}")
            default = self.formater.list(default)
        return default

    def to_string(
        self,
        variable,
        prop,
        identifier="",
    ):
        calculation_type = variable.information.get(
            f"{prop}_calculation_type{identifier}", None
        )
        if not calculation_type:
            raise Exception(
                f"cannot find {prop}_calculation_type{identifier} information, do you have declare doc has a plugins?"
            )
        calculation = variable.information.get(f"{prop}_calculation{identifier}")
        if calculation_type == "jinja":
            if calculation is not True:
                values = self.formater.to_string(calculation)
            else:
                values = "depends on a calculation"
                warning = f'"{prop}" is a calculation for {variable.path()} but has no description in {display_xmlfiles(variable.information.get("dictionaries"))}'
                warn(warning)
        elif calculation_type == "variable":
            if prop in PROPERTY_ATTRIBUTE:
                values = self.formater.to_string(calculation)
            else:
                values = _('the value of the variable "{0}"').format(calculation)
        elif calculation_type == "identifier":
            if prop in PROPERTY_ATTRIBUTE:
                values = self.formater.to_string(calculation)
            else:
                values = _("value of the {0}").format(calculation_type)
        else:
            values = _("value of the {0}").format(calculation_type)
        if not values.endswith("."):
            values += "."
        return values

    def type_to_string(
        self,
        variable,
        subparameter,
        comment,
    ):
        variable_type = variable.information.get("type")
        doc_type = DocTypes.get(variable_type, {"params": {}})
        subparameter.append(
            (
                self.formater.link(
                    doc_type.get("msg", variable_type), ROUGAIL_VARIABLE_TYPE
                ),
                None,
            )
        )
        option = variable.get()
        validators = []
        for param, msg in doc_type["params"].items():
            value = option.impl_get_extra(f"_{param}")
            if value is None:
                value = option.impl_get_extra(param)
            if value is not None and value is not False:
                validators.append(msg.format(value))
        valids = [
            name
            for name in variable.information.list()
            if name.startswith("validators_calculation_type_")
        ]
        if valids:
            for idx in range(len(valids)):
                validators.append(
                    self.to_string(
                        variable,
                        "validators",
                        f"_{idx}",
                    )
                )
        if validators:
            if len(validators) == 1:
                comment.append(f'{self.formater.bold("Validator")}: ' + validators[0])
            else:
                comment.append(
                    f'{self.formater.bold("Validators")}:'
                    + self.formater.list(validators)
                )

    def manage_exemples(
        self,
        multi,
        variable,
        examples_all,
        examples_mini,
        comment,
    ):
        example_mini = None
        example_all = None
        example = variable.information.get("examples", None)
        if example is None:
            example = variable.information.get("test", None)
        default = variable.value.get()
        if isinstance(example, tuple):
            example = list(example)
        mandatory = "mandatory" in variable.property.get(uncalculated=True)
        if example:
            if not multi:
                example = example[0]
                title = _("Example")
                if mandatory:
                    example_mini = example
                example_all = example
            else:
                if mandatory:
                    example_mini = "\n - example"
                example_all = example
                len_test = len(example)
                example = self.formater.list(example)
                if len_test > 1:
                    title = _("Examples")
                else:
                    title = _("Example")
            comment.append(f"{self.formater.bold(title)}: {example}")
        elif default not in [None, []]:
            example_all = default
        else:
            example = CONVERT_OPTION.get(variable.information.get("type"), {}).get(
                "example", None
            )
            if example is None:
                example = "xxx"
            if multi:
                example = [example]
            if mandatory:
                example_mini = example
            example_all = example
        if variable.isleader():
            if example_mini is not None:
                for mini in example_mini:
                    examples_mini.append({variable.name(): mini})
            if example_all is not None:
                for mall in example_all:
                    examples_all.append({variable.name(): mall})
        elif variable.isfollower():
            if example_mini is not None:
                for idx in range(0, len(examples_mini)):
                    examples_mini[idx][variable.name()] = example_mini
            if example_all is not None:
                for idx in range(0, len(examples_all)):
                    examples_all[idx][variable.name()] = example_all
        else:
            if example_mini is not None:
                examples_mini[variable.name()] = example_mini
            examples_all[variable.name()] = example_all


RougailOutput = RougailOutputDoc
__all__ = ("RougailOutputDoc",)
