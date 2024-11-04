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
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Any, Generic, overload

from .. import core
from ..core import DataType
from . import utils
from .parallel import Parallel

__all__ = ["Backend"]


class Backend(ABC, Generic[DataType]):
    """Base class for backend implementations in the Mithril library."""

    type = ""
    device_type = None
    supported_precisions = [16, 32, 64]
    is_installed = True
    _device: str
    _precision: int
    fn_dict: dict[str, Callable]
    primitive_function_dict: dict[str, Callable]
    registered_primitives: dict[str, Callable]
    array_creation_funcs: list[str]
    primitive_fn_path: str

    def __init__(self, precision: int = 32, device: str = "cpu") -> None:
        # Check if given precision is a valid one.
        if self.precision not in self.supported_precisions:
            raise Exception(
                f"'{self.precision}' bits precision is not available!"
                " Available precisions: '{self.supported_precisions}'"
            )

        # Initialize epsilon constants according to given precision.
        # for key, value in core.epsilon_table[f"float{self.precision}"].items():
        #     setattr(self, key, value)

    @property
    def precision(self):
        return self._precision

    @property
    def device(self):
        return self._device

    @property
    def inf(self):
        raise NotImplementedError("inf is not implemented")

    @property
    def is_manualgrad(self):
        raise NotImplementedError("is_manualgrad is not implemented")

    def get_backend_array_type(self):  # noqa: B902
        raise NotImplementedError("get_backend_array_type is not implemented")

    @staticmethod
    def register_primitive(fn: Callable) -> None:
        raise NotImplementedError("register_primitive is not implemented!")

    @abstractmethod
    def set_seed(self, seed: int):
        raise NotImplementedError(
            "set_seed function must be overriden for every backend individually!"
        )

    def to_device(self, data: DataType, device: str, asynchronous: bool = True):
        raise RuntimeError("Backend does not support to_device method!")

    def block_until_ready(self, data: DataType):
        raise RuntimeError("Backend does not support block_until_ready method!")

    def empty_cache(self):  # noqa: B027
        pass
        # print("Warning: empty_cache is not supported!")

    @abstractmethod
    def _init_dtypes(self):
        raise NotImplementedError("_init_dtypes is not implemeted!")

    def _initialize_attributes(self):
        self.int16 = None
        self.float16 = None
        self.int32 = None
        self.float32 = None
        self.int = None
        self.float = None
        self.int64 = None
        self.float64 = None
        self.seed = 10  # Can be set any integer.
        self._init_dtypes()

        attrs = dir(self)

        for fn_key, fn in self.fn_dict.items():
            if fn_key in attrs:
                fn_key = f"_{fn_key}_impl"
            setattr(self, fn_key, fn)

    def cast(self, value: Any) -> Any:
        # Simply casts given value to the backend's precision.
        # If type of value is not int or float, returns the
        # value as is.
        if isinstance(value, bool):
            return value
        elif isinstance(value, int | float):
            return self.array(value).item()  # type: ignore
        elif isinstance(value, tuple):
            return tuple(self.cast(item) for item in value)
        elif isinstance(value, list):
            return [self.cast(item) for item in value]

        return value

    def __del__(self):
        self.empty_cache()

    def zeros(self, *shape: int, dtype: core.dtype | None = None) -> DataType:
        """Returns a new backend array on speficied device filled with zeros.

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be variable number of int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """

        _shape = utils.process_shape(shape)
        return self._zeros_impl(_shape, dtype=dtype)  # type: ignore

    def ones(self, *shape: int, dtype: core.dtype | None = None) -> DataType:
        """Returns a new backend array on speficied device filled with ones.

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """

        _shape = utils.process_shape(shape)
        return self._ones_impl(_shape, dtype=dtype)  # type: ignore

    def ones_like(self, array, *, dtype: core.dtype | None = None) -> DataType:
        """Returns a new backend array filled with ones, with the same size,
        same dtype and same device with the given array.

        Parameters
        ----------
        array : array_like
            Source array
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """

        return self._ones_like_impl(array, dtype=dtype)  # type: ignore

    def zeros_like(self, array, *, dtype: core.dtype | None = None) -> DataType:
        """Returns a new backend array filled with zeros, with the same size,
        same dtype and same device with the given array.

        Parameters
        ----------
        array : array_like
            Source array

        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        return self._zeros_like_impl(array, dtype=dtype)  # type: ignore

    @overload
    def arange(self, stop: int, *, dtype: core.dtype | None = None) -> DataType: ...

    @overload
    def arange(
        self, start: int, stop: int, *, dtype: core.dtype | None = None
    ) -> DataType: ...

    @overload
    def arange(
        self, start: int, stop: int, step: int, *, dtype: core.dtype | None = None
    ) -> DataType: ...

    def arange(self, *args, **kwargs) -> DataType:
        if len(args) == 0:
            raise RuntimeError(
                "arange() missing 1 required positional argument: 'stop'"
            )
        elif len(args) == 1:
            return self._arange_impl(0, args[0], 1, **kwargs)  # type: ignore
        elif len(args) == 2:
            if args[0] >= args[1]:
                return self.array([])

            return self._arange_impl(args[0], args[1], 1, **kwargs)  # type: ignore
        elif len(args) == 3:
            return self._arange_impl(args[0], args[1], args[2], **kwargs)  # type: ignore
        else:
            raise RuntimeError(
                "arange() accepts 1 to 3 positional arguments,"
                " but `f{len(args)}` were provided"
            )

    def rand_uniform(
        self, *shape: int | tuple[int, ...] | list[int], dtype: core.dtype | None = None
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._rand_uniform_impl(_shape)  # type: ignore

    def flatten(
        self, array: DataType, start_dim: int = 0, end_dim: int = -1
    ) -> DataType:
        """Flattens the given multi-dimensional array into a one-dimensional array.
        If start_dim or end_dim is provided, only the desired dimensions
        will be flattened.


        Parameters
        ----------
        array : int or tuple of ints
            The input multi-dimensional array to be flattened

        start_dim : int, optional
            The starting dimension to begin flattening, by default 0.

        end_dim : int, optional
            The ending dimension to stop flattening, by default -1.

        Returns
        -------
        DataType
            The flattened one-dimensional array.
        """

        return self._flatten_impl(array, start_dim=start_dim, end_dim=end_dim)  # type: ignore

    def abs(self, array: DataType) -> DataType:
        """
        Computes the element-wise absolute values of the given array.

        Parameters
        ----------
        array : DataType
            The input array for which absolute values will be calculated.

        Returns
        -------
        DataType
            An array of the same shape as the input, containing the absolute values.
        """
        return self._abs_impl(array)  # type: ignore

    def log(self, array: DataType) -> DataType:
        """
        Computes the element-wise natural logarithm values of the given array.

        Parameters
        ----------
        array : DataType
            The input array for which natural logarithm values will be calculated.

        Returns
        -------
        DataType
            An array of the same shape as the input.
        """
        return self._log_impl(array)  # type: ignore

    def sin(self, array: DataType) -> DataType:
        """
        Computes the element-wise sine values of the given array.

        Parameters
        ----------
        array : DataType
            The input array for which sine values will be calculated.

        Returns
        -------
        DataType
            An array of the same shape as the input, containing the sine values.
        """
        return self._sin_impl(array)  # type: ignore

    def cos(self, array: DataType) -> DataType:
        """
        Computes the element-wise cosine values of the given array.

        Parameters
        ----------
        array : DataType
            The input array for which cosine values will be calculated.

        Returns
        -------
        DataType
            An array of the same shape as the input, containing the cosine values.
        """
        return self._cos_impl(array)  # type: ignore

    def sign(self, array: DataType) -> DataType:
        """
        Computes the element-wise sign values of the given array.

        Parameters
        ----------
        array : DataType
            The input array for which sign values will be calculated.

        Returns
        -------
        DataType
            An array of the same shape as the input, containing the sign values.
        """
        return self._sign_impl(array)  # type: ignore

    def relu(self, array: DataType) -> DataType:
        """
        Applies the Rectified Linear Unit (ReLU) activation function element-wise
        to the input array.

        Parameters
        ----------
        array : DataType
            Input array on which the ReLU activation is applied.

        Returns
        -------
        DataType
            An array with the same shape as the input, where each element is the result
            of applying the ReLU activation function to the corresponding element of
            the input array.

        """
        return self._relu_impl(array)  # type: ignore

    def leaky_relu(self, array: DataType, slope: DataType) -> DataType:
        """
        Applies the Leaky Rectified Linear Unit (ReLU) activation function
        element-wise to the input array.

        Parameters
        ----------
        array : DataType
            Input array on which the Leaky ReLU activation is applied.

        Returns
        -------
        DataType
            An array with the same shape as the input, where each element is the result
            of applying the Leaky ReLU activation function to the corresponding element
            of the input array.

        """
        return self._leaky_relu_impl(array, slope)  # type: ignore

    def tanh(self, array: DataType) -> DataType:
        """
        Applies the Hyperbolic Tangent (tanh) function element-wise to the input array.

        Parameters
        ----------
        array : DataType
            Input array on which the tanh activation is applied.

        Returns
        -------
        DataType
            An array with the same shape as the input, where each element is the result
            of applying the tanh activation function to the corresponding element
            of the input array.

        """
        return self._tanh_impl(array)  # type: ignore

    def sigmoid(self, array: DataType) -> DataType:
        """
        Applies the Sigmoid activation function element-wise to the input array.

        Parameters
        ----------
        array : DataType
            Input array on which the Sigmoid activation is applied.

        Returns
        -------
        DataType
            An array with the same shape as the input, where each element is the result
            of applying the Sigmoid activation function to the corresponding element
            of the input array.

        """
        return self._sigmoid_impl(array)  # type: ignore

    def softplus(self, array: DataType) -> DataType:
        """
        Applies the Softplus activation function element-wise to the input array.

        Parameters
        ----------
        array : DataType
            Input array on which the Softplus activation is applied.

        Returns
        -------
        DataType
            An array with the same shape as the input, where each element is the result
            of applying the Softplus activation function to the corresponding element
            of the input array.

        """
        return self._softplus_impl(array)  # type: ignore

    def softmax(self, array: DataType, dim: int = -1) -> DataType:
        """
        Compute the softmax of the input array along the specified dimension.

        Parameters:
        array (DataType): The input array for which to compute the softmax.
        dim (int or tuple[int, ...], optional):
            The dimension or dimensions along which to compute the softmax.
            Defaults to -1, which indicates the last dimension.

        Returns:
        DataType: The array with softmax applied along the specified dimension.

        Raises:
        NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Implement softmax method!")

    def isnan(self, array: DataType) -> DataType:
        """
        Checks for NaN (Not a Number) values in the input array.

        Parameters
        ----------
        array : DataType
            Input array to check for NaN values.

        Returns
        -------
        DataType
            Boolean array with the same shape as the input, where each element is True
        if the corresponding element in the input array is NaN, and False otherwise.
        """
        return self._isnan_impl(array)  # type: ignore

    def array(self, data: Any, *, dtype: core.dtype | None = None) -> DataType:
        """Returns a backend array on speficied device by copying `data`.

        Parameters
        ----------
        data : DataType
            Can be tuple, list or Numpy ndarray.
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Returns a backend array
        """
        return self._array_impl(data, dtype=dtype)  # type: ignore

    def stop_gradient(self, data: DataType) -> DataType:
        """Stops gradients from being computed. This method works like an identity
        function and does not change values.


        Parameters
        ----------
        data : array_like
            Must be a backend array

        Returns
        -------
        DataType
            Returns a backend array
        """

        if not hasattr(self, "_stop_gradient_impl"):
            raise NotImplementedError(
                "Backend '{self.type}' does not support 'stop_gradient' for now."
            )

        return self._stop_gradient_impl(data)  # type: ignore

    def randn(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | None = None,
        **kwargs,
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._randn_impl(  # type: ignore
            *_shape, dtype=dtype, **kwargs
        )

    def rand(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
        **kwargs,
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._rand_uniform_impl(  # type: ignore
            *shape, dtype=dtype, device_mesh=device_mesh, **kwargs
        )

    def jit(self, fn: Callable) -> Callable:
        return self._jit_impl(fn)  # type: ignore

    def tranpose(self, data: DataType) -> DataType:
        raise NotImplementedError()

    def topk(
        self, input: core.DataType, k: int
    ) -> tuple[core.DataType, core.DataType | None]:
        raise NotImplementedError("topk is not implemented!")

    def where(
        self, cond: core.DataType, input1: core.DataType, input2: core.DataType
    ) -> core.DataType:
        raise NotImplementedError("where is not implemented!")

    def multinomial(
        self,
        probs: core.DataType,
        num_samples: int,
        replacement: bool = False,
    ) -> core.DataType:
        raise NotImplementedError("multinomial is not implemented!")

    def cat(
        self, inputs: tuple[core.DataType, ...] | list[core.DataType], dim: int = 0
    ) -> core.DataType:
        raise NotImplementedError("cat is not implemented!")


class ParallelBackend(Backend[DataType]):
    def __init__(self, device_mesh: tuple[int, ...] | None) -> None:
        assert (
            isinstance(device_mesh, tuple) or device_mesh is None
        ), "device_mesh must be a tuple or None."
        super().__init__()

        self._raw_device_mesh = device_mesh
        self.n_devices = math.prod(device_mesh) if device_mesh is not None else 1
        self._parallel_manager: Parallel | None

    def zeros(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
    ) -> DataType:
        """Returns a new backend array on speficied device filled with zeros.

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be variable number of int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None
        device_mesh : tuple[int, ...], optional
            The device mesh for parallelization, by default None

        Returns
        -------
        DataType
            Backend array
        """

        _shape = utils.process_shape(shape)
        return self._zeros_impl(_shape, dtype=dtype, device_mesh=device_mesh)  # type: ignore

    def zeros_like(
        self,
        array,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
    ) -> DataType:
        """Returns a new backend array filled with zeros, with the same size,
        same dtype and same device with the given array.

        Parameters
        ----------
        array : array_like
            Source array

        dtype : mithril.dtype, optional
            Desired data type, by default None

        device_mesh : tuple[int, ...], optional
            The device mesh for parallelization, by default None

        Returns
        -------
        DataType
            Backend array
        """
        return self._zeros_like_impl(array, dtype=dtype, device_mesh=device_mesh)  # type: ignore

    def ones(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | str | None = None,
        device_mesh: tuple[int, ...] | None = None,
    ) -> DataType:
        """Returns a new backend array on speficied device filled with ones.

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints

        dtype : mithril.dtype, optional
            Desired data type, by default None

        device_mesh : tuple[int, ...], optional
            The device mesh for parallelization, by default None

        Returns
        -------
        DataType
            Backend array
        """

        _shape = utils.process_shape(shape)
        return self._ones_impl(_shape, dtype=dtype, device_mesh=device_mesh)  # type: ignore

    def ones_like(
        self,
        array: DataType,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
    ) -> DataType:
        """Returns a new backend array filled with ones, with the same size,
        same dtype and same device with the given array.

        Parameters
        ----------
        array : array_like
            Source array

        dtype : mithril.dtype, optional
            Desired data type, by default None

        device_mesh : tuple[int, ...], optional
            The device mesh for parallelization, by default None

        Returns
        -------
        DataType
            Backend array
        """

        return self._ones_like_impl(array, dtype=dtype, device_mesh=device_mesh)  # type: ignore

    def array(
        self,
        data,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
    ) -> DataType:
        """Returns a backend array on speficied device by copying `data`.


        Parameters
        ----------
        data : DataType
            Can be tuple, list or Numpy ndarray.

        dtype : mithril.dtype, optional
            Desired data type, by default None

        device_mesh : tuple[int, ...], optional
            The device mesh for parallelization, by default None

        Returns
        -------
        DataType
            Returns a backend array
        """
        return self._array_impl(data, dtype=dtype, device_mesh=device_mesh)  # type: ignore

    @overload  # type: ignore[override]
    def arange(
        self,
        stop: int,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None,
    ) -> DataType: ...

    @overload
    def arange(  # type: ignore[override]
        self,
        start: int,
        stop: int,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None,
    ) -> DataType: ...

    @overload
    def arange(  # type: ignore[override]
        self,
        start: int,
        stop: int,
        step: int,
        *,
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None,
    ) -> DataType: ...

    def arange(  # type: ignore[override]
        self, *args, device_mesh: tuple[int, ...] | None = None, **kwargs
    ) -> DataType:
        """Generate an array of evenly spaced values within a specified range."""
        if len(args) == 0:
            raise RuntimeError(
                "arange() missing 1 required positional argument: 'stop'"
            )
        elif len(args) == 1:
            return self._arange_impl(0, args[0], 1, device_mesh=device_mesh, **kwargs)  # type: ignore
        elif len(args) == 2:
            if args[0] >= args[1]:
                return self.array([])

            return self._arange_impl(  # type: ignore
                args[0], args[1], 1, device_mesh=device_mesh, **kwargs
            )
        elif len(args) == 3:
            return self._arange_impl(  # type: ignore
                args[0], args[1], args[2], device_mesh=device_mesh, **kwargs
            )
        else:
            raise RuntimeError(
                "arange() accepts 1 to 3 positional arguments,"
                " but `f{len(args)}` were provided"
            )

    def randn(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
        **kwargs,
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._randn_impl(  # type: ignore
            *_shape, dtype=dtype, device_mesh=device_mesh, **kwargs
        )

    def rand(
        self,
        *shape: int | tuple[int, ...] | list[int],
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
        **kwargs,
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._rand_uniform_impl(  # type: ignore
            *_shape, dtype=dtype, device_mesh=device_mesh, **kwargs
        )

    def randint(
        self,
        low: int,
        high: int,
        shape: tuple[int, ...],
        dtype: core.dtype | None = None,
        device_mesh: tuple[int, ...] | None = None,
        **kwargs,
    ) -> DataType:
        """Returns a new backend array filled with random samples between [0, 1).

        Parameters
        ----------
        shape : int or tuple of ints
            Shape of the new data, could be int or tuple of ints
        dtype : mithril.dtype, optional
            Desired data type, by default None

        Returns
        -------
        DataType
            Backend array
        """
        _shape = utils.process_shape(shape)
        return self._randint_impl(  # type: ignore
            low, high, _shape, dtype=dtype, device_mesh=device_mesh, **kwargs
        )

    def _register_callable(
        self, fn: Callable | partial, fn_name: str, jit: bool
    ) -> None:
        raise NotImplementedError()

    def _run_callable(self, *primals, fn_name: str):
        raise NotImplementedError()

    def _create_parallel(self, device_mesh: tuple[int, ...]) -> Parallel:
        raise NotImplementedError(
            f"{self.type.capitalize()} backend does not support parallelization!"
        )


class NotInstalledBackendMock:
    is_installed = False

    def __init__(self, *args, **kwargs) -> None:
        raise RuntimeError(
            "Backend is not installed. Please install the backend to use it."
        )
