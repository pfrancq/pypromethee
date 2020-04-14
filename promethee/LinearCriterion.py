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
from promethee.Criterion import Criterion, CriterionType


# ----------------------------------------------------------------------------------------------------------------------
class LinearCriterion(Criterion):
    """
    The criterion criterion class implements the classic linear method. It is defined by two parameters 'p' and 'q':

    - When two solutions have a relative difference less than 'q', they are supposed of equally preferable.
    - When two solutions have a relative difference greater than 'p', one must always be preferred.
    - Else, the preference between two solutions varies linearly with their relative difference.

    |

    The instance attributes are:

    p:
        P parameter.
    q:
        Q parameter.
    """

    # -------------------------------------------------------------------------
    def __init__(self, name: str, type: CriterionType, p: float = 0.1, q: float = 0.05):
        """
        Constructor.

        :param name: Name of the criterion.
        :param type: Type of the criterion (Maximize or Minimize).
        :param p: Value of the 'p' parameter.
        :param q: Value of the 'q' parameter.
        """

        Criterion.__init__(self, name=name, type=type, normalized=True)
        self.p = p
        self.q = q

    # -------------------------------------------------------------------------
    def apply_config(self, config: dict) -> bool:
        """
        Look in a dictionary contains some entries related to parameters.

        :param config: Configuration dictionary.
        """
        Criterion.apply_config(self=self, config=config)
        if "p" in config:
            self.p = float(config["p"])
        if "q" in config:
            self.q = float(config["q"])

    # -------------------------------------------------------------------------
    def compute_pref(self, u: float, v: float) -> float:
        """
        Compute the preference between two values of the criterion.

        :param u: Value used as reference.
        :param v: Value used to compare.
        :return: a number between [0,1] that represents if 'u' is a better criterion value that 'v'.
        """

        d = abs(u-v)

        # No solution is better
        if d <= self.q:
            return 0.0

        # One solution is better than the other one
        if d >= self.p:
            if self.type == CriterionType.LinearMaximize:
                if u > v:
                    return 1.0
                else:
                    return 0.0
            else:  # self.criterion == CriterionType.LinearMinimize
                if u < v:
                    return 1.0
                else:
                    return 0.0

        # Between q and p -> Compute the preference.
        if self.type == CriterionType.LinearMaximize:
            if u > v:
                return (d - self.q) / (self.p - self.q)
            else:
                return 0.0
        else:  # self.criterion == CriterionType.LinearMinimize
            if u < v:
                return (d - self.q) / (self.p - self.q)
            else:
                return 0.0
