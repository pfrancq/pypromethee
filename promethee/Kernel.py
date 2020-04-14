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
from promethee.Criterion import Criterion, CriterionType
from promethee.Solution import Solution
from promethee.KernelCriterion import KernelCriterion


# ----------------------------------------------------------------------------------------------------------------------
class Kernel:
    """
    This class represents a PROMETHEE kernel. It manages a set of solutions and criteria, their values and the overall
    process. The solutions and the criteria are defined by a specific set of identifiers that start with 0 and are
    consecutive.

    In practice, to be used, the following steps must be done:

    - Create a new kernel while specifying the number of solutions and criteria.
    - For each criterion, use the 'set_criterion' method to set its criterion by using the corresponding identifier.
    - Call the rank method with a matrix (solutions,criteria) containing the values of the solutions for each criteria.
    - Use the 'Kernel.ordered_solutions' to obtain the identifiers of the ranked solutions.

    Internally, since all solutions have an identifier in [0, nb_solutions-1], you may needed a correspondence table.
    Let's suppose you have a list of 5 users with identifiers 1, 5, 10, 150, and 120. You can manage that:

    ::

        users_solutions = [1, 5, 10, 150, 120] # Correspondence table
        for solution in kernel.ordered_solutions:
            print("User identifier: " + str(users_solutions[solution]))

    |

    The instance attributes are:

    matrix:
        Matrix representing the values of each solution for each criteria.

    nb_criteria:
        Number of criteria.

    criteria:
        List of criteria.

    nb_solutions:
        Number of solutions.

    solutions:
        List of solutions.

    ordered_solutions:
        Ordered list of solutions after the ranking.
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
            criterion = KernelCriterion(criterion_id, self.nb_solutions)
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
    def set_criterion(self, id: int, criterion: Criterion, weight: float = 0.0) -> Criterion:
        """
        Assign a type and a weight to a given criterion.

        :param id: Identifier of the criterion.
        :param criterion: Criterion (must be an inheriting class of 'Criterion').
        :param weight: Weight of the criterion.
        :return: the criterion.
        """

        self.criteria[id].criterion = criterion
        self.criteria[id].weight = weight
        return criterion

    # -------------------------------------------------------------------------
    def apply_config(self, config: dict) -> bool:
        """
        Look in a dictionary if some entries corresponds to criteria parameters. It is supposed that the
        dictionary has an entry named after each criterion and that its value is itself a dictionary with one
        (entry, value) pair for each parameter

        :param config: Configuration dictionary.
        """
        for criterion in self.criteria:
            if criterion.criterion.name not in config:
                continue
            criterion_dict = config[criterion.criterion.name]
            criterion.criterion.apply_config(config=criterion_dict)
            if "weight" in criterion_dict:
                criterion.weight = float(criterion_dict["weight"])

    # -------------------------------------------------------------------------
    def rank(self, matrix: ndarray) -> None:
        """
        Rank the solutions and store the results in 'Kernel.ordered_solutions'.

        :param matrix: The matrix (solutions,criteria) containing the values of the solutions for each criteria.
        :return: nothing
        """

        if (self.nb_solutions < 2) or (self.nb_criteria==0):
            self.ordered_solutions = []
            for solution in self.solutions:
                self.ordered_solutions.append(solution)
            return

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
            for (criterion,val) in zip(self.criteria,solution.values):
                solution.fi_plus += criterion.weight * val.fi_plus
                solution.fi_minus += criterion.weight * val.fi_minus
            solution.fi_plus /= total_weight * (len(self.solutions) - 1)
            solution.fi_minus /= total_weight * (len(self.solutions) - 1)
            solution.fi = solution.fi_plus - solution.fi_minus

        # Rank the solutions by fitness
        self.ordered_solutions = []
        for solution in self.solutions:
            self.ordered_solutions.append(solution)
        self.ordered_solutions.sort(reverse=True, key=lambda solution: solution.fi)
