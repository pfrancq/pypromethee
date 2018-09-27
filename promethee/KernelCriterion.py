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
from promethee.Criterion import Criterion


# ----------------------------------------------------------------------------------------------------------------------
class CriterionSolutionValue:
    """
    This class represents the value of a solution for a given criterion. It also encapsulates a set of computed values.
    Each instance is referred by the corresponding solution and criterion instances.


    |

    The instance attributes are:

    fi:
        The global Φ for the pair (criterion, solution).

    fi_plus:
        The positive Φ for the pair (criterion, solution).

    fi_minus:
        The negative Φ for the pair (criterion, solution).

    value:
        Value for the pair (criterion, solution).

    used_value:
        Value for the pair (criterion, solution) used for the computation (so eventually normalised).
    """

    # -------------------------------------------------------------------------
    fi: float
    fi_plus: float
    fi_minus: float
    value: float
    used_value: float

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Constructor.
        """

        self.fi = 0.0
        self.fi_plus = 0.0
        self.fi_minus = 0.0
        self.value = 0.0
        self.used_value = 0.0


# ----------------------------------------------------------------------------------------------------------------------
class KernelCriterion:
    """
    This class represents a given criterion defined by a type and a set of values for each solutions.

    |

    The instance attributes are:

    id:
        Identifier of the criterion.

    criterion:
        Criterion used.

    weight:
        Weight of the criterion.

    nb_solutions:
        Number of solutions.

    values:
        Values for the criterion for the different solutions.
    """

    # -------------------------------------------------------------------------
    id: int
    criterion: Criterion
    weight: float
    nb_solutions: int
    values: List[CriterionSolutionValue]

    # -------------------------------------------------------------------------
    def __init__(self, id: int, nb_solutions: int):
        """
        Constructor.

        :param id: Identifier of the criterion.

        :param nb_solutions: Number of solutions.
        """

        self.id = id
        self.criterion = None
        self.weight = 0.0
        self.nb_solutions = nb_solutions
        self.values = []
        for _ in range(0, nb_solutions):
            self.values.append(CriterionSolutionValue())

    # -------------------------------------------------------------------------
    def normalize(self) -> None:
        """
        This method normalize all values of the criterion to the domain [0,1].

        :return: nothing.
        """

        if self.criterion.normalized:
            # Compute minimum and maximum values
            min = max = self.values[0].value
            for i in range(1, self.nb_solutions):
                if max < self.values[i].value:
                    max = self.values[i].value
                if min > self.values[i].value:
                    min = self.values[i].value
            diff = max - min

            # Normalize
            if diff != 0.0:
                for i in range(0, self.nb_solutions):
                    self.values[i].used_value = (self.values[i].value - min) / diff
            else:
                # All values identical -> Set them to 1.0
                for i in range(0, self.nb_solutions):
                    self.values[i].used_value = 1.0
        else:
            # No normalization -> Simply copy 'original_value' in 'value'.
            for i in range(0, self.nb_solutions):
                self.values[i].used_value = self.values[i].value

    # -------------------------------------------------------------------------
    def compute_fis(self, kernel) -> None:
        """
        Compute the different Φ (plus, minus and balance) of the criterion.

        :param kernel: PROMETHEE kernel to which the criterion belong.
        :return: nothing.
        """

        for (sol1, val1) in zip(kernel.solutions, self.values):
            val1.fi_plus = val1.fit_minus = 0.0
            for (sol2, val2) in zip(kernel.solutions, self.values):
                if sol1.id == sol2.id:
                    continue
                val1.fi_plus += self.criterion.compute_pref(val1.used_value, val2.used_value)
                val1.fi_minus += self.criterion.compute_pref(val2.used_value, val1.used_value)

        for val in self.values:
            val.fi = val.fi_plus - val.fi_minus
