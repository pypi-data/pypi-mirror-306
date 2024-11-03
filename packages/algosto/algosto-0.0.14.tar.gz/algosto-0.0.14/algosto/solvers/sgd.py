from typing import Callable, Any
import numpy as np
import numpy.typing as npt

from algosto.constraints.abstract_constraint import AbstractConstraint
from algosto.solvers import AbstractSolver

class SGDSolver(AbstractSolver):
    """
    The solver for the Stochastic Gradient Descent (SGD) algorithm.

    Parameters
    ----------
    ct : AbstractConstraint
        A constraint object that inherits from ``AbstractConstraint``.
    objective : function
        The objective function to minimize. This function must be able to handle
        a 1-D array of several points.
    grad : function
        The gradient of the objective.
    batch_size : float
        The rate of dimensions kept to compute the gradient.
    gamma : float
        The learning rate.
    """
    def __init__(self, ct: AbstractConstraint, objective: Callable, grad: Callable, batch_size: float = 0.2, gamma: float = 0.1) -> None: # type: ignore
        super().__init__(ct, objective)

        self._grad = grad
        self._batch_size = batch_size
        self._gamma = gamma
    
    def fit(self, x_start: np.ndarray = None, n_iter: int = 1000):
        """
        Run the SGD solver to approximate the solution of the optimization problem.

        Parameters
        ----------
        x_start : array_like
            The point where the algorithm will start running.
        n_iter : int
            The number of iterations. The solver will run exactly this number of times.

        Raises
        ------
        ValueError
            It raises a ``ValueError`` if the dimension of ``x_start`` does not 
            match the dimension of the ``constraint``.
        """
        d = self._ct.get_dimension()

        if x_start is not None and x_start.shape[0] != d:
            raise ValueError(f"The start point must have the same "
                             f"dimension as the constraint."
                             f"Start point has {x_start.shape[0]} and constraint as {d}")

        x = self._ct.get_one_element() if x_start is None else x_start
        self._trajectory.append(x)

        for n in range(1, n_iter):
            random_filter = np.random.choice(x.shape[1], self._batch_size)
            x = x - self._gamma * self._grad(x * random_filter)

            self._trajectory.append(x)
        
    def get_grad(self) -> Callable:
        """
        Returns the gradient function.

        Returns
        -------
            grad : Callable
                The gradient function.
        """
        return self._grad
    
    def get_lr(self) -> float:
        """
        Returns the learning rate.

        Returns
        -------
            lr : float
                The learning rate of the stochastic gradient descent algorithm.
        """
        return self._lr
    
    def get_trajectory(self) -> npt.NDArray:
        """
        Returns the trajectory registered by the solver during the ``fit`` operation.
        
        It's a matrix of size ``(n, d)``.

        Returns
        -------
            out : ndarray
                An array of dimension ``(n_iter, d)`` where d is the dimension defined in the constraint
        """
        return super().get_trajectory()
    
            
    def get_objective(self) -> Callable:
        """
        Returns the objective function registered by the solver.

        Returns
        -------
            out : Callable
                The objective function is registered by the solver at its instanciation.
        """
        return super().get_objective()
    
    def get_constraint(self) -> AbstractConstraint:
        """
        Returns the constraint registered by the solver

        Returns
        -------
            out : AbstractConstraint
                The constraint is registered by the solver at its instanciation.
        """
        return super().get_constraint()
    
    def get_batch_size(self) -> float:
        """
        Returns the batch_size.

        Returns
        -------
            out : float
                The batch size.
        """
        return self._batch_size
