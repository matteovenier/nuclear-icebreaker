import src.nuclear_icebreaker.config as config
import src.nuclear_icebreaker.external.panel as pnl
import src.nuclear_icebreaker.external.resistance as res
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from multiprocessing import Pool
import os


# BEWARE: AI GENERATED CODE BELOW, may contain errors. Made for learning about parallelization.

def compute_speed(args):
    """Worker function: compute speed for a (power, ice_thickness) pair."""
    power, ice, panels = args
    pow = power * 1e6 * config.PROPELLER_EFFICIENCY  # Convert MW to W
    speed = res.calculate_resistance(panels, starting_speed=0.3, given_power=pow, ice_thickness=ice)
    return {
        "power_MW": power,
        "ice_thickness_m": ice,
        "speed_mps": speed,
    }


if __name__ == "__main__":
    # Create panels inside if __name__ block
    panels = [
        pnl.Panel(25.8 + 3.7 + 10, 34, 0.2, False, False, 0),  # Front panel
        pnl.Panel(10, 173.3, 0.005, True, True, 0.2),  # Side panels underwater
        pnl.Panel(10, 173.3, 0.005, True, True, 0.2),
        pnl.Panel(34, 173.3, 0.005, True, True, 0.2),  # Bottom panel underwater
    ]

    for panel in panels:
        print(
            f"Panel {panels.index(panel)}, Roughness: {panel.roughness}, "
            f"Reynolds Number: {panel.reynolds_number(5.0 * config.KNOT_TO_MPS)}"
        )

    powers = np.linspace(40, 80, 100)
    ice_thicknesses_m = np.linspace(0.5, 3.0, 100)

    # Generate all (power, ice, panels) tuples
    param_pairs = [(p, i, panels) for p in powers for i in ice_thicknesses_m]

    # Parallelize across CPU cores
    num_workers = os.cpu_count()  # Use all available CPU cores
    print(f"Using {num_workers} workers...")

    with Pool(num_workers) as pool:
        results = pool.map(compute_speed, param_pairs)

    print(f"Computed {len(results)} results")

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
            xaxis_title="Power (MW)",
            yaxis_title="Ice Thickness (m)",
            zaxis_title="Speed (m/s)",
        ),
        width=900,
        height=700,
    )
    fig3d.show()
