# ----------------------------------------------------------------------------------------------------------------------
#
# PROMETHEE multi-criterai decision method
#
# Copyright 2000-2018 by Pascal Francq (pascal@francq.info).
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library, as a file COPYING.LIB; if not, write
# to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
class Criterion:
    """
    This is an abstract class that represents a generic criterion that must maximize or minimize. Moreover, a criterion
    can work a normalized values of the original values.

    Inheriting classes must override the 'compute_pref' method.

    |

    The instance attributes are:

    name:
        Name of the criterion.

    type:
        Type of the criterion. It defines if the criterion must be maximised or minimised.

    normalized:
        Need the criterion a normalisation of its values for the different solution.
    """

    # -------------------------------------------------------------------------
    Maximize: int = 1
    Minimize: int = 2

    # -------------------------------------------------------------------------
    def __init__(self, name: str, type: int, normalized: bool):
        """
        Constructor.

        :param name: Name of the criterion.

        :param type: Type of the criterion (Maximize or Minimize).

        :param normalized: Works the criterion on normalized values?
        """

        self.name = name
        if (type != self.Minimize) and (type != self.Maximize):
            raise ValueError("Only 'Maximize' and 'Minimize' are allowed.")
        self.type=type
        self.normalized = normalized

    # -------------------------------------------------------------------------
    # @abc.abstractmethod
    def compute_pref(self, u: float, v: float) -> float: pass
