# SPDX-FileCopyrightText: 2024 Tjark Sievers
#
# SPDX-License-Identifier: MIT

"""
Parameter Classes
=================

Main class holding all the parameters for the calculation.

- :class:`Parameters<quant_met.parameters.Parameters>`

Classes holding the configuration for the Hamiltonians.

.. autosummary::
   :toctree: generated/parameters/

    Parameters  # noqa
    DressedGrapheneParameters
    GrapheneParameters
    OneBandParameters
    TwoBandParameters
    ThreeBandParameters
"""  # noqa: D205, D400

from .hamiltonians import (
    DressedGrapheneParameters,
    GenericParameters,
    GrapheneParameters,
    OneBandParameters,
    ThreeBandParameters,
    TwoBandParameters,
)
from .main import Parameters

__all__ = [
    "Parameters",
    "DressedGrapheneParameters",
    "GrapheneParameters",
    "OneBandParameters",
    "TwoBandParameters",
    "ThreeBandParameters",
    "GenericParameters",
]
