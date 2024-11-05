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
class PSOResult:
    best_solution: np.ndarray
    best_objective: float
    solution_history: np.ndarray
    objective_history: np.ndarray
    best_solution_history: np.ndarray
    best_objective_history: np.ndarray


class ParticleSwarmOptimizer(Optimizer):

    def minimize(
        self,
        objective_function: Callable[[np.ndarray], float],
        init_pop_mean: np.ndarray,
        init_pop_std: np.ndarray,
        num_gen: int = 50,
        pop_size: int = 100,
        inertia: float = 0.5,
        cognitive: float = 1.5,
        social: float = 1.5,
        plot: bool = False
    ) -> PSOResult:
        """
        Minimize the objective function using a particle swarm optimization algorithm.
    
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
        inertia : float, optional
            The inertia coefficient (default is 0.5).
        cognitive : float, optional
            The cognitive coefficient (default is 1.5).
        social : float, optional
            The social coefficient (default is 1.5).
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
        best_solution_history : np.ndarray
            The history of the best solutions over generations. Shape: (n_dimensions, num_gen)
        best_objective_history : np.ndarray
            The history of the best objective values over generations. Shape: (1, num_gen)
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
        velocities = np.random.normal(0, 1, (pop_size, len(init_pop_mean)))
        personal_best_positions = population.copy()
        personal_best_scores = np.array([objective_function(ind) for ind in population])
        global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
        global_best_score = np.min(personal_best_scores)
    
        for generation in range(num_gen):
            # Évaluation
            fitness = np.array([objective_function(ind) for ind in population])
    
            # Mise à jour des meilleures positions personnelles
            better_mask = fitness < personal_best_scores
            personal_best_positions[better_mask] = population[better_mask]
            personal_best_scores[better_mask] = fitness[better_mask]
    
            # Mise à jour de la meilleure position globale
            if np.min(fitness) < global_best_score:
                global_best_position = population[np.argmin(fitness)]
                global_best_score = np.min(fitness)
    
            # Enregistrement de la population et des valeurs d'objectifs
            solution_history[:, generation, :] = population.T
            objective_history[0, generation, :] = fitness
    
            # Mise à jour des vitesses et des positions
            r1 = np.random.rand(pop_size, len(init_pop_mean))
            r2 = np.random.rand(pop_size, len(init_pop_mean))
            velocities = (inertia * velocities +
                          cognitive * r1 * (personal_best_positions - population) +
                          social * r2 * (global_best_position - population))
            population = population + velocities
    
        # Historique du meilleur individu pour chaque génération
        best_solution_index_history = objective_history.argmin(axis=2).flatten()
        best_objective_history = objective_history[0, np.arange(num_gen), best_solution_index_history]
        best_solution_history = solution_history[:, np.arange(num_gen), best_solution_index_history]

        result = PSOResult(
            best_solution=global_best_position,
            best_objective=global_best_score,
            solution_history=solution_history,
            objective_history=objective_history,
            best_solution_history=best_solution_history,
            best_objective_history=best_objective_history
        )

        return result