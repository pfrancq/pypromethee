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
from unittest import TestCase
from promethee.Kernel import Kernel
from promethee.LinearCriterion import LinearCriterion
import numpy as np;


# ----------------------------------------------------------------------------------------------------------------------
class TestPROMETHEE(TestCase):
    """
    Class to test the PROMETHEE method.
    """

    # -------------------------------------------------------------------------
    def test_promethee(self, weight_power: float = 1.0) -> None:
        """
        Test the PROMETHEE method on a little problem.

        :param weight_power: Weight for the power criterion. Depending of the value, the ranking varies. The method
        verifies 1.0 and 4.0.

        :return: Nothing.
        """

        matrix =  a = np.matrix('8.75 6.2 1 30; 13.75 7.5 1 50; 25 8 3 80; 62.5 20 2 120')
        print(matrix)

        kernel = Kernel(nb_criteria=4, nb_solutions=4)
        kernel.set_criterion(0, 1.0,
                             LinearCriterion(name="Price", type=LinearCriterion.Minimize, p=0.2, q=0.05))
        kernel.set_criterion(1, 1.0,
                             LinearCriterion(name="Cons", type=LinearCriterion.Minimize, p=0.2, q=0.05))
        kernel.set_criterion(2, 1.0,
                             LinearCriterion(name="Comfort", type=LinearCriterion.Maximize, p=0.2, q=0.05))
        kernel.set_criterion(3, weight_power,
                             LinearCriterion(name="Power", type=LinearCriterion.Maximize, p=0.2, q=0.05))
        kernel.rank(matrix)

        print()
        print("Car \t Φ+ \t Φ- \t Φ")
        for sol in kernel.ordered_solutions:
            print("Car " + str(sol.id+1) + '\t' + "{:.3f}".format(sol.fi_plus) + '\t' + "{:.3f}".format(sol.fi_minus) + '\t' + "{:.3f}".format(sol.fi))

        sols = []
        for sol in kernel.ordered_solutions:
            sols.append(sol.id)
        if weight_power == 1.0:
            self.assertTrue(sols == [2, 1, 0, 3])
        elif weight_power == 4.0:
            self.assertTrue(sols == [3, 2, 1, 0])


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    test = TestPROMETHEE()
    test.test_promethee(weight_power=1.0)
    print("# ----------------------------------------------------------------------------------------------------------------------")
    test.test_promethee(weight_power=4.0)