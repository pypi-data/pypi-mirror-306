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
from typing import Callable

from .optimizer import Optimizer


@dataclass
class GeneticAlgorithmResult:
    best_solution: np.ndarray
    best_objective: float
    solution_history: np.ndarray
    objective_history: np.ndarray
    best_solution_history: np.ndarray
    best_objective_history: np.ndarray


class GeneticAlgorithm(Optimizer):

    def minimize(
        self,
        objective_function: Callable[[np.ndarray], float],
        init_pop_mean: np.ndarray,
        init_pop_std: np.ndarray,
        num_gen: int = 50,
        pop_size: int = 100,
        mutation_rate: float = 0.01,
        plot: bool = False
    ) -> GeneticAlgorithmResult:
        """
        Minimize the objective function using a genetic algorithm.
    
        Parameters
        ----------
        objective_function : Callable[[np.ndarray], float]
            The objective function to minimize.
        init_pop_mean : np.ndarray
            The mean of the initial population. Shape: (n_dimensions,)
        init_pop_std : np.ndarray
            The standard deviation of the initial population. Shape: (n_dimensions,)
        num_gen : int, optional
            The number of generations (iterations) to run the algorithm (default is 50).
        pop_size : int, optional
            The size of the population (default is 100).
        mutation_rate : float, optional
            The mutation rate (default is 0.01).
        plot : bool, optional
            Whether to plot the progress of the algorithm (default is False).
    
        Returns
        -------
        best_solution : np.ndarray
            The best solution found by the algorithm. Shape: (n_dimensions,)
        best_objective : float
            The objective value of the best solution.
        solution_history : np.ndarray
            The history of solutions over generations. Shape: (n_dimensions, num_gen, pop_size)
        objective_history : np.ndarray
            The history of objective values over generations. Shape: (1, num_gen, pop_size)
        """
        
        # TODO vérif cohérence pop_size et init_pop_mean / init_pop_std
    
        # Solution history is a 3D array:
        #   - 1st dimension: the solutions dimension
        #   - 2nd dimension: the generation number (or iteration number)
        #   - 3rd dimension: the individuals dimension
        # Thus with a run of 100 iterations, a 2D objective function and a population size of 30, solution_history will have a shape of (2, 100, 30)
        solution_history = np.zeros((len(init_pop_mean), num_gen, pop_size))
    
        # Objective history is a 3D array:
        #   - 1st dimension: the number of objectives to optimize (by default 1)
        #   - 2nd dimension: the generation number (or iteration number)
        #   - 3rd dimension: the individuals dimension
        # Thus with a run of 100 iterations, a mono objective function and a population size of 30, solution_history will have a shape of (1, 100, 30)
        objective_history = np.zeros((1, num_gen, pop_size))
    
        # Initialisation de la population
        population = np.random.normal(init_pop_mean, init_pop_std, (pop_size, len(init_pop_mean)))
    
        for generation in range(num_gen):
            # Évaluation
            fitness = np.array([objective_function(ind) for ind in population])
    
            # Enregistrement de la population et des valeurs d'objectifs
            solution_history[:, generation, :] = population.T
            objective_history[0, generation, :] = fitness
    
            # Sélection
            selected_indices = np.argsort(fitness)[:pop_size // 2]
            selected_population = population[selected_indices]
    
            # Croisement
            new_population = []
            for _ in range(pop_size // 2):
                parents = selected_population[np.random.choice(len(selected_population), 2, replace=False)]
                if len(parents[0]) > 2:
                    crossover_point = np.random.randint(1, len(parents[0]) - 1)
                else:
                    crossover_point = 1  # or some other logic
                child1 = np.concatenate((parents[0][:crossover_point], parents[1][crossover_point:]))
                child2 = np.concatenate((parents[1][:crossover_point], parents[0][crossover_point:]))
                new_population.extend([child1, child2])
    
            # Mutation
            new_population = np.array(new_population)
            mutations = np.random.rand(*new_population.shape) < mutation_rate
            new_population = new_population + mutations * np.random.normal(0, 1, new_population.shape)
    
            population = new_population
    
        # Retourner le meilleur individu
        best_index = np.argmin([objective_function(ind) for ind in population])
        best_solution = population[best_index]
        best_objective = objective_function(best_solution)

        # Historique du meilleur individu pour chaque génération
        best_objective_history = objective_history.argmin(axis=2)
        best_solution_history = solution_history[:, :, best_objective_history]

        # best_solution_history = solution_history[:, :, best_index]
        # best_objective_history = objective_history[0, :, best_index]

        # Historique du meilleur individu pour chaque génération
        best_solution_index_history = objective_history.argmin(axis=2).flatten()
        best_objective_history = objective_history[0, np.arange(num_gen), best_solution_index_history]
        best_solution_history = solution_history[:, np.arange(num_gen), best_solution_index_history]

        result = GeneticAlgorithmResult(
            best_solution=best_solution,
            best_objective=best_objective,
            solution_history=solution_history,
            objective_history=objective_history,
            best_solution_history=best_solution_history,
            best_objective_history=best_objective_history
        )
    
        return result
