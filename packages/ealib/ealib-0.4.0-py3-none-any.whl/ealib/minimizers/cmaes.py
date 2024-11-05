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
class CMAESResult:
    best_solution: np.ndarray
    best_objective: float
    solution_history: np.ndarray
    objective_history: np.ndarray


class CMAES(Optimizer):

    def minimize(
        self,
        objective_function,
        init_solution,
        standard_deviation=1.,
        num_iterations=50,
        population_size=10,
        plot=False
    ) -> CMAESResult:
        n = len(init_solution)
        mean = np.array(init_solution)
        sigma = standard_deviation
        population_size = population_size
        weights = np.log(population_size + 0.5) - np.log(np.arange(1, population_size + 1))
        weights /= np.sum(weights)
        mu_eff = 1 / np.sum(weights ** 2)
        c_sigma = (mu_eff + 2) / (n + mu_eff + 5)
        d_sigma = 1 + 2 * max(0, np.sqrt((mu_eff - 1) / (n + 1)) - 1) + c_sigma
        c_c = (4 + mu_eff / n) / (n + 4 + 2 * mu_eff / n)
        c_1 = 2 / ((n + 1.3) ** 2 + mu_eff)
        c_mu = min(1 - c_1, 2 * (mu_eff - 2 + 1 / mu_eff) / ((n + 2) ** 2 + mu_eff))
        p_c = np.zeros(n)
        p_sigma = np.zeros(n)
        B = np.eye(n)
        D = np.ones(n)
        C = B @ np.diag(D ** 2) @ B.T
        inv_sqrt_C = B @ np.diag(D ** -1) @ B.T
        best_solution = mean
        best_objective = objective_function(best_solution)

        solution_history = []
        objective_history = []

        for i in range(num_iterations):
            population = np.random.multivariate_normal(mean, sigma ** 2 * C, population_size)
            fitness = np.array([objective_function(ind) for ind in population])
            indices = np.argsort(fitness)
            population = population[indices]
            fitness = fitness[indices]

            mean = np.dot(weights, population[:len(weights)])
            p_sigma = (1 - c_sigma) * p_sigma + np.sqrt(c_sigma * (2 - c_sigma) * mu_eff) * inv_sqrt_C @ (mean - best_solution) / sigma
            h_sigma = np.linalg.norm(p_sigma) / np.sqrt(1 - (1 - c_sigma) ** (2 * (i + 1))) < (1.4 + 2 / (n + 1)) * np.sqrt(n)
            p_c = (1 - c_c) * p_c + h_sigma * np.sqrt(c_c * (2 - c_c) * mu_eff) * (mean - best_solution) / sigma
            artmp = (population[:len(weights)] - best_solution) / sigma
            C = (1 - c_1 - c_mu) * C + c_1 * (np.outer(p_c, p_c) + (1 - h_sigma) * c_c * (2 - c_c) * C) + c_mu * artmp.T @ np.diag(weights) @ artmp
            sigma *= np.exp((c_sigma / d_sigma) * (np.linalg.norm(p_sigma) / np.sqrt(1 - (1 - c_sigma) ** (2 * (i + 1))) - 1))

            best_solution = population[0]
            best_objective = fitness[0]

            solution_history.append(best_solution)
            objective_history.append(best_objective)

        solution_history = np.array(solution_history).T
        objective_history = np.array(objective_history)

        result = CMAESResult(
            best_solution=best_solution,
            best_objective=best_objective,
            solution_history=solution_history,
            objective_history=objective_history
        )

        return result