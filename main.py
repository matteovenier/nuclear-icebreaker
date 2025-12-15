import src.nuclear_icebreaker.config as config
import src.nuclear_icebreaker.external.panel as pnl
import src.nuclear_icebreaker.external.resistance as res
import numpy as np

# from src.nuclear_icebreaker.external.panel import Panel as pnl
# from src.nuclear_icebreaker import config as cfg

panels = [
    # pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, False, 0),  # Side panels
    # pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, False, 0),
    pnl.Panel(25.8+3.7+10, 34 , 0.2, False, False,0),  # Front panel
    pnl.Panel(10, 173.3, 0.005, True, True, 0.2),  # Side panels underwater
    pnl.Panel(10, 173.3, 0.005, True, True, 0.2),
    pnl.Panel(34, 173.3, 0.005, True, True,0.2)  # Bottom panel underwater
]

for panel in panels:
    # Example velocity and kinematic viscosity
    print(
        f"Panel {panels.index(panel)}, Roughness: {panel.roughness}, "
        f"Reynolds Number: {panel.reynolds_number(5.0*config.KNOT_TO_MPS)}"
    )

pow =  config.REACTOR_EXAMPLE_POWER_MW * 1e6 * config.PROPELLER_EFFICIENCY  # Convert MW to W
res.calculate_resistance(panels, starting_speed=0.3, given_power=pow)
