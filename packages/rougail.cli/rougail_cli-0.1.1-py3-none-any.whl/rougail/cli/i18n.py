"""Internationalisation utilities
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

from gettext import translation
from pathlib import Path

t = translation("rougail_cli", str(Path(__file__).parent / "locale"))

_ = t.gettext
