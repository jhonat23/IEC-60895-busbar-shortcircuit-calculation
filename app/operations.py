from math import pi, sqrt, log

# Constants
PI = pi # 3.1415...
Uo = 4 * PI * (10)**-7 # Vacuum permeability (H/m)
k = 1.35 # Value from R/X=0.3 relation in 4.3.1 of IEC 60909

# For calculate k1s factor
def k1s(busbar_width: int, busbar_thickness: int, phase_distance: int) -> float:
    """Returns factor k1s required for find equivalent phase distance"""
    # Equation constants
    bd = busbar_width / busbar_thickness
    ad = phase_distance / busbar_thickness
    adbd = ad / bd

    # Equation
    ka = (-(((ad + 1) / bd)**3 * log(((ad + 1)**2 + bd**2) / (ad + 1)**2)) + (2 * adbd**3 * log((ad**2 + bd**2) / ad**2)) - (((ad - 1) / bd)**3 * log(((ad - 1)**2 + bd**2) / (ad - 1)**2))) * ((ad * bd) / 6)

    return ka


# Functions
def magnetic_mid_force(current: int, support_distance: int, phase_distance: int) -> float:
    mf = (Uo / (2 * PI)) * (sqrt(3) / 2) * (current * 1000 * k * sqrt(2))**2 * (support_distance / phase_distance)
    return mf

if __name__ == '__main__':
    r = magnetic_mid_force(16, 1000, 202)
    print(round(r, 2))
