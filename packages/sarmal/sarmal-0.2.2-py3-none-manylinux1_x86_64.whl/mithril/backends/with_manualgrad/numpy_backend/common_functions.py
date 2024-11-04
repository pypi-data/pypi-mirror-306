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

import numpy as np

from .utils import accumulate_grads


def flatten(input: np.ndarray, *, start_dim: int = 0, end_dim: int = -1) -> np.ndarray:
    """Flattens a Numpy array akin to torch.flatten"""
    if end_dim == -1 or end_dim == len(input.shape):
        end_dim = len(input.shape) + 1
    end_dim = (
        int(end_dim == -1 or end_dim == len(input.shape)) * (len(input.shape) + 1)
        + int(end_dim != -1 and end_dim != len(input.shape)) * end_dim
    )
    prod = np.prod(input.shape[start_dim : end_dim + 1]).astype(int)
    shape = input.shape[:start_dim] + (prod,) + input.shape[end_dim + 1 :]
    return np.reshape(input, shape)


def relu(input: np.ndarray) -> np.ndarray:
    return np.maximum(np.array(0.0, dtype=input.dtype), input)


def leaky_relu(input: np.ndarray, slope: np.ndarray):
    return np.maximum(np.array(0.0, dtype=input.dtype), input) + slope * np.minimum(
        np.array(0.0, dtype=input.dtype), input
    )


def tanh(input: np.ndarray) -> np.ndarray:
    return np.tanh(input)


def sigmoid(input: np.ndarray) -> np.ndarray:
    # For numerical stability implement sigmoid with respect to the
    # sign of input.
    mask = input >= 0
    sig = np.zeros_like(input)
    sig[mask] = 1.0 / (1.0 + np.exp(-input[mask]))
    sig[~mask] = np.exp(input[~mask]) / (1.0 + np.exp(input[~mask]))
    return sig


# def softmax(input: np.ndarray, *, axis: int | tuple[int, ...] = -1) -> np.ndarray:
#     input_tensor = input - np.max(input, axis=axis, keepdims=True)
#     e = np.exp(input_tensor)
#     s = np.sum(e, axis=axis, keepdims=True)
#     return e / s


def softplus(input: np.ndarray) -> np.ndarray:
    # See: https://stackoverflow.com/questions/44230635/avoid-overflow-with-softplus-function-in-python
    return np.log1p(np.exp(-np.abs(input))) + np.maximum(input, 0.0)


def verify_shapes(
    inputs: tuple[np.ndarray, ...], idx: int, non_differentiables=None
) -> None:
    if idx >= len(inputs):
        raise Exception(f"Gradient is not defined for the input at index {idx}!")
    if non_differentiables is not None and idx in non_differentiables:
        raise Exception(f"Given key at index {idx} is not differentiable!")


fn_dict: dict[str, Callable] = {
    "abs": np.abs,
    "sin": np.sin,
    "cos": np.cos,
    "relu": relu,
    "leaky_relu": leaky_relu,
    "tanh": tanh,
    "sigmoid": sigmoid,
    "softplus": softplus,
    "squeeze": np.squeeze,
    "reshape": np.reshape,
    "dot": np.dot,
    "flatten": flatten,
    "sort": np.sort,
    "expand_dims": np.expand_dims,
    "stack": np.stack,
    "concatenate": np.concatenate,
    "pad": np.pad,
    "log": np.log,
    "isnan": np.isnan,
    "atleast_1d": np.atleast_1d,
    "accumulate_grads": accumulate_grads,
    "all": np.all,
    "any": np.any,
}

creation_fn_dict: dict[str, Callable] = {
    "zeros": np.zeros,
    "zeros_like": np.zeros_like,
    "ones_like": np.ones_like,
    "arange": np.arange,
    "rand_uniform": np.random.uniform,
    "ones": np.ones,
    "unique": np.unique,
    "eye": np.eye,
    "randint": np.random.randint,
}

conversion_fn_dict: dict[str, Callable] = {"array": np.array}
