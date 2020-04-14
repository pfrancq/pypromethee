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
import abc
from enum import Enum


# ----------------------------------------------------------------------------------------------------------------------
class CriterionType(Enum):
    """
    Define the type of a criterion.

    Actually, only linear criteria are supported (to maximize or minimized)
    """
    LinearMaximize = 1
    LinearMinimize = 2


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
    criterion:
        Type of the criterion. It defines if the criterion must be maximised or minimised.
    normalized:
        Need the criterion a normalisation of its values for the different solution.
    """

    # -------------------------------------------------------------------------
    name: str
    type: CriterionType
    normalized: bool

    # -------------------------------------------------------------------------
    def __init__(self, name: str, type: CriterionType, normalized: bool):
        """
        Constructor.

        :param name: Name of the criterion.

        :param type: Type of the criterion (Maximize or Minimize).

        :param normalized: Works the criterion on normalized values?
        """

        self.name = name
        self.type = type
        self.normalized = normalized

    # -------------------------------------------------------------------------
    def apply_config(self, config: dict) -> bool:
        """
        Look in a dictionary contains some entries related to parameters.

        :param config: Configuration dictionary.
        """
        pass

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def compute_pref(self, u: float, v: float) -> float:
        """
        Compute the preference between two values of the criterion.

        :param u: Value used as reference.
        :param v: Value used to compare.
        :return: a number between [0,1] that represents if 'u' is a better criterion value that 'v'.
        """
        pass
