"""
Docstring for ship.external.panel
This module defines the Panel class used in the ship simulation.
"""

class Panel:
    height: float  # in meters
    length: float  # in meters
    area: float  # in square meters
    roughness: float  # meters
    angle: float  # in degrees
    parallel_to_flow: bool
    underwater: bool
    reynolds_number: float

    def __init__(self, height, length, roughness,parallel_to_flow, underwater, angle):
        self.height = height
        self.length = length
        self.area = height * length
        self.roughness = roughness
        self.parallel_to_flow = parallel_to_flow
        self.underwater = underwater
        self.angle = angle

        # PLACEHOLDER CODE, does not account if perpendicular or parallel to flow
    def calculate_reynolds_number(self, velocity: float, kinematic_viscosity: float) -> float:
        """Calculate the Reynolds number for the panel."""
        characteristic_length = self.length if self.parallel_to_flow else self.height
        return (velocity * characteristic_length) / kinematic_viscosity

