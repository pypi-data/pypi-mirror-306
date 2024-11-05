from hashlib import md5

import numpy as np
from numpy.typing import ArrayLike
from werkzeug.datastructures import ImmutableMultiDict


def encode_array(array, name: str) -> dict:
    """Encodes an array to send it in an HTTP request

    Encodes an array into a dict that can be sent as data in an HTTP request. The
    type of the array is preserved.

    Args:
        array: The numpy array to encode.
        name: The name of the array in the output dict.

    Returns:
        A dict that can be appended to HTTP request data.

    """

    return {
        name: str(array.tobytes(), "ISO-8859-1"),
        f"{name}-shape": array.shape,
        f"{name}-dtype": str(array.dtype),
    }


def decode_array(response: dict, name: str):
    """Decodes an array from an HTTP request
    Decodes an array from an HTTP request that was encoded using encode_array. The
    type of the array is preserved.
    Args:
        response: The HTTP response in dict format.
        name: The name of the array to decode.
    Returns:
        A numpy array decoded from the response.
    """
    # Depending on the source of the data (requests, or flask request), the shape
    # is not encoded in the same way.
    if isinstance(response, ImmutableMultiDict):
        shape = [int(i) for i in response.getlist(f"{name}-shape")]
    else:
        shape = response[f"{name}-shape"]
    dtype = response[f"{name}-dtype"]
    array = np.frombuffer(bytes(response[name], "ISO-8859-1"), dtype=dtype)
    array = array.reshape(shape)
    return array


def hash_array(array: ArrayLike) -> str:
    """Given an array, create a hash for fast matching."""
    flat_array = np.asarray(array).ravel()
    flat_array.flags.writeable = False
    return md5(flat_array.data).hexdigest()


def hash_array_with_sorting(array: ArrayLike) -> str:
    """Given an array, sort it and then create a hash for fast matching."""
    return hash_array(np.sort(array, axis=None))
