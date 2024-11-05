""" This module implements helping functions for the introduced types. """

import hashlib
import numpy as np
from typing import Union, Iterable, List, Dict
from .globals import ScalarOrArray, FloatOrArray


def size(x: ScalarOrArray) -> int:
    """ Returns the number of elements in x.

    :param x:
    :return: the number of elements in x.
    """

    if isinstance(x, np.ndarray):
        return x.size
    else:
        return 1


def to_1d_array(x: Union[float, int, Iterable, np.ndarray]) -> np.ndarray:
    """  Transforms x into a 1d array.

    :param x:
    :return: a 1-dimensional array corresponding to x.
    """

    return np.asarray(x).reshape(1, -1)[0, :]


def to_float_if_singleton(x: FloatOrArray) -> FloatOrArray:
    """ Transforms x into a Float if it has a single element.

    :param x:
    :return: x if it is an array, or x as a float if it has only a single element.
    """

    if x.size == 1:
        return x.flatten()[0]
    else:
        return x


def has_nan(x: np.ndarray) -> bool:
    """ Checks whether any element in x is NaN.

    :param x:
    :return: True if any element in x is NaN, False otherwise.
    """
    return np.isnan(np.sum(x))


def compute_hash(a: np.ndarray,
                 n_chars: int = -1,
                 include_dtype: bool = False,
                 include_shape: bool = False) -> str:
    """ Returns a hash for the given array a. The hashing algorithm for np arrays is based on
    https://stackoverflow.com/questions/64753916/unique-identifier-for-numpy-array

    :param a:
    :param n_chars: the number of characters in the hashing string.
    :param include_dtype: if True also incorporate the dtype in the hash.
    :param include_shape: if True also incorporate the shape in the hash (so two arrays with identical elements but a different shape receive a different hash string).
    :return: the hash string corresponding to the given array.
    """

    data = bytes()
    if include_dtype:
        data += str(a.dtype).encode('ascii')
        data += b','
    if include_shape:
        data += str(a.shape).encode('ascii')
        data += b','
    data += a.tobytes()
    hash_values = hashlib.sha256(data).hexdigest()
    return hash_values[:n_chars]


def dicts_to_array(dicts: List[dict]) -> np.ndarray:
    """ Converts a list of dicts with indices as keys to an array.

    :param dicts:
    :return: array corresponding to the list.
    """

    result_dict = {}
    for d in dicts:
        result_dict.update(d)

    return dict_to_array(result_dict)


def dict_to_array(d: Dict[int, float]) -> np.ndarray:
    """ Convert a dict with indices as keys to an array.

    :param d:
    :return: array corresponding to the dict.
    """

    idx = np.array(list(d.keys()))
    val = np.array(list(d.values()))

    out = np.zeros(shape=val.shape)
    out[idx[:]] = val
    return out
