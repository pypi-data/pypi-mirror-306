from typing import Tuple
import numpy.typing as npt
from abc import abstractmethod, ABC
import numpy as np

class AbstractConstraint(ABC):
    def __init__(self, d: int) -> None:
        super().__init__()
        self._d = d

    @abstractmethod
    def get_one_element(self):
        pass
    
    def get_grid(self, num: int) -> Tuple[npt.NDArray, npt.NDArray]:
        x = np.linspace(-self._r, self._r, num)
        y = np.linspace(-self._r, self._r, num)
        
        return np.meshgrid(x, y)

    def get_dimension(self) -> int:
        """
        Gives the dimension of the constraint.

        Returns
        -------
            out : int
                The dimension of the constraint.
        """
        return self._d
