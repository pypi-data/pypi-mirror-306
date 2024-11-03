from typing import Callable
import numpy as np
import numpy.typing as npt

from algosto.solvers import AbstractSolver
from algosto.constraints import AbstractConstraint

class KieferWolfowitzSolver(AbstractSolver):
    """
    The Kiefer-Wolfowitz algorithm wrapped in a solver class.

    Parameters
    ----------
    ct : AbstractConstraint
        A constraint object that inherits from ``AbstractConstraint``.
    objective : Callable
        The objective function to minimize. This function must be able to handle
        a 1-D array of several points.
    a : float
        The ``a`` value as described below.
    alpha : float
        The ``alpha`` value as described below.
    b : float
        The ``b`` value as described below.
    beta : float
        The ``beta`` value as described below.
        
    References
    ----------
    .. [1] Kiefer, J. and Wolfowitz, J., "Stochastic estimation of the maximum of a regression function", *Annals of Mathematical Statistics*, 1952.
        
    Examples
    --------
    >>> ct = RdSquareConstraint(2, 10, np.zeros(2))
    >>> def objective(x: npt.NDArray) -> npt.NDArray:
    ...    # ...
    >>> solver = KieferWolfowitzSolver(ct, objective)
    >>> solver.fit()
    >>> plot(solver)
    """

    def __init__(self,
                 ct: AbstractConstraint,
                 objective: Callable,
                 a: float = 1,
                 alpha: float = 0.3,
                 b: float = 1,
                 beta: float = 0.6) -> None:
        super().__init__()
        
        super().__init__(ct, objective)
        self._a = a
        self._alpha = alpha
        self._b = b
        self._beta = beta

    def fit(self, x_start: npt.NDArray[np.float64] = None, n_iter: int = 1000) -> None:
        """
        Run the solver to approximate the solution to the optimization problem.

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
            gamma_n =  self._a/(n**self._alpha)
            c_n = self._b/(n**self._beta)

            Y = self._objective(x.reshape(1, -1).repeat(d, axis=0) + np.eye(d) * c_n)
            Z = self._objective(x.reshape(1, -1).repeat(d, axis=0) - np.eye(d) * c_n)

            gradient_estimate = Y-Z
            x = x + gamma_n * gradient_estimate/(2*c_n)
            
            self._trajectory.append(x)
    
    def get_a(self) -> float:
        """
        Returns the ``a`` value registered by the solver

        Returns
        -------
            out : float
                The ``a`` value.
        """
        return self._a
    
    def get_alpha(self) -> float:
        """
        Returns the ``alpha`` value registered by the solver

        Returns
        -------
            out : float
                The ``alpha`` value.
        """
        return self._alpha
    
    def get_b(self) -> float:
        """
        Returns the ``b`` value registered by the solver

        Returns
        -------
            out : float
                The ``b`` value.
        """
        return self._b
    
    def get_beta(self) -> float:
        """
        Returns the ``beta`` value registered by the solver

        Returns
        -------
            out : float
                The ``beta`` value.
        """
        return self._beta
