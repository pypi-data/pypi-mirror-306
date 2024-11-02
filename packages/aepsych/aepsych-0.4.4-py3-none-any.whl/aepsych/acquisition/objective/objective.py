#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from typing import Optional

import torch
from aepsych.config import Config
from botorch.acquisition.objective import MCAcquisitionObjective
from torch import Tensor
from torch.distributions.normal import Normal


class AEPsychObjective(MCAcquisitionObjective):
    def inverse(self, samples: Tensor, X: Optional[Tensor] = None) -> Tensor:
        raise NotImplementedError


class ProbitObjective(AEPsychObjective):
    """Probit objective

    Transforms the input through the normal CDF (probit).
    """

    def forward(self, samples: Tensor, X: Optional[Tensor] = None) -> Tensor:
        """Evaluates the objective (normal CDF).

        Args:
            samples (Tensor): GP samples.
            X (Optional[Tensor], optional): ignored, here for compatibility
                with MCAcquisitionObjective.

        Returns:
            Tensor: [description]
        """
        return Normal(loc=0, scale=1).cdf(samples.squeeze(-1))

    def inverse(self, samples: Tensor, X: Optional[Tensor] = None) -> Tensor:
        """Evaluates the inverse of the objective (normal PPF).

        Args:
            samples (Tensor): GP samples.
            X (Optional[Tensor], optional): ignored, here for compatibility
                with MCAcquisitionObjective.

        Returns:
            Tensor: [description]
        """
        return Normal(loc=0, scale=1).icdf(samples.squeeze(-1))


class FloorLinkObjective(AEPsychObjective):
    """
    Wrapper for objectives to add a floor, when
    the probability is known not to go below it.
    """

    def __init__(self, floor: float=0.5) -> None:
        self.floor = floor
        super().__init__()

    def forward(self, samples: Tensor, X: Optional[Tensor] = None) -> Tensor:
        """Evaluates the objective for input x and floor f

        Args:
            samples (Tensor): GP samples.
            X (Optional[Tensor], optional): ignored, here for compatibility
                with MCAcquisitionObjective.

        Returns:
            Tensor: outcome probability.
        """
        return self.link(samples.squeeze(-1)) * (1 - self.floor) + self.floor

    def inverse(self, samples: Tensor, X: Optional[Tensor] = None) -> Tensor:
        """Evaluates the inverse of the objective.

        Args:
            samples (Tensor): GP samples.
            X (Optional[Tensor], optional): ignored, here for compatibility
                with MCAcquisitionObjective.

        Returns:
            Tensor: [description]
        """
        return self.inverse_link((samples - self.floor) / (1 - self.floor))

    def link(self, samples: Tensor) -> Tensor:
        raise NotImplementedError

    def inverse_link(self, samples: Tensor) -> Tensor:
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: Config) -> FloorLinkObjective:
        floor = config.getfloat(cls.__name__, "floor")
        return cls(floor=floor)


class FloorLogitObjective(FloorLinkObjective):
    """
    Logistic sigmoid (aka expit, aka logistic CDF),
    but with a floor so that its output is
    between floor and 1.0.
    """

    def link(self, samples: Tensor) -> Tensor:
        return torch.special.expit(samples)

    def inverse_link(self, samples: Tensor) -> Tensor:
        return torch.special.logit(samples)


class FloorGumbelObjective(FloorLinkObjective):
    """
    Gumbel CDF but with a floor so that its output
    is between floor and 1.0. Note that this is not
    the standard Gumbel distribution, but rather the
    left-skewed Gumbel that arises as the log of the Weibull
    distribution, e.g. Treutwein 1995, doi:10.1016/0042-6989(95)00016-X.
    """

    def link(self, samples: Tensor) -> Tensor:
        return torch.nan_to_num(
            -torch.special.expm1(-torch.exp(samples)), posinf=1.0, neginf=0.0
        )

    def inverse_link(self, samples: Tensor) -> Tensor:
        return torch.log(-torch.special.log1p(-samples))


class FloorProbitObjective(FloorLinkObjective):
    """
    Probit (aka Gaussian CDF), but with a floor
    so that its output is between floor and 1.0.
    """

    def link(self, samples: Tensor) -> Tensor:
        return Normal(0, 1).cdf(samples)

    def inverse_link(self, samples: Tensor) -> Tensor:
        return Normal(0, 1).icdf(samples)
