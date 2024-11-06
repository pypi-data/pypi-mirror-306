#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from typing import Protocol, runtime_checkable

from torch import Tensor


@runtime_checkable
class ForwardFeatures(Protocol):
    def forward_features(self, x: Tensor) -> Tensor:
        """Extracts features.

        Args:
            x: Inputs with shape (B, C_in, H_in, W_in).

        Returns:
            Unpooled features with shape (B, C_out, H_out, W_out). H_out and W_out are
            usually >1.
        """
        ...


@runtime_checkable
class ForwardPool(Protocol):
    def forward_pool(self, x: Tensor) -> Tensor:
        """Pools features, should be called after `forward_features`.

        Args:
            x: Features with shape (B, C_in, H_in, W_in).

        Returns:
            Pooled features with shape (B, C_out, H_out, W_out). H_out and W_out depend
            on the pooling strategy but are usually 1.
        """
        ...


@runtime_checkable
class FeatureDim(Protocol):
    def feature_dim(self) -> int:
        """Returns the feature dimension of the extractor."""
        ...


@runtime_checkable
class FeatureExtractor(ForwardFeatures, ForwardPool, FeatureDim, Protocol): ...
