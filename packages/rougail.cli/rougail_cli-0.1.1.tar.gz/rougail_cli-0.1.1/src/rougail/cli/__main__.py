"""
Silique (https://www.silique.fr)
Copyright (C) 2024

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mtools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Mtools.  If not, see <http://www.gnu.org/licenses/>.
"""

from tiramisu_cmdline_parser import TiramisuCmdlineParser
from tiramisu import Config
from pathlib import Path

from rougail import Rougail, PropertiesOptionError
from rougail.config import get_rougail_config
from rougail.update import RougailUpgrade
from rougail.utils import load_modules

from .i18n import _


def _main():
    rougailconfig = get_rougail_config(
        backward_compatibility=False, add_extra_options=False
    )
    cmd_config = rougailconfig.config
    cmd_config.property.read_write()
    cmd_config.property.add("not_for_commandline")
    parser = TiramisuCmdlineParser(
        cmd_config,
        add_extra_options=False,
        short_name_max_len=2,
    )
    parser.parse_args()
    cmd_config.property.remove("not_for_commandline")
    cmd_config.property.read_only()
    if rougailconfig["upgrade"]:
        RougailUpgrade(rougailconfig=rougailconfig).run()
        return
    try:
        user_data_names = rougailconfig["step.user_data"]
    except PropertiesOptionError:
        user_data_names = []
    output_name = rougailconfig["step.output"]
    # structural
    rougail = Rougail(rougailconfig)
    for user_data_name in user_data_names:
        rougail.converted.plugins.append("user_data_" + user_data_name)
    rougail.converted.plugins.append("output_" + output_name)
    config = rougail.get_config()
    # data user
    if not user_data_names:
        user_datas = None
    else:
        config.property.read_write()
        user_datas = []
        for user_data_name in user_data_names:
            path = (
                Path(__file__).parent.parent
                / ("user_data_" + user_data_name)
                / "__init__.py"
            )
            if not path.is_file():
                raise Exception(
                    _('cannot find "user_data" module "{0}"').format(user_data_name)
                )
            module = load_modules("rougail.user_data_" + user_data_name, str(path))
            user_datas.extend(
                module.RougailUserData(
                    config,
                    rougailconfig=rougailconfig,
                ).run()
            )
    if user_datas:
        err_warn = rougail.user_datas(user_datas)
    else:
        err_warn = {"errors": [], "warnings": []}
    # output
    config.property.read_only()
    path = Path(__file__).parent.parent / ("output_" + output_name) / "__init__.py"
    if not path.is_file():
        raise Exception(
            _('cannot find cli file for "output_name" module "{0}"').format(output_name)
        )
    module = load_modules("rougail.output_" + output_name, str(path))
    module.RougailOutput(
        config=config,
        rougailconfig=rougailconfig,
        user_data_errors=err_warn["errors"],
        user_data_warnings=err_warn["warnings"],
    ).run()


def main():
    try:
        _main()
    except Exception as err:
        print(_("ERROR: {0}").format(err))
        exit(1)
