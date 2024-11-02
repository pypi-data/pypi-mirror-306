#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


def handle_finish_strategy(self, request):
    self.strat.finish()
    return f"finished strategy {self.strat.name}"
