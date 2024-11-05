""" This module collects functionality for fast evaluation of matrix operations. """

import numpy as np
from scipy.sparse import issparse
from scipy.sparse.linalg import inv as sparse_inv
from scipy.linalg import inv, det


def fast_matrix_inversion(M: np.ndarray) -> np.ndarray:
    """ Performs fast matrix inversion.

    :param M:
    :return: The inverse of M.
    """

    if M.size == 1:
        return 1.0 / M
    elif issparse(M):
        return sparse_inv(M)
    else:
        return inv(M)


def fast_determinant(M: np.ndarray) -> float:
    """ Computes the determinant of M.

    :param M:
    :return: det(M).
    """
    if M.size == 1:
        return np.abs(M[0, 0])
    else:
        return det(M)


def fast_quadratic_form(A: np.ndarray,
                        x: np.ndarray) -> float:
    """ Computes the quadratic form x'Ax.

    :param A: An (n,n) array.
    :param x: An (n,1) array.
    :return: the quadratic form x'Ax.
    """
    return (np.dot(x.T, np.dot(A, x)))[0, 0]


def fast_columnwise_bilinear_form(A: np.ndarray,
                                  B: np.ndarray,
                                  C: np.ndarray) -> np.ndarray:
    """ Efficiently compute the bilinear form A_i.T @ B @ C_i for i = 1,...,n, with A_i and C_i denoting the columns
        of the matrices A_i and C_i, respectively.

    :param A: (m, n) np array
    :param B: (m, m) np array
    :param C: (m, n) np array
    :return: an (n,) np array containing the results
    """

    return ((A.T @ B) * C.T).sum(axis=1)


if __name__ == "__main__":
    A = np.array([[1, 2], [3, 5]])
    B = 3.0 * A + 4.2
    C = np.array([[9, 4], [2, 1]])
    x = np.array([[9], [1]])

    from computils.performance_checking import compute_average_running_time
    n_repeats = 1000
    regular_quadratic_form = lambda M, z: z.T @ M @ z
    average_time_regular = compute_average_running_time(regular_quadratic_form, args=(A, x), n_repeats=n_repeats)
    average_time_fast_eval = compute_average_running_time(fast_quadratic_form, args=(A, x), n_repeats=n_repeats)

    print("Regular / fast eval time = {:f}".format(average_time_regular/average_time_fast_eval))
    pass
