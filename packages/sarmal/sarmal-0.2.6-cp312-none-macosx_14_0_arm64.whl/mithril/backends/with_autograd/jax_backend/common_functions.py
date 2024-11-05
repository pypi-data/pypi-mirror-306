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

import jax
import jax.numpy as jnp

# TODO: Below setting will be removed. Precision settings
# will all be performed in corresponding backend object
# in backends.__init__.
jax.config.update("jax_enable_x64", True)


def flatten(input: jax.Array, *, start_dim: int = 0, end_dim: int = -1) -> jax.Array:
    """Flattens a JAX array akin to torch.flatten"""

    start_dim = (
        int(start_dim == -1) * len(input.shape) + int(start_dim != -1) * start_dim
    )
    end_dim = int(end_dim == -1) * len(input.shape) + int(end_dim != -1) * end_dim
    shape: tuple[int, ...] = (
        input.shape[:start_dim]
        + int(start_dim != end_dim) * (-1,)
        + input.shape[end_dim + 1 :]
    )

    if len(shape) == 0:
        shape = (1,)

    return jnp.reshape(input, shape)


fn_dict: dict[str, Callable] = {
    "grad": jax.grad,
    "value_and_grad": jax.value_and_grad,
    "vjp": jax.vjp,
    "vmap": jax.vmap,
    "jacrev": jax.jacrev,
    "jacfwd": jax.jacfwd,
    "jit": jax.jit,
    "stop_gradient": jax.lax.stop_gradient,
    "flatten": flatten,
    "jacobian": jax.jacobian,
    "squeeze": jnp.squeeze,
    "reshape": jnp.reshape,
    "expand_dims": jnp.expand_dims,
    "stack": jnp.stack,
    "concatenate": jnp.concatenate,
    "pad": jnp.pad,
    "rand_uniform": jax.random.uniform,
    "all": jnp.all,
    "any": jnp.any,
    "randint": jax.random.randint,
}


creation_fn_dict: dict[str, Callable] = {
    "ones_like": jnp.ones_like,
    "zeros_like": jnp.zeros_like,
    "ones": jnp.ones,
    "zeros": jnp.zeros,
    "arange": jnp.arange,
    "unique": jnp.unique,
}

conversion_fn_dict: dict[str, Callable] = {"array": jnp.array}
