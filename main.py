import src.nuclear_icebreaker.config as config
import src.nuclear_icebreaker.external.panel as pnl

# from src.nuclear_icebreaker.external.panel import Panel as pnl
# from src.nuclear_icebreaker import config as cfg

panels = [
    pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, 0),  # Side panels
    pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, 0),
    pnl.Panel(25.8, 31, 0.2, False, 90),  # Front panel
]

for panel in panels:
    # Example velocity and kinematic viscosity
    print(
        f"Panel Area: {panel.area} m², Roughness: {panel.roughness}, "
        f"Reynolds Number: {panel.reynolds_number(5.0, config.WATER_KINEMATIC_VISCOSITY)}"
    )
