import numpy as np
import matplotlib.pyplot as plt

from algosto.solvers import AbstractSolver

def plot(solver: AbstractSolver, num: int = 300) -> None:
    """_summary_

    Parameters
    ----------
        solver : AbstractSolver
            An array, any object exposing the array interface, an object whose __array__ method returns an array, or any (nested) sequence. If object is a scalar, a 0-dimensional array containing object is returned.
    """
    X, Y = solver.get_constraint().get_grid(num)
    points = np.vstack((X.flatten(), Y.flatten())).T
    Z = solver.get_objective()(points)
    Z = Z.reshape((num, num))
    
    X = np.nan_to_num(X, nan=0)
    Y = np.nan_to_num(Y, nan=0)

    plt.figure(figsize=(6, 6))

    # Plot surface
    contour = plt.contourf(X, Y, Z, levels=20, cmap='viridis')
    plt.colorbar(contour)

    # Plot trajectory
    trajectory = solver.get_trajectory()
    plt.plot(trajectory[:,0], trajectory[:,1], 'r-', markersize=8)
    
    # Plot
    x_start = solver.get_trajectory()[0]
    x_end = solver.get_trajectory()[-1]
    plt.scatter(x_start[0], x_start[1], c='gray')
    plt.scatter(x_end[0], x_end[1], c='white')

    plt.title("Graphe")
    plt.axis('equal')

    plt.show()
