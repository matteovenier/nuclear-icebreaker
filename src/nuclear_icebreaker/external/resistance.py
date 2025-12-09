"""
Docstring for src.nuclear_icebreaker.external.resistance
Iterative loop for calculating ship resistance.
Starting speed with iterations until balance of thrust and resistance is achieved.

I need to calculate both fluid resistance and ice resistance in each loop iteration.
Resistance needs to be equal to the thrust provided by the propeller at the given speed.
So F res = F thrust = Power / Velocity
"""
from src.nuclear_icebreaker.config import WATER_DENSITY, WATER_KINEMATIC_VISCOSITY, AIR_DENSITY
import src.nuclear_icebreaker.external.panel as pnl

def calculate_resistance(panels, starting_speed: float, given_power: float):
    pass  # Placeholder for resistance calculation logic
    current_speed = starting_speed
    f_res = 0.0


    while f_res < (given_power * 1e6) / (current_speed-0.1):  # noqa: F405
        # Calculate fluid resistance from panels
        for panel in panels:
            reynolds_number = panel.reynolds_number(current_speed, WATER_KINEMATIC_VISCOSITY)
            panel.reynolds_number = reynolds_number  # Store Reynolds number in panel
            # Placeholder for fluid resistance calculation
            fluid_resistance = 0.5 * WATER_DENSITY * current_speed**2 * panel.area * 0.01  # Simplified drag formula

        # Placeholder for ice resistance calculation
        ice_resistance = 0.0  # This would be calculated based on ice conditions

        f_res = fluid_resistance + ice_resistance

        # Insert here ice resistance calculation

        if f_res < (given_power * 1e6) / current_speed:
            current_speed += 0.1  # Increment speed for next iteration

