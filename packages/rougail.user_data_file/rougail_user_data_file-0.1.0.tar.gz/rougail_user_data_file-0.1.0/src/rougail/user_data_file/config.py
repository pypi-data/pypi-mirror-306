"""
Config file for Rougail-user-data

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


def get_rougail_config(
    *,
    backward_compatibility=True,
) -> dict:
    options = """
file:
  description: Configuration rougail-user-data-file
  disabled:
    type: jinja
    jinja: |
      {% if 'file' not in step.user_data %}
      disabled
      {% endif %}
  filename:
    description: Filename with user data
    alternative_name: ff
    type: unix_filename
    multi: true
    params:
       allow_relative: True
       test_existence: True
       types:
         - file
"""
    return {
        "name": "file",
        "process": "user data",
        "options": options,
        "level": 50,
    }


__all__ = "get_rougail_config"
