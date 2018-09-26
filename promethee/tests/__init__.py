from unittest import TestCase

import promethee
import numpy as np;

class TestPROMETHEE(TestCase):

    def test_promethee(self, weight_power: float = 1.0):

        matrix =  a = np.matrix('8.75 6.2 1 30; 13.75 7.5 1 50; 25 8 3 80; 62.5 20 2 120')
        print(matrix)

        kernel = promethee.Kernel(nb_criteria=4, nb_solutions=4)
        kernel.set_criterion(0, 1.0,
                             promethee.LinearCriterion(name="Price", type=promethee.Criterion.Minimize, p=0.2, q=0.05))
        kernel.set_criterion(1, 1.0,
                             promethee.LinearCriterion(name="Cons", type=promethee.Criterion.Minimize, p=0.2, q=0.05))
        kernel.set_criterion(2, 1.0,
                             promethee.LinearCriterion(name="Comfort", type=promethee.Criterion.Maximize, p=0.2, q=0.05))
        kernel.set_criterion(3, weight_power,
                             promethee.LinearCriterion(name="Power", type=promethee.Criterion.Maximize, p=0.2, q=0.05))
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