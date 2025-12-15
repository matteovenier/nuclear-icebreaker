import src.nuclear_icebreaker.config as config
import src.nuclear_icebreaker.external.panel as pnl
import src.nuclear_icebreaker.external.resistance as res

import plotly.express as px
import plotly.graph_objects as go

import numpy as np

from multiprocessing import Pool
import os


# from src.nuclear_icebreaker.external.panel import Panel as pnl
# from src.nuclear_icebreaker import config as cfg

panels = [
    # pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, False, 0),  # Side panels
    # pnl.Panel(25.8, 32 + 57 + 34, 0.2, True, False, 0),
    pnl.Panel(25.8 + 3.7 + 10, 34, 0.2, False, False, 0),  # Front panel
    pnl.Panel(10, 173.3, 0.005, True, True, 0.2),  # Side panels underwater
    pnl.Panel(10, 173.3, 0.005, True, True, 0.2),
    pnl.Panel(34, 173.3, 0.005, True, True, 0.2),  # Bottom panel underwater
]

for panel in panels:
    # Example velocity and kinematic viscosity
    print(
        f"Panel {panels.index(panel)}, Roughness: {panel.roughness}, "
        f"Reynolds Number: {panel.reynolds_number(5.0 * config.KNOT_TO_MPS)}"
    )

powers = np.linspace(40, 80, 1000)
ice_thicknesses_m = np.linspace(0.5, 3.0, 20)
results = []
for power in powers:
    for ice in ice_thicknesses_m:
        pow = power * 1e6 * config.PROPELLER_EFFICIENCY  # Convert MW to W
        speed = res.calculate_resistance(
            panels, starting_speed=0.3, given_power=pow, ice_thickness=ice
        )
        results.append(
            {
                "power_MW": power,
                "ice_thickness_m": ice,
                "speed_mps": speed,
            }
        )

# 2D: power (x) vs speed (y), with separate lines per ice thickness
fig2d = px.line(
    results,
    x="power_MW",
    y="speed_mps",
    color="ice_thickness_m",
    markers=True,
    title="Speed vs Power (colored by ice thickness)",
)
fig2d.show()

# 3D: power (x), ice thickness (y), speed (z)
fig3d = px.scatter_3d(
    results,
    x="power_MW",
    y="ice_thickness_m",
    z="speed_mps",
    color="ice_thickness_m",
    title="Speed vs Power vs Ice thickness",
)
fig3d.show()

# 3D Surface: reshape results into a grid
power_grid, ice_grid = np.meshgrid(powers, ice_thicknesses_m)
speed_grid = np.zeros_like(power_grid)

for i, ice in enumerate(ice_thicknesses_m):
    for j, power in enumerate(powers):
        # Find matching result
        for r in results:
            if abs(r["power_MW"] - power) < 1e-6 and abs(r["ice_thickness_m"] - ice) < 1e-6:
                speed_grid[i, j] = r["speed_mps"]
                break

fig3d = go.Figure(
    data=[
        go.Surface(
            x=power_grid,
            y=ice_grid,
            z=speed_grid,
            colorscale="Viridis",
            colorbar=dict(title="Speed (m/s)"),
        )
    ]
)

fig3d.update_layout(
    title="Speed vs Power vs Ice Thickness (Surface)",
    scene=dict(
        xaxis_title="Power (MW)", yaxis_title="Ice Thickness (m)", zaxis_title="Speed (m/s)"
    ),
    width=900,
    height=700,
)
fig3d.show()
