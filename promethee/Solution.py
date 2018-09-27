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
from typing import List
from promethee.KernelCriterion import CriterionSolutionValue


# ----------------------------------------------------------------------------------------------------------------------
class Solution:
    """
    This class represents a solution defined by a set of values for the different criteria.

        |

    The instance attributes are:

    id:
        Identifier of the solution.

    fi:
        The global Φ for the solution.

    fi_plus:
        The positive Φ for the solution.

    fi_minus:
        The negative Φ for the solution.

    values:
        Values for the solution for the different criteria.
    """

    # -------------------------------------------------------------------------
    id: int
    fi: float
    fi_plus: float
    fi_minus: float
    values: List[CriterionSolutionValue]

    # -------------------------------------------------------------------------
    def __init__(self, id: int):
        """
        Constructor.

        :param id: Identifier of the solution.
        """

        self.id = id
        self.fi = 0.0
        self.fi_plus = 0.0
        self.fi_minus = 0.0
        self.values = []
