"""
Docstring for ship.config
This module contains configuration settings for the ship simulation.
"""

# Power parameters
REACTOR_EXAMPLE_POWER_MW = 60  # Reactor power in megawatts
PROPELLER_EFFICIENCY = 0.6  # Efficiency of the propeller

# Environmental Conditions
GRAVITY = 9.81  # m/s²
AIR_DENSITY = 1.225  # kg/m³
AIR_KINEMATIC_VISCOSITY = 1.5e-5  # m²/s (at 15°C)
WATER_DENSITY = 1025  # kg/m³ (seawater)
WATER_KINEMATIC_VISCOSITY = 1.83e-6  # m²/s (cold seawater)
ICE_THICKNESS = 1.5  # meters
ICE_COMPRESSIVE_STRENGTH = 15e6  # Pascals
FRICTIONAL_COEFFICIENT = 0.034  # Coefficient of friction between hull and ice
ICE_FLEXURAL_STRENGTH = 0.6e6  # Pascals

KNOT_TO_MPS = 0.5144  # Conversion factor from knots to meters per second

# Geometric Parameters
L_WL = 173.3  # Length at waterline in meters
B_WL = 34  # Beam at waterline in meters
FRAME_ANGLE = 30  # Frame angle in degrees
STEM_ANGLE = 15  # Stem angle in degrees
DRAFT = 10  # Draft in meters
CONTACT_FACTOR = 0.8  # Contact factor for ice interaction
