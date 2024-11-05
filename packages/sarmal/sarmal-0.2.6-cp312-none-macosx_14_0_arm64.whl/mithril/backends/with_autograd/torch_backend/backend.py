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
import torch
from torch._C import Generator
from torch.distributed._tensor import DTensor

from ...backend import ParallelBackend
from . import common_functions, ops, utils
from .parallel import TorchParallel

__all__ = ["TorchBackend"]


class TorchBackend(ParallelBackend[torch.Tensor]):
    """TorchBackend: A backend implementation for the Mithril library.

    This backend provides integration with PyTorch.

    Parameters
    ----------
    device: str, optional
        The device on which to perform computations, default is "cpu".
    precision: int, optional
        The precision of the tensors, either 32 or 64, default is 32.
    """

    type = "torch"
    registered_primitives = {}
    primitive_fn_path = "mithril.backends.with_autograd.torch_backend.ops"

    def __init__(
        self, device: str = "cpu", precision: int = 32, device_mesh=None
    ) -> None:
        self._device = device
        self._precision = precision
        self._parallel_manager: TorchParallel | None = None

        utils.get_device(device)  # Check if device is valid

        super().__init__(device_mesh=device_mesh)
        if device_mesh is not None:
            self._create_parallel(device_mesh)

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
        torch.random.manual_seed(self.seed)

    @property
    def is_manualgrad(self):
        return False

    @property
    def inf(self):
        return torch.inf

    @property
    def DataType(self):  # noqa: N802
        return utils.ArrayType

    @property
    def device(self):
        return utils.get_device(self._device)

    def get_backend_array_type(self):
        return torch.Tensor

    @staticmethod
    def register_primitive(fn: Callable) -> None:
        TorchBackend.registered_primitives[fn.__name__] = fn

    @staticmethod
    def get_available_devices() -> list[str]:
        """Static method to get a list of available devices.

        Parameters
        ----------
        list[str]
            List of available devices.
        """

        return utils.get_available_devices()

    def set_seed(self, seed: int):
        self.seed = seed
        torch.random.manual_seed(seed)

    def to_device(self, data: torch.Tensor, device: str, asynchronous: bool = False):
        """Move data to the specified device.

        Parameters
        ----------
        data: torch.Tensor
            The data to be moved to the specified device.
        device: str
            The target device for the data.
        """
        return data.to(device)

    # def block_until_ready(self, data: ArrayType | None = None) -> None:
    #     getattr(torch, f"{self.device_type.lower()}").synchronize()

    def empty_cache(self) -> None:
        """Empty the cache on the device."""
        if self._device in ["MPS", "CUDA"]:
            getattr(torch, f"{self._device.lower()}").empty_cache()
        else:
            pass
            # print(f"Warning: empty_cache is not implemented for {self.device_type}")

    def _creation_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for PyTorch tensor creation functions.

        Parameters
        ----------
        fn: Callable
            The original tensor creation function.

        Returns
        -------
        Callable
            A wrapped function that creates tensors with specified dtype and device.

        Notes
        -----
        This wrapper ensures that tensors are created with the correct dtype
        and on the specified device.
        """

        array_creation_fn = partial(
            utils.creation_fn_wrapper_inner,
            fn=fn,
            device=self._device,
            precision=self.precision,
        )
        array_creation_fn = partial(self._parallelize, fn=array_creation_fn)

        return array_creation_fn

    def _conversion_fn_wrapper(self, fn: Callable) -> Callable:
        """
        Wrapper for PyTorch tensor conversion functions.

        Parameters
        ----------
        fn: Callable
            The original tensor conversion function.

        Returns
        -------
        Callable
            A wrapped function that converts tensors with specified dtype and device.

        Notes
        -----
        Wrapper handles the conversion of tensors between different dtypes and devices.
        """

        array_conversion_fn = partial(
            utils.conversion_fn_wrapper_inner,
            fn=fn,
            device=self._device,
            precision=self.precision,
        )
        array_conversion_fn = partial(self._parallelize, fn=array_conversion_fn)

        return array_conversion_fn

    def _parallelize(
        self, *args, fn: Callable, device_mesh, **kwargs
    ) -> DTensor | torch.Tensor:
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
            Returns tensor parallelized across the specified device mesh.
        """
        tensor: torch.Tensor = fn(*args, **kwargs)
        if self._parallel_manager is None:
            # TODO: raise device_mesh should be None
            return tensor

        return self._parallel_manager.parallelize(
            tensor, self.base_device_mesh, device_mesh
        )

    def _register_callable(
        self, fn: Callable | partial, fn_name: str, jit: bool = False
    ):
        """
        Register a callable function with the backend.

        Parameters
        ----------
        fn: Callable
            The function to be registered.
        """
        assert (
            self._parallel_manager is not None
        ), "Parallel manager is not initialized!"

        fn_name = str(id(self)) + fn_name
        self._parallel_manager.register_callable(
            fn, fn_name, self.base_device_mesh, jit
        )

    def atleast_1d(self, *args) -> torch.Tensor | list[torch.Tensor]:
        if len(args) == 1:
            return torch.atleast_1d(self.array(args[0]))
        else:
            return [torch.atleast_1d(arr) for arr in args]

    def to_numpy(self, arr: torch.Tensor) -> np.ndarray:
        return arr.detach().cpu().numpy()

    def unique(self, *args, **kwargs) -> torch.Tensor:
        return torch.unique(*args, **kwargs)

    def jit(self, *args, **kwargs):
        backend = "inductor"
        if "mps" in self._device:
            backend = "aot_eager"
        return torch.compile(*args, backend=backend, **kwargs)

    def transpose(
        self, data: torch.Tensor, axis: tuple[int, ...] | list[int] | None = None
    ) -> torch.Tensor:
        if axis is None:
            axis = tuple(reversed(range(data.ndim)))

        return data.permute(axis)

    def _init_dtypes(self):
        for name, value in utils.dtype_map.items():
            setattr(self, name, value)

    def _create_parallel(self, device_mesh: tuple[int, ...]):
        assert isinstance(device_mesh, tuple), "Device mesh must be tuple or None!"
        assert isinstance(
            self._raw_device_mesh, tuple
        ), "Device mesh must be tuple or None!"

        self._parallel_manager = TorchParallel(
            self.n_devices, device=self._device.split(":")[0]
        )
        self.base_device_mesh = self._parallel_manager._init_device_mesh(
            self._raw_device_mesh
        )

    def _run_callable(self, *primals, fn_name: str):
        assert (
            self._parallel_manager is not None
        ), "Parallel manager is not initialized!"

        fn_name = str(id(self)) + fn_name
        return self._parallel_manager.run_callable(*primals, fn_name=fn_name)

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        # _parallel_manager is not picklable, not going to write it into pickle file
        # We can recreate it using the device mesh
        if "_parallel_manager" in state:
            del state["_parallel_manager"]
        return state

    def __setstate__(self, state) -> None:
        self.__dict__.update(state)
        self._init_dtypes()
        # Recreate the parallel manager
        if self._raw_device_mesh is not None:
            self._create_parallel(self._raw_device_mesh)
        else:
            self._parallel_manager = None

    def where(
        self, cond: torch.Tensor, input1: torch.Tensor, input2: torch.Tensor
    ) -> torch.Tensor:
        return ops.where(cond, input1, input2)

    def topk(self, input: torch.Tensor, k: int) -> tuple[torch.Tensor, torch.Tensor]:
        return torch.topk(input, k)  # TODO: Returns different tuple type???

    def softmax(self, input: torch.Tensor, dim: int = -1) -> torch.Tensor:
        return ops.softmax(input, axis=dim)

    def multinomial(
        self,
        probs: torch.Tensor,
        num_samples: int,
        replacement: bool = False,
        *,
        generator: Generator | None = None,
        out: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return torch.multinomial(
            probs, num_samples, replacement, generator=generator, out=out
        )

    def cat(
        self, inputs: tuple[torch.Tensor, ...] | list[torch.Tensor], dim: int = 0
    ) -> torch.Tensor:
        return ops.concat(*inputs, axis=dim)
