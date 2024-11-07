# Copyright (C) 2018-2019 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Union, List, Dict, Tuple, Optional, Any

try:
    from .api import TiramisuCmdlineParser
except ImportError as err:
    import warnings

    warnings.warn("cannot not import TiramisuCmdlineParser {err}", ImportWarning)
    TiramisuCmdlineParser = None

__version__ = "0.5"
__all__ = ("TiramisuCmdlineParser",)
