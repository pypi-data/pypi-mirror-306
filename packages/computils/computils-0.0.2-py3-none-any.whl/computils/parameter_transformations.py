""" This module contains transformations and their inverse functions for imposing parameter restrictions. """

import numpy as np


def impose_lower_bound(transformed_parameter: float, lower_bound: float) -> float:
    """ Imposes a lower bound on transformed_parameter.

    :param transformed_parameter: any real number.
    :param lower_bound: any real number.
    :return: the corresponding parameter value with the lower bound imposed.
    """

    return np.exp(transformed_parameter) + lower_bound


def inverse_impose_lower_bound(parameter: float, lower_bound: float) -> float:
    """ Applies the inverse lower-bound transformation to parameter.

    :param parameter: a real number which adheres to the given lower bound.
    :param lower_bound: any real number.
    :return: the transformed parameter, which can take on any real number.
    """

    return np.log(parameter - lower_bound)


def impose_upper_bound(transformed_parameter: float, upper_bound: float) -> float:
    """ Imposes an upper bound on transformed_parameter.

    :param transformed_parameter: any real number.
    :param upper_bound: any real number.
    :return: the corresponding parameter value with the upper bound imposed.
    """

    return -np.exp(transformed_parameter) + upper_bound


def inverse_impose_upper_bound(parameter: float, upper_bound: float) -> float:
    """ Applies the inverse upper-bound transformation to parameter.

    :param parameter: a real number which adheres to the given upper bound.
    :param upper_bound: any real number.
    :return: the transformed parameter, which can take on any real number.
    """

    return np.log(upper_bound - parameter)


def impose_bounds(transformed_parameter: float, lower_bound: float, upper_bound: float) -> float:
    """ Imposes a lower and an upper bound on transformed_parameter.

    :param transformed_parameter: any real number.
    :param lower_bound: any real number.
    :param upper_bound: any real number strictly larger than lower bound.
    :return: a real number which adheres to the given bounds.
    """

    return lower_bound + (upper_bound - lower_bound)/(1.0 + np.exp(-transformed_parameter))


def inverse_impose_bounds(parameter: float, lower_bound: float, upper_bound: float) -> float:
    """ Applies the inverse bounds transformation to parameter.

    :param parameter: a real number which adheres to the given bounds.
    :param lower_bound: any real number.
    :param upper_bound: any real number strictly larger than lower bound.
    :return: the transformed parameter, which can take on any real number.
    """

    z = (parameter - lower_bound)/(upper_bound - lower_bound)
    return np.log(z) - np.log(1.0 - z)


def impose_upper_bound_sum(transformed_params: np.ndarray, upper_bound: float) -> np.ndarray:
    """ Imposes an upper bound on the sum of params, such that all params are in (0, upper_bound).

    :param transformed_params: (n_params,) array of transformed parameters, real numbers
    :param upper_bound: real number
    :return: constrained_params: (n_params,) array of parameters with constraints
    """

    exp_trans_params = np.exp(transformed_params)
    constrained_params = upper_bound * np.divide(exp_trans_params, np.sum(exp_trans_params) + 1.0)
    return constrained_params


def inverse_impose_upper_bound_sum(params: np.ndarray, upper_bound: float) -> np.ndarray:
    """  Inverse transformation function of impose_upper_bound_sum.

    :param params: (n_params,) array of params that are all in (0, upper_bound)
    :param upper_bound: real number
    :return: unconstrained_params
    """

    sum_params = np.sum(params)
    unconstrained_params = np.log(params / (upper_bound - sum_params))
    return unconstrained_params
