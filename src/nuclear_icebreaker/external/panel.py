"""
Docstring for ship.external.panel
This module defines the Panel class used in the ship simulation.
"""

import src.nuclear_icebreaker.config as config
import numpy as np


class Panel:
    height: float  # in meters
    length: float  # in meters
    area: float  # in square meters
    roughness: float  # meters
    k: float  # Form factor
    parallel_to_flow: bool
    underwater: bool
    reynolds_number: float
    Ct: float  # Friction coefficient

    def __init__(self, height, length, roughness, parallel_to_flow, underwater, k):
        self.height = height
        self.length = length
        self.area = height * length
        self.roughness = roughness
        self.parallel_to_flow = parallel_to_flow
        self.underwater = underwater
        self.k = k
        self.reynolds = 0.0

        # PLACEHOLDER CODE, does not account if perpendicular or parallel to flow

    def reynolds_number(self, velocity: float) -> float:
        """Calculate the Reynolds number for the panel."""
        characteristic_length = self.length
        if self.underwater:
            return (velocity * characteristic_length) / config.WATER_KINEMATIC_VISCOSITY
        else:
            return (velocity * characteristic_length) / config.AIR_KINEMATIC_VISCOSITY

    def friction_coefficient(self) -> float:
        """Calculate the friction coefficient for the panel."""
        Re = self.reynolds
        if self.parallel_to_flow and self.underwater:
            if Re < 1e6:
                # Not fully turbulent yet
                Cf = 0.075 / np.power(Re, 1 / 5)
            else:
                # Turbulent flow
                Cf = np.power(1.89 - 1.62 * np.log10(self.roughness / self.length), -2.5)
            self.Ct = Cf * (1 + self.k)
        else:
            # Simplified for other cases
            self.Ct = 2

        return self.Ct
