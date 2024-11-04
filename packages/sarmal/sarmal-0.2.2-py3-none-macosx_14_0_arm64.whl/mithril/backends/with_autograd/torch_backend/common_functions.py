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

import torch
from torch._functorch.apis import grad as torch_grad
from torch._functorch.apis import vmap as torch_vmap
from torch._functorch.eager_transforms import jacfwd as torch_jacfwd
from torch._functorch.eager_transforms import jacrev as torch_jacrev
from torch._functorch.eager_transforms import vjp as torch_vjp

fn_dict: dict[str, Callable] = {
    "abs": torch.abs,
    "sin": torch.sin,
    "cos": torch.cos,
    "relu": torch.relu,
    "leaky_relu": torch.nn.functional.leaky_relu,
    "tanh": torch.tanh,
    "sigmoid": torch.sigmoid,
    "softplus": torch.nn.functional.softplus,
    "grad": torch_grad,
    "vjp": torch_vjp,
    "vmap": torch_vmap,
    "jacrev": torch_jacrev,
    "jacfwd": torch_jacfwd,
    "squeeze": torch.squeeze,
    "reshape": torch.reshape,
    "dot": torch.dot,
    "flatten": torch.flatten,
    "sort": torch.sort,
    "expand_dims": torch.unsqueeze,
    "stack": torch.stack,
    "concatenate": torch.cat,
    "pad": torch.nn.functional.pad,
    "log": torch.log,
    "isnan": torch.isnan,
    "all": torch.all,
    "any": torch.any,
}

creation_fn_dict: dict[str, Callable] = {
    "rand_uniform": torch.rand,
    "zeros_like": torch.zeros_like,
    "ones": torch.ones,
    "zeros": torch.zeros,
    "ones_like": torch.ones_like,
    "arange": torch.arange,
    "randn": torch.randn,
    "rand": torch.rand,
    "randint": torch.randint,
}

conversion_fn_dict: dict[str, Callable] = {
    "array": torch.tensor,
}
