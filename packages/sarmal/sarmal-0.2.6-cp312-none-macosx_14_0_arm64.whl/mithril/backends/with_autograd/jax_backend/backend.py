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

import math
import os
from collections.abc import Callable
from functools import partial

import jax
import numpy as np

from .... import core
from ...backend import ParallelBackend
from ...utils import process_shape
from . import common_functions, ops, utils
from .parallel import JaxParallel

__all__ = ["JaxBackend"]


class JaxBackend(ParallelBackend[jax.numpy.ndarray]):
    """JaxBackend: A backend implementation for the Mithril library using Jax.

    Parameters
    ----------
    device: str, optional
        The device on which to perform computations, default is "cpu".
    precision: int, optional
        The precision of the arrays, either 32 or 64, default is 32.
    pre_allocate: bool, optional
        This argument controls whether JAX pre-allocates memory, default is False.
    """

    type = "jax"
    registered_primitives = {}
    primitive_fn_path = "mithril.backends.with_autograd.jax_backend.ops"

    def __init__(
        self,
        device: str = "cpu",
        precision: int = 32,
        pre_allocate: bool = False,
        device_mesh: tuple[int, ...] | None = None,
    ) -> None:
        self._device = device
        utils.get_device(device)  # Check device is available
        self._precision = precision
        self._parallel_manager: JaxParallel | None = None

        super().__init__(device_mesh=device_mesh)

        if device_mesh is not None:
            self._create_parallel(device_mesh=device_mesh)

        os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = str(pre_allocate).lower()

        self.fn_dict = common_functions.fn_dict
        self.array_creation_funcs = ops.array_creation_funcs
        self.primitive_function_dict = ops.primitive_func_dict

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

        self._init_dtypes()
        self._initialize_attributes()
        self.prng_key = jax.random.PRNGKey(self.seed)

    # @staticmethod
    # def is_installed():
    #     return is_backend_installed

    # @staticmethod
    # def __check_installation():
    #     if not is_backend_installed:
    #         raise RuntimeError("Jax is not installed!")

    @property
    def is_manualgrad(self):
        return False

    @property
    def inf(self):
        return jax.numpy.inf

    def get_backend_array_type(self):
        return jax.Array

    # @property
    # def is_backend_installed(self):
    #     return is_backend_installed

    @property
    def device(self):
        return utils.get_device(self._device)

    # TODO: This property is weird! Investigate why this property is used.
    @property
    def ArrayType(self):  # noqa: N802
        return utils.ArrayType

    @staticmethod
    def get_available_devices():
        """Static method to get a list of available devices.

        Parameters
        ----------
        list[str]
            List of available devices.
        """
        return utils.get_available_devices()

    @staticmethod
    def register_primitive(fn: Callable) -> None:
        JaxBackend.registered_primitives[fn.__name__] = fn

    def set_seed(self, seed: int):
        self.seed = seed
        self.prng_key = jax.random.PRNGKey(seed)

    def to_device(
        self, data: jax.Array, device: str, asynchronous: bool = True
    ) -> jax.Array:
        """Move data to the specified device.

        Parameters
        ----------
        data: jax.Array
            The data to be moved to the specified device.
        device: str
            The target device for the data.
        """
        _device = utils.get_device(device)
        if not asynchronous:
            return jax.device_put(data, device=_device).block_until_ready()
        return jax.device_put(data, device=_device)

    def to_numpy(self, arr: jax.Array) -> np.ndarray:
        # TODO: docstring
        return np.array(arr)

    def transpose(
        self, data: jax.Array, axis: tuple[int, ...] | list[int] | None = None
    ) -> jax.Array:
        return data.transpose(axis)

    def block_until_ready(self, data: jax.Array):
        """Block until the specified data is ready.

        Parameters
        ----------
        data: jax.Array
            The data for which the method will block until it is ready.
        """
        data.block_until_ready()

    def _creation_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for array creation functions.

        Parameters
        ----------
        fn: Callable
            The original array creation function.

        Returns
        -------
        Callable
            A wrapped function that creates arrays with specified dtype and device.

        Notes
        -----
        Ensures that arrays are created with the correct dtype and device.
        """

        array_conversion_fn = partial(
            utils.creation_fn_wrapper,
            fn=fn,
            device=self._device,
            precision=self.precision,
        )
        array_conversion_fn = partial(self._parallelize, fn=array_conversion_fn)

        return array_conversion_fn

    def _conversion_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for array conversion functions.

        Parameters
        ----------
        fn: Callable
            The original array conversion function.

        Returns
        -------
        Callable
            A wrapped function that converts arrays with specified dtype and device.

        Notes
        -----
        Handles the conversion of arrays between different dtypes and devices.

        If dtype is provided, it uses `utils._handle_dtype` to ensure a valid dtype.
        If the input data is a JAX Array, it ensures it's on the specified device.
        If dtype is not provided, uses the default device and handles data precision.
        """
        array_conversion_fn = partial(
            utils.conversion_fn_wrapper,
            fn=fn,
            device=self._device,
            precision=self.precision,
        )
        array_conversion_fn = partial(self._parallelize, fn=array_conversion_fn)

        return array_conversion_fn

    def _parallelize(self, *args, fn: Callable, device_mesh, **kwargs) -> jax.Array:
        """
        Parallelizes the function's return tensor across devices.

        Parameters
        ----------
        fn : Callable
            The function whose return tensor will be parallelized.

        device_mesh : tuple[int, ...], optional
            A tuple specifying the device mesh for parallelization.
            If not provided, the default device mesh is used.

        Returns
        -------
        Callable
            Return tensor parallelized across the specified device mesh.
        """

        tensor: jax.Array = fn(*args, **kwargs)
        if self._parallel_manager is None:
            return tensor
        return self._parallel_manager.parallelize(tensor, device_mesh)

    def randn(self, *shape, device_mesh=None, **kwargs):
        _shape = process_shape(shape)
        result = utils.creation_fn_wrapper(
            fn=jax.random.normal,
            key=self.prng_key,
            device=self._device,
            precision=self.precision,
            shape=_shape,
            **kwargs,
        )
        if self._parallel_manager is not None:
            result = self._parallel_manager.parallelize(result, device_mesh=device_mesh)

        # Update prng_key
        self.prng_key, _ = jax.random.split(self.prng_key)
        return result

    def rand(self, *shape, device_mesh=None, **kwargs):
        _shape = process_shape(shape)
        result = utils.creation_fn_wrapper(
            fn=jax.random.uniform,
            key=self.prng_key,
            device=self._device,
            precision=self.precision,
            shape=_shape,
            **kwargs,
        )
        if self._parallel_manager is not None:
            result = self._parallel_manager.parallelize(result, device_mesh=device_mesh)
        # Update prng_key
        self.prng_key, _ = jax.random.split(self.prng_key)
        return result

    def randint(
        self,
        low: int,
        high: int,
        shape: tuple[int, ...],
        dtype: core.dtype | None = None,
        device_mesh=None,
        **kwargs,
    ):
        _shape = process_shape(shape)
        result = utils.creation_fn_wrapper(
            fn=jax.random.randint,
            key=self.prng_key,
            device=self._device,
            precision=self.precision,
            shape=_shape,
            minval=low,
            maxval=high,
            **kwargs,
        )
        if self._parallel_manager is not None:
            result = self._parallel_manager.parallelize(result, device_mesh=device_mesh)

        # Update prng_key
        self.prng_key, _ = jax.random.split(self.prng_key)
        return result

    def dot(self, *args, **kwargs):
        return jax.numpy.dot(*args, **kwargs)

    def sort(self, *args, **kwargs):
        return jax.numpy.sort(*args, **kwargs)

    def log(self, *args, **kwargs):
        return jax.numpy.log(*args, **kwargs)

    def isnan(self, *args, **kwargs):
        return jax.numpy.isnan(*args, **kwargs)

    def atleast_1d(self, *args, **kwargs):
        return jax.numpy.atleast_1d(*args, **kwargs)

    def abs(self, array: jax.Array) -> jax.Array:
        return jax.numpy.abs(array)

    def sin(self, array: jax.Array) -> jax.Array:
        return jax.numpy.sin(array)

    def cos(self, array: jax.Array) -> jax.Array:
        return jax.numpy.cos(array)

    def relu(self, array: jax.Array) -> jax.Array:
        return jax.nn.relu(array)

    def leaky_relu(self, array: jax.Array, slope: jax.Array) -> jax.Array:
        return jax.nn.leaky_relu(array, slope)

    def tanh(self, array: jax.Array) -> jax.Array:
        return jax.nn.tanh(array)

    def sigmoid(self, array: jax.Array) -> jax.Array:
        return jax.nn.sigmoid(array)

    def softplus(self, array: jax.Array) -> jax.Array:
        return jax.nn.softplus(array)

    # make this dtypes automatically load from utils map!
    def _init_dtypes(self):
        for name, value in utils.dtype_map.items():
            setattr(self, name, value)

    def _register_callable(
        self, fn: Callable | partial, fn_name: str, jit: bool = False
    ):
        assert (
            self._parallel_manager is not None
        ), "Parallel manager is not initialized!"

        fn_name = str(id(self)) + fn_name
        return self._parallel_manager.register_callable(fn, fn_name, jit)

    def _run_callable(self, *primals, fn_name: str):
        assert (
            self._parallel_manager is not None
        ), "Parallel manager is not initialized!"

        fn_name = str(id(self)) + fn_name
        return self._parallel_manager.run_callable(*primals, fn_name=fn_name)

    def _create_parallel(self, device_mesh: tuple[int, ...]):
        self._parallel_manager = JaxParallel(math.prod(device_mesh), self._device)

    def where(self, cond: jax.Array, input1: jax.Array, input2: jax.Array) -> jax.Array:
        return ops.where(cond, input1, input2)

    def topk(self, input: jax.Array, k: int) -> tuple[jax.Array, jax.Array]:
        return jax.lax.top_k(input, k)

    def softmax(self, input: jax.Array, dim: int = -1) -> jax.Array:
        # TODO: dim can be Sequence[int] as well. Should work
        # for all backends.
        return ops.softmax(input, axis=dim)

    def multinomial(self, probs, num_samples, replacement=True):
        """
        Faster JAX implementation of multinomial sampling.

        Args:
            key: JAX PRNG key
            input: 1D or 2D array of probabilities
            num_samples: number of samples to draw
            replacement: whether to sample with replacement
        """
        input = jax.numpy.asarray(probs)
        if input.ndim == 1:
            input = input[None, :]
            squeeze_result = True
        else:
            squeeze_result = False

        # Normalize probabilities
        input = input / jax.numpy.sum(input, axis=-1, keepdims=True)

        if replacement:
            # Use categorical directly - much faster than choice
            samples = jax.random.categorical(
                self.prng_key,
                jax.numpy.log(jax.numpy.maximum(input, 1e-37)),  # avoid log(0)
                shape=(input.shape[0], num_samples),
            )
        else:
            # For without replacement, use Gumbel-max trick
            # This is much faster than using choice
            z = -jax.numpy.log(
                -jax.numpy.log(
                    jax.random.uniform(
                        self.prng_key,
                        shape=(input.shape[0], input.shape[1], num_samples),
                    )
                )
            )
            # Add log probabilities for Gumbel-max trick
            z = z + jax.numpy.log(jax.numpy.maximum(input, 1e-37))[..., None]
            # Get top k indices
            samples = jax.numpy.argsort(-z, axis=1)[:, :num_samples]

        # Update prng_key.
        self.prng_key, _ = jax.random.split(self.prng_key)

        if squeeze_result:
            samples = jax.numpy.squeeze(samples, axis=0)

        return samples

    def cat(
        self, inputs: tuple[jax.Array, ...] | list[jax.Array], dim: int = 0
    ) -> jax.Array:
        return ops.concat(*inputs, axis=dim)
