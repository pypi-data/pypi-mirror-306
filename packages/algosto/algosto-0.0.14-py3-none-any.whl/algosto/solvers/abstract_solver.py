from abc import ABC, abstractmethod
from typing import Callable
import numpy as np
import numpy.typing as npt

from algosto.constraints import AbstractConstraint

class AbstractSolver(ABC):
    def __init__(self, ct: AbstractConstraint, objective: Callable) -> None:
        super().__init__()

        self._ct = ct
        self._objective = objective

        self._trajectory = list()

    @abstractmethod
    def fit(self, x_start: npt.NDArray = None, n_iter: int = 1000):
        pass

    def get_trajectory(self) -> npt.NDArray:
        """
        Returns the trajectory registered by the solver during the ``fit`` operation.
        
        It's a matrix of size ``(n, d)``.

        Returns
        -------
            out : ndarray
                An array of dimension ``(n_iter, d)`` where d is the dimension defined in the constraint
        """
        return np.array(self._trajectory)
    
            
    def get_objective(self) -> Callable:
        """
        Returns the objective function registered by the solver.

        Returns
        -------
            out : Callable
                The objective function is registered by the solver at its instanciation.
        """
        return self._objective
    
    def get_constraint(self) -> AbstractConstraint:
        """
        Returns the constraint registered by the solver

        Returns
        -------
            out : AbstractConstraint
                The constraint is registered by the solver at its instanciation.
        """
        return self._ct
