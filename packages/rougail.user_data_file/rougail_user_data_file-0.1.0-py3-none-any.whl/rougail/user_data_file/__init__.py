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

from rougail import RougailConfig
from ruamel.yaml import YAML
from tiramisu.error import ValueOptionError, PropertiesOptionError, LeadershipError

from .i18n import _


class RougailUserDataFile:
    def __init__(
        self,
        config,
        *,
        rougailconfig=None,
    ) -> None:
        if rougailconfig is None:
            rougailconfig = RougailConfig
            user_data = rougailconfig["step.user_data"]
            if "file" not in user_data:
                user_data.append("file")
                rougailconfig["step.user_data"] = user_data
        user_data = rougailconfig["step.user_data"]
        if "file" not in user_data:
            raise Exception(_("file is not set in step.user_data"))
        self.rougailconfig = rougailconfig
        self.filenames = self.rougailconfig["file.filename"]
        self.yaml = YAML()
        self.config = config
        self.errors = []
        self.warnings = []

    def run(
        self,
    ) -> None:
        user_datas = []
        for filename in self.filenames:
            with open(filename) as fh_config:
                file_values = self.yaml.load(fh_config)
            if not file_values:
                continue
            if not isinstance(file_values, dict):
                self.errors.append(
                    _(
                        'cannot load "{0}", the root value is not a dict but "{1}"'
                    ).format(filename, file_values)
                )
                continue
            values = {}
            self.parse(
                values,
                "",
                file_values,
                filename,
            )
            user_datas.append(
                {
                    "source": _("file ({0})").format(filename),
                    "errors": self.errors,
                    "warnings": self.warnings,
                    "values": values,
                }
            )
        return user_datas

    def parse(
        self,
        values: dict,
        parent_path: str,
        file_values: dict,
        filename: str,
    ):
        for key, value in file_values.items():
            path = parent_path + key
            if isinstance(value, dict):
                self.parse(values, path + ".", value, filename)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # it's a leadership
                keys = set()
                for val in value:
                    if not isinstance(val, dict):
                        self.errors.append(
                            _('"{0}" in {1} has an unknown value').format(
                                path, filename
                            )
                        )
                        break
                    keys |= set(val)
                else:
                    for val in value:
                        for key in keys:
                            values.setdefault(path + "." + key, []).append(
                                val.get(key, None)
                            )

            else:
                values[path] = value


RougailUserData = RougailUserDataFile


__all__ = ("RougailUserDataFile",)
