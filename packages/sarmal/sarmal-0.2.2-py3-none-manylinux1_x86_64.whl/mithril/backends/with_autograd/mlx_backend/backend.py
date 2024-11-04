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

import os
from collections.abc import Callable
from functools import partial

import mlx.core as mx
import numpy as np

from ...backend import Backend
from . import common_functions, ops, utils

__all__ = ["MlxBackend"]


class MlxBackend(Backend[mx.array]):
    type = "mlx"
    supported_precisions = [16, 32]
    registered_primitives = {}
    primitive_fn_path = "mithril.backends.with_autograd.mlx_backend.ops"

    def __init__(
        self, device: str = "cpu", precision: int = 32, eager_free: bool = False
    ) -> None:
        self._init_dtypes()

        if eager_free:
            os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"] = "platform"

        self._precision = precision
        self._device = device
        super().__init__()

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
        self._initialize_attributes()
        mx.random.seed(self.seed)

    @property
    def is_manualgrad(self):
        return False

    @property
    def inf(self):
        return mx.inf

    @property
    def device(self):
        utils.get_device(self._device)

    # TODO: This property is weird! Investigate why this property is used.

    def get_backend_array_type(self):
        return mx.array

    @staticmethod
    def get_available_devices():
        return utils.get_available_devices()

    @staticmethod
    def register_primitive(fn: Callable) -> None:
        MlxBackend.registered_primitives[fn.__name__] = fn

    def set_seed(self, seed: int):
        self.seed = seed
        mx.random.seed(seed)

    def to_device(
        self, data: mx.array, device: str, asynchronous: bool = True
    ) -> mx.array:
        return data

    def block_until_ready(self, data: mx.array):
        mx.eval(data)

    def _creation_fn_wrapper(self, fn: Callable) -> Callable:
        return partial(
            utils.creation_fn_wrapper,
            fn=fn,
            precision=self.precision,
        )

    def _conversion_fn_wrapper(self, fn: Callable) -> Callable:
        return partial(
            utils.conversion_fn_wrapper,
            fn=fn,
            precision=self.precision,
        )

    def randn(self, *shape, **kwargs):
        # TODO: To resemble the Jax implementation, we can set the seed using the key.
        return utils.creation_fn_wrapper(
            fn=mx.random.normal, shape=shape, precision=self.precision, **kwargs
        )

    def rand(self, *shape, **kwargs):
        # TODO: To resemble the Jax implementation, we can set the seed using the key.
        return utils.creation_fn_wrapper(
            fn=mx.random.uniform,
            shape=shape,
            precision=self.precision,
            **kwargs,
        )

    def randint(self, low, high, shape, **kwargs):
        # TODO: To resemble the Jax implementation, we can set the seed using the key.
        return utils.creation_fn_wrapper(
            fn=mx.random.randint,
            low=low,
            high=high,
            shape=shape,
            precision=self.precision,
            **kwargs,
        )

    def to_numpy(self, arr: mx.array) -> np.ndarray:
        return np.array(arr)

    def transpose(
        self, data: mx.array, axis: tuple[int, ...] | list[int] | None = None
    ) -> mx.array:
        if axis is None:
            return data.transpose()
        return data.transpose(axis)

    # make this dtypes automatically load from utils map!
    def _init_dtypes(self):
        for name, value in utils.dtype_map.items():
            setattr(self, name, value)

    def where(self, cond: mx.array, input1: mx.array, input2: mx.array) -> mx.array:
        return ops.where(cond, input1, input2)

    def topk(self, input: mx.array, k: int) -> tuple[mx.array, None]:
        return (-mx.sort(-mx.topk(input, k)), None)

    def softmax(self, input: mx.array, dim: int = -1) -> mx.array:
        # TODO: dim can be Sequence[int] as well. Should work
        # for all backends.
        return ops.softmax(input, axis=dim)

    def multinomial(self, probs, num_samples, replacement=True, seed=None):
        """
        MLX implementation matching torch.multinomial behavior.

        Args:
            probs: 1D or 2D array of probabilities.
                If 2D, each row is a distribution
            num_samples: number of samples to draw
            replacement: whether to sample with replacement
            seed: random seed

        Returns:
            1D or 2D array of indices sampled according to probs
        """
        if seed is not None:
            mx.random.seed(seed)

        probs = mx.array(probs)
        if probs.ndim == 1:
            probs = probs[None, :]  # Add batch dimension
            squeeze_result = True
        else:
            squeeze_result = False

        batch_size, num_categories = probs.shape

        # Handle zero probabilities like PyTorch
        zeros_mask = probs == 0
        probs = mx.where(zeros_mask, 0, probs)

        # Check if any row has all zeros
        valid_probs = mx.any(probs > 0, axis=1)

        # Normalize probabilities
        probs = probs / mx.maximum(mx.sum(probs, axis=1, keepdims=True), 1e-10)

        if replacement:
            # Generate uniform random numbers
            u = mx.random.uniform(shape=(batch_size, num_samples, 1))

            # Expand probs for comparison with random numbers
            expanded_probs = mx.expand_dims(probs, 1)  # [batch, 1, num_categories]
            cumsum = mx.cumsum(expanded_probs, axis=-1)  # [batch, 1, num_categories]

            # Compare random numbers with cumulative probabilities
            expanded_u = mx.broadcast_to(u, (batch_size, num_samples, num_categories))
            expanded_cumsum = mx.broadcast_to(
                cumsum, (batch_size, num_samples, num_categories)
            )

            # Count how many cumsum values are less than each random number
            samples = mx.sum(expanded_u > expanded_cumsum, axis=-1)

            # Handle invalid probability rows
            samples = mx.where(
                mx.expand_dims(valid_probs, -1), samples, mx.zeros_like(samples)
            )
        else:
            if num_samples > num_categories:
                raise ValueError(
                    f"Cannot sample {num_samples} samples without replacement "
                    f"from {num_categories} categories"
                )

            samples = mx.zeros((batch_size, num_samples), dtype=mx.int32)

            for b in range(batch_size):
                if not valid_probs[b]:
                    continue

                # Generate ordered random values for this batch
                ordered_u = mx.sort(mx.random.uniform(shape=(num_categories,)))

                # Convert probabilities to cumulative sum
                p = probs[b]
                cumsum = mx.cumsum(p)

                # Track used indices to avoid replacement
                used_mask = mx.zeros((num_categories,), dtype=mx.bool_)  # type: ignore
                batch_samples = mx.zeros((num_samples,), dtype=mx.int32)

                for i in range(num_samples):
                    u = ordered_u[i]

                    # Find index considering already used indices
                    valid_cumsum = mx.where(used_mask, 2.0, cumsum)
                    idx = mx.sum(u > valid_cumsum)

                    # Update used mask and store result
                    used_mask = mx.where(
                        mx.arange(num_categories) == idx, True, used_mask
                    )
                    batch_samples = mx.where(
                        mx.arange(num_samples) == i, idx, batch_samples
                    )

                # Update the samples array for this batch
                samples = mx.where(
                    mx.expand_dims(mx.arange(batch_size) == b, -1),  # type: ignore
                    mx.expand_dims(batch_samples, 0),
                    samples,
                )

        if squeeze_result:
            samples = mx.squeeze(samples, axis=0)

        return samples

    def cat(
        self, inputs: tuple[mx.array, ...] | list[mx.array], dim: int = 0
    ) -> mx.array:
        return ops.concat(*inputs, axis=dim)
