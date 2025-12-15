"""
Docstring for src.nuclear_icebreaker.external.resistance
Iterative loop for calculating ship resistance.
Starting speed with iterations until balance of thrust and resistance is achieved.

I need to calculate both fluid resistance and ice resistance in each loop iteration.
Resistance needs to be equal to the thrust provided by the propeller at the given speed.
So F res = F thrust = Power / Velocity
"""

from src.nuclear_icebreaker.config import   *
import src.nuclear_icebreaker.external.panel as pnl
import numpy as np


def calculate_resistance(panels, starting_speed: float, given_power: float):
    pass  # Placeholder for resistance calculation logic
    current_speed = starting_speed
    g = GRAVITY
    f_res = 0.0
    p_max = ICE_FLEXURAL_STRENGTH * 1/1.469 * np.power(WATER_DENSITY*g*ICE_THICKNESS**5, 1/4)

    while True:  # noqa: F405
        # Calculate fluid resistance from panels
        R_fluid = 0.0
        for panel in panels:
            reynolds_number = panel.reynolds_number(current_speed)
            panel.reynolds = reynolds_number  # Store Reynolds number in panel
            # Placeholder for fluid resistance calculation
            panel.friction_coefficient()
            R_fluid += 0.5 * (WATER_DENSITY if panel.underwater else AIR_DENSITY) * current_speed**2 * panel.area * panel.Ct




        # Ice resistance depends on effects of crushing, submersion, and bending

        # displacement = 0
        # phi = np.radians(FRAME_ANGLE)
        # beta = np.radians(STEM_ANGLE)
        # if displacement/np.cos(phi) <= ICE_THICKNESS:
        # # Triangular Crushing Area
        #     area = displacement**2 / (np.sin(phi) * np.cos(phi) * np.cos(beta))
        # # Quadrilateral Crushing Area
        # else:
        #     area = displacement**2 * np.cos(phi) * (2 - np.cos(phi) ** 2) / (np.sin(phi) * np.cos(beta))

        # force = area * ICE_COMPRESSIVE_STRENGTH * CONTACT_FACTOR
        # force_z = force * (np.cos(phi) - np.sin(phi)*FRICTIONAL_COEFFICIENT)

        # Ice resistance calculation parameters
        sigma_f = ICE_FLEXURAL_STRENGTH
        Hi = ICE_THICKNESS
        E = 5e+9  # Modulus of elasticity for ice in Pascals
        nu = 0.3  # Poisson's ratio for ice
        rho_w = WATER_DENSITY
        rho_i = 917  # Density of ice in kg/m³
        mu = FRICTIONAL_COEFFICIENT
        Bw1 = B_WL
        B = B_WL
        L = L_WL
        T = DRAFT
        V = current_speed
        alpha = np.radians(FRAME_ANGLE)
        phi1 = np.radians(STEM_ANGLE)
        Psi = np.arctan(T / (B / 2.0))

        # ---- Helper terms (readability) ----
        cosPsi = np.cos(Psi)
        sinAlpha = np.sin(alpha)

        # ---- R_B ----
        Rb_stiffness = Hi**1.5 / np.sqrt(E / (12.0 * (1.0 - nu**2) * rho_w * g))
        Rb_angle_term = (np.tan(Psi) + mu * np.cos(phi1)) / (cosPsi * sinAlpha)
        Rb_cos_correction = (1.0 + 1.0 / cosPsi)

        R_B = (37.0 / 64.0) * sigma_f * Bw1 * Rb_stiffness * Rb_angle_term * Rb_cos_correction

        # ---- R_C ----
        Rc_num = np.tan(phi1) + mu * (np.cos(phi1) / cosPsi)
        Rc_den = 1.0 - mu * (np.sin(phi1) / cosPsi)

        R_C = 0.5 * sigma_f * Hi**2 * (Rc_num / Rc_den)

        # ---- R_S ----
        Rs_buoyancy = (rho_w - rho_i) * g * Hi * B
        Rs_geom = T * (B + T) / (B + 2.0 * T)
        Rs_sqrt = np.sqrt(1.0 / (np.sin(phi1)**2) + 1.0 / (np.tan(alpha)**2))

        Rs_friction = mu * (
            0.7 * L
            - T / np.tan(phi1)
            - B / (4.0 * np.tan(alpha))
            + T * np.cos(phi1) * cosPsi * Rs_sqrt
        )

        R_S = Rs_buoyancy * (Rs_geom + Rs_friction)

        # ---- R_ice ----
        R_ice = (R_C + R_B) * (1.0 + 1.4 * V / np.sqrt(g * Hi)) + R_S * (1.0 + 9.4 * V / np.sqrt(g * L))

        f_res = R_fluid + R_ice
        if f_res < (given_power) / current_speed:
                current_speed += 0.1  # Increment speed for next iteration
        else:
            break

    print(f"At speed {current_speed:.2f} m/s, Total Resistance: {f_res:.2f} N")
    print(f" -- Fluid Resistance: {R_fluid:.2f} N, Ice Resistance: {R_ice:.2f} N")


