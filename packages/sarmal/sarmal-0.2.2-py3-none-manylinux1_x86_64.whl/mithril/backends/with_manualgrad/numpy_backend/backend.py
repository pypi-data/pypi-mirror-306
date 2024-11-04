# Copyright 2022 Synnada, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Callable
from functools import partial

import numpy as np

from ....core import dtype
from ...backend import Backend
from . import common_functions, ops, ops_grad, utils


class NumpyBackend(Backend[np.ndarray]):
    """A backend implementation for the Mithril library using NumPy with
    manual gradient support.

    Parameters
    ----------
    device: str, optional
        The device on which to perform computations, default is "cpu".
    precision: int, optional
        The precision of the arrays, either 32 or 64, default is 32.
    """

    type = "numpy"

    registered_primitives = {}
    primitive_fn_path = "mithril.backends.with_manualgrad.numpy_backend.ops"
    primitive_grad_fn_path = "mithril.backends.with_manualgrad.numpy_backend.ops_grad"
    registered_primitives_grad_fn: dict[str, Callable] = {}

    def __init__(self, device: str = "cpu", precision: int = 32) -> None:
        self._init_dtypes()

        self._precision = precision
        if device != "cpu":
            raise RuntimeError(
                f"Specified device: '{device}' is not available!"
                f"Available devices: {NumpyBackend.get_available_devices()}"
            )
        self._device = device

        super().__init__()

        self.fn_dict = common_functions.fn_dict
        self.array_creation_funcs = ops.array_creation_funcs
        self.primitive_function_dict = ops.primitive_func_dict
        self.primitive_grad_function_dict = ops_grad.primitive_grad_func_dict
        self.fn_dict.update(
            {
                key: self._creation_fn_wrapper(fn)
                for key, fn in common_functions.creation_fn_dict.items()
            }
        )
        self.fn_dict.update(
            {
                key: self._conversion_fn_wrapper(fn)
                for key, fn in common_functions.conversion_fn_dict.items()
            }
        )

        self._initialize_attributes()
        np.random.seed(self.seed)

    @property
    def is_manualgrad(self):
        return True

    @property
    def inf(self):
        return np.inf

    def get_backend_array_type(self):
        return np.ndarray

    @staticmethod
    def get_available_devices() -> list[str]:
        """Static method to get available devices. Currently, in the NumpyBackend,
        only the "cpu" device is supported.

        Parameters
        ----------
        list[str]
            List of available devices.
        """
        return ["cpu"]

    @staticmethod
    def register_primitive(fn: Callable, fn_grad: Callable) -> None:  # type: ignore[override]
        formula_key = fn.__name__
        NumpyBackend.registered_primitives[formula_key] = fn
        NumpyBackend.registered_primitives_grad_fn[formula_key + "_grad"] = fn_grad

    def set_seed(self, seed: int):
        self.seed = seed
        np.random.seed(seed)

    def _creation_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for NumPy array creation functions.

        Parameters
        ----------
        fn: Callable
            The original array creation function.

        Returns
        -------
        Callable
            A wrapped function that creates NumPy arrays with specified dtype.

        Notes
        -----
        This wrapper ensures that NumPy arrays are created with the correct dtype.
        """
        return partial(utils.creation_fn_wrapper, fn=fn, precision=self.precision)

    def _conversion_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for NumPy array conversion functions.

        Parameters
        ----------
        fn: Callable
            The original array conversion function.

        Returns
        -------
        Callable
            A wrapped function that converts arrays to NumPy arrays with
            specified dtype.

        Notes
        -----
        This wrapper handles the conversion of arrays to NumPy arrays with
        different dtypes.
        """
        return partial(utils.conversion_fn_wrapper, fn=fn, precision=self.precision)

    def _init_dtypes(self):
        for name, value in utils.dtype_map.items():
            setattr(self, name, value)

    def randn(self, *shape, dtype: dtype | None = None, **kwargs):
        return self._creation_fn_wrapper(np.random.randn)(*shape, dtype=dtype, **kwargs)

    def rand(self, *shape, dtype: dtype | None = None, **kwargs):
        return self._creation_fn_wrapper(np.random.rand)(*shape, dtype=dtype, **kwargs)

    def randint(self, low, high, shape, dtype: dtype | None = None):
        return self._creation_fn_wrapper(np.random.randint)(
            low, high, shape, dtype=dtype
        )

    def to_numpy(self, data: np.ndarray) -> np.ndarray:
        return data

    def transpose(
        self, data: np.ndarray, axis: tuple[int, ...] | list[int] | None = None
    ) -> np.ndarray:
        return data.transpose(axis)

    def where(
        self, cond: np.ndarray, input1: np.ndarray, input2: np.ndarray
    ) -> np.ndarray:
        return ops.where(cond, input1, input2)

    # TODO: Analyze the code's efficiency and refactor it if necessary.
    # topk_namedtuple = namedtuple('topk_namedtuple', ['values', 'indices'])
    def topk(self, array: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
        array = np.asarray(array)
        flat = array.ravel()
        indices = np.argpartition(flat, -k)[-k:]
        argsort = np.argsort(-flat[indices])

        indices = indices[argsort]
        values = flat[indices]
        leading_dims = len(array.shape) - len(values.shape)
        values = values.reshape((-1,) * leading_dims + values.shape)
        tuple_indices = np.unravel_index(indices, array.shape)
        if len(tuple_indices) == 1:
            (indices,) = tuple_indices
        return (values, indices)

    def softmax(self, input: np.ndarray, dim: int = -1) -> np.ndarray:
        return ops.softmax(input, axis=dim)

    def multinomial(
        self, probs: np.ndarray, num_samples: int, replacement: bool = False
    ) -> np.ndarray:
        input = np.asarray(probs)
        if input.ndim == 1:
            input = input[None, :]
            squeeze_result = True
        else:
            squeeze_result = False

        batch_size, num_categories = input.shape

        # Normalize probabilities
        input = input / np.sum(input, axis=-1, keepdims=True)

        if replacement:
            # Use standard numpy.random.choice
            samples = np.vstack(
                [
                    np.random.choice(
                        num_categories, size=num_samples, p=p, replace=True
                    )
                    for p in input
                ]
            )
        else:
            if num_samples > num_categories:
                raise ValueError(
                    f"Cannot sample {num_samples} samples without replacement "
                    f"from {num_categories} categories"
                )

            # Gumbel-max trick for parallel sampling without replacement
            z = -np.log(-np.log(np.random.random((batch_size, num_categories))))
            # Add log probabilities for Gumbel-max trick
            z = z + np.log(np.maximum(input, 1e-37))
            # Get top k indices
            samples = np.argsort(-z, axis=1)[:, :num_samples]

        if squeeze_result:
            samples = np.squeeze(samples, axis=0)

        return samples

    def cat(
        self, inputs: tuple[np.ndarray, ...] | list[np.ndarray], dim: int = 0
    ) -> np.ndarray:
        return ops.concat(*inputs, axis=dim)
