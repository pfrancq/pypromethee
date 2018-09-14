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
from numpy import ndarray



# ----------------------------------------------------------------------------------------------------------------------
class CriterionType:
    """
    This is an abstract class that represents a generic criterion type that must maximize or minimize.

    Inheriting classes must override the 'compute_pref' method.
    """


    # -------------------------------------------------------------------------
    Maximize: int = 1
    Minimize: int = 2


    # -------------------------------------------------------------------------
    def __init__(self, name: str, type: int):
        """
        Constructor.

        :param name: Name of the criterion.
        :param type: Type of the criterion (Maximize or Minimize).
        """
        self.name = name
        if (type != self.Minimize) and (type != self.Maximize):
            raise ValueError("Only 'Maximize' and 'Minimize' are allowed.")
        self.type=type


    # -------------------------------------------------------------------------
    # @abc.abstractmethod
    def compute_pref(self, u: float, v: float) -> float: pass




# ----------------------------------------------------------------------------------------------------------------------
class LinearCriterion(CriterionType):
    """
    The criterion type class implements the classic linear method. It is defined by two parameters 'p' and 'q':

    - When two solutions have a relative difference less than 'q', they are supposed of equally preferable.
    - When two solutions have a relative difference greater than 'p', one must always be preferred.
    - Else, the preference between two solutions varies linearly with their relative difference.
    """


    # -------------------------------------------------------------------------
    def __init__(self, name: str, type: int, p: float, q: float):
        """
        Constructor.

        :param name: Name of the criterion.
        :param type: Type of the criterion (Maximize or Minimize).
        :param p: Value of the 'p' parameter.
        :param q: Value of the 'q' parameter.
        """
        CriterionType.__init__(self, name, type)
        self.p = p
        self.q = q


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
            if self.type == CriterionType.Maximize:
                if u > v:
                    return 1.0
                else:
                    return 0.0
            else: # self.type == PromCriterionType.Minimize
                if u < v:
                    return 1.0
                else:
                    return 0.0

        # Between q and p -> Compute the preference.
        if self.type == CriterionType.Maximize:
            if u > v:
                return (d - self.q) / (self.p - self.q)
            else:
                return 0
        else: # self.type == PromCriterionType.Minimize
            if u < v:
                return (d - self.q) / (self.p - self.q);
            else:
                return 0.0




# ----------------------------------------------------------------------------------------------------------------------
class CriterionSolutionValue:
    """
    This class represents the value of a solution for a given criterion. It also encapsulates a set of computed values.
    Each instance is referred by the corresponding solution and criterion instances.
    """


    # -------------------------------------------------------------------------
    fi: float
    fi_plus: float
    fi_minus: float
    normalized: float
    value: float


    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Constructor.
        """
        self.fi = 0.0
        self.fi_plus = 0.0
        self.fi_minus = 0.0
        self.value = 0.0
        self.normalized = 0.0




# ----------------------------------------------------------------------------------------------------------------------
class Criterion:
    """
    This class represents a given criterion defined by a type and a set of values for each solutions.
    """


    # -------------------------------------------------------------------------
    type: CriterionType


    # -------------------------------------------------------------------------
    def __init__(self, id: int, nb_solutions: int):
        """
        Constructor.

        :param id: Identifier of the criterion.
        :param nb_solutions: Number of solutions.
        """
        self.id = id
        self.type = None
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
                self.values[i].normalized = (self.values[i].value - min) / diff


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
                val1.fi_plus += self.type.compute_pref(val1.normalized, val2.normalized)
                val1.fi_minus += self.type.compute_pref(val2.normalized, val1.normalized)

        for val in self.values:
            val.fi = val.fi_plus - val.fi_minus




# ----------------------------------------------------------------------------------------------------------------------
class Solution:
    """
    This class represents a solution defined by a set of values for the different criteria.
    """


    # -------------------------------------------------------------------------
    fi: float


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




# ----------------------------------------------------------------------------------------------------------------------
class Kernel:
    """
    This class represents a PROMETHEE kernel. It manages a set of solutions and criteria, their values and the overall
    process. The solutions and the criteria are defined by a specific set of identifiers that start with 0 and are
    consecutive.

    In practice, to be used, the following steps must be done:

    - Create a new kernel while specifying the number of solutions and criteria.
    - For each criterion, use the 'set_criterion' method to set its type by using the corresponding identifier.
    - Call the rank method with a matrix (solutions,criteria) containing the values of the solutions for each criteria.
    - Use the 'Kernel.ordered_solutions' to obtain the identifiers of the ranked solutions.

    Internally, since all solutions have an identifier in [0, nb_solutions-1], you may needed a correspondence table.
    Let's suppose you have a list of 5 users with identifiers 1, 5, 10, 150, and 120. You can manage that:

    ...

    users_solutions = [1, 5, 10, 150, 120] # Correspondence table
    for solution in kernel.ordered_solutions:
        print("User identifier: " + str(users_solutions[solution]))
    """


    # -------------------------------------------------------------------------
    def __init__(self, nb_criteria: int, nb_solutions: int):
        """
        Constructor.

        :param nb_criteria: Number of criteria.
        :param nb_solutions: Number of solution.
        """

        self.matrix = None
        self.nb_criteria = nb_criteria
        self.nb_solutions = nb_solutions
        self.ordered_solutions = []

        # Solutions
        self.solutions = []
        for sol_id in range(0, self.nb_solutions):
            self.solutions.append(Solution(sol_id))

        # Criteria
        self.criteria = []
        for criterion_id in range(0, self.nb_criteria):
            criterion = Criterion(criterion_id, self.nb_solutions)
            self.criteria.append(criterion)
            for (solution, value) in zip(self.solutions, criterion.values):
                solution.values.append(value)


    # -------------------------------------------------------------------------
    def _assign_values(self, matrix: ndarray) -> None:
        """
        Assign the values to the different internal variables of the kernel.

        :param matrix: The matrix (solutions,criteria) containing the values of the solutions for each criteria.
        :return: nothing
        """
        for criterion in self.criteria:
            for solution_id in range(0, self.nb_solutions):
                criterion.values[solution_id].value = matrix[solution_id, criterion.id]


    # -------------------------------------------------------------------------
    def set_criterion(self, id: int, weight: float, type: CriterionType) -> None:
        """
        Assign a type and a weigth to a given criterion.

        :param id: Identifier of the criterion.
        :param weight: Weight of the criterion.
        :param type: Type of the criterion (must be an inheriting class of 'CriterionType').
        :return: nothing
        """
        self.criteria[id].type = type
        self.criteria[id].weight = weight


    # -------------------------------------------------------------------------
    def rank(self, matrix: ndarray) -> None:
        """
        Rank the solutions and store the results in 'Kernel.ordered_solutions'.

        :param matrix: The matrix (solutions,criteria) containing the values of the solutions for each criteria.
        :return: nothing
        """

        self._assign_values(matrix)

        # Compute fi for each criterion
        total_weight = 0.0
        for criterion in self.criteria:
            criterion.normalize()
            criterion.compute_fis(self)
            total_weight += criterion.weight

        # Compute the flow for each solution
        for solution in self.solutions:
            solution.fi_minus = solution.fi_plus = 0.0
            for val in solution.values:
                solution.fi_plus += val.fi_plus
                solution.fi_minus += val.fi_minus
            solution.fi_plus /= total_weight * (len(self.solutions) - 1)
            solution.fi_minus /= total_weight * (len(self.solutions) - 1)
            solution.fi = solution.fi_plus - solution.fi_minus

        # Rank the solutions by fitness
        self.ordered_solutions = self.solutions
        self.ordered_solutions.sort(reverse=True, key=lambda solution: solution.fi)
