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

import mlx.core as mx
import mlx.nn as nn

ArrayType = mx.array


def flatten(input: mx.array, start_dim: int, end_dim: int) -> mx.array:
    return mx.flatten(input, start_axis=start_dim, end_axis=end_dim)


def buffer_fn(key):
    return key


fn_dict: dict[str, Callable] = {
    "abs": mx.abs,
    "sin": mx.sin,
    "cos": mx.cos,
    "tanh": mx.tanh,
    "relu": nn.relu,
    "leaky_relu": nn.leaky_relu,
    "softplus": nn.softplus,
    "grad": mx.grad,
    "value_and_grad": mx.value_and_grad,
    "stop_gradient": mx.stop_gradient,
    "vjp": mx.vjp,
    "vmap": mx.vmap,
    "jacrev": buffer_fn,
    "jacfwd": buffer_fn,
    "jit": buffer_fn,
    "jacobian": buffer_fn,
    "squeeze": mx.squeeze,
    "reshape": mx.reshape,
    "sort": mx.sort,
    "expand_dims": mx.expand_dims,
    "stack": mx.stack,
    "concatenate": mx.concatenate,
    "pad": mx.pad,
    "rand_uniform": mx.random.uniform,
    "log": mx.log,
    "isnan": mx.isnan,
    "atleast_1d": mx.atleast_1d,
    "atleast_2d": mx.atleast_2d,
    "flatten": flatten,
    "all": mx.all,
    "any": mx.any,
    "randint": mx.random.randint,
}


creation_fn_dict: dict[str, Callable] = {
    "zeros": mx.zeros,
    "zeros_like": mx.zeros_like,
    "ones_like": mx.ones_like,
    "ones": mx.ones,
    "arange": mx.arange,
}

conversion_fn_dict: dict[str, Callable] = {"array": mx.array}
