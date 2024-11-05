""" This module is used to instantiate classes in the package. """

from .globals import *
from .interpolation import InternalInterpolator


def create_interpolator(x: np.ndarray,
                        y: np.ndarray,
                        inter_type: InterpolationType,
                        extra_type: ExtrapolationType = ExtrapolationType.nan) -> Interpolator:
    """ Creates an instance of the Interpolator class with the given inter- and extrapolation types.

    :param x:
    :param y:
    :param inter_type:
    :param extra_type:
    :return: an instance of the Interpolator class with the given inter- and extrapolation types.
    """

    return InternalInterpolator(x=x, y=y, inter_type=inter_type, extra_type=extra_type)
