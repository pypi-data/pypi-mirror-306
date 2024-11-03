from typing import Tuple
import numpy as np
import numpy.typing as npt
from algosto.constraints import AbstractConstraint

class RdBallConstraint(AbstractConstraint):
    """
    A constraint on the ball in Rd with center ``c`` and radius ``r``.

    Parameters
    ----------
    d : int
        The space dimension.
    c : array_like
        The center of the ball in Rd.
    r : float
        The radius of the ball.
        
    Raises
    ------
    ValueError
        If the array that gives the center of the ball has not the same length as `d`.
    """
    def __init__(self, d: int, c: npt.NDArray[np.float64], r: float) -> None:
        super().__init__(d)
        
        if d != c.shape[0]:
            raise ValueError("The center of the ball must be a 1-D numpy array of shape d.")
        
        self._d = d
        self._c = c
        self._r = r
    
    def get_one_element(self) -> npt.NDArray[np.float64]:
        """
        Gives randomly one element which is inside the constraint.
        
        It follows a uniform law.

        Returns
        -------
        out : ndarray
            A vector in Rd inside the constraint.
        """
        x = np.random.rand(self._d) * 2 - 1
        x /= np.linalg.norm(x)
        
        return x * (self._r - np.random.uniform(0, self._r))
    
    def get_grid(self, num: int) -> Tuple[npt.NDArray, npt.NDArray]:
        """
        Gives a grid of `num` elements on ``X`` and ``Y``.

        Parameters
        ----------
            num : int
                The number of points on one axis to make the grid.

        Returns
        -------
            out : Tuple[ndarray, ndarray]
                returns X and Y.
        """
        X, Y = super().get_grid(num)
        
        norm = np.sqrt(X**2 + Y**2)
        
        X[norm > self._r] = np.nan
        Y[norm > self._r] = np.nan
        
        return X, Y
    
    def get_dimension(self) -> int:
        """
        Gives the dimension of the constraint.

        Returns
        -------
            out : int
                The dimension of the constraint.
        """
        return super().get_dimension()
