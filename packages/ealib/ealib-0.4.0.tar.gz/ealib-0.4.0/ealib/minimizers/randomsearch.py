# -*- coding: utf-8 -*-

# Copyright (c) 2013,2014,2015,2016,2017,2024 Jeremie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from dataclasses import dataclass
import numpy as np

from .optimizer import Optimizer


@dataclass
class RandomSearchResult:
    best_solution: np.ndarray
    best_objective: float
    solution_history: np.ndarray
    objective_history: np.ndarray


class RandomSearch(Optimizer):

    def minimize(
        self,
        objective_function,
        init_solution,
        standard_deviation=1.,
        num_iterations=50,
        plot=False
    ) -> RandomSearchResult:

        best_solution = init_solution
        best_objective = objective_function(best_solution)

        solution_history = []
        objective_history = []

        for i in range(num_iterations):
            random_solution = np.random.normal(loc=best_solution, scale=standard_deviation)
            random_objective = objective_function(random_solution)

            if random_objective < best_objective:
                best_solution = random_solution
                best_objective = random_objective

            solution_history.append(best_solution)
            objective_history.append(best_objective)

        solution_history = np.array(solution_history).T
        objective_history = np.array(objective_history)

        result = RandomSearchResult(
            best_solution=best_solution,
            best_objective=best_objective,
            solution_history=solution_history,
            objective_history=objective_history
        )

        return result
