from math import pi, sqrt

# Constants
PI = pi # 3.1415...
Uo = 4 * PI * (10)**-7 # Vacuum permeability (H/m)

# Functions
def magnetic_mid_force(current: int, support_distance: int, phase_distance: int) -> float:
    mf = (Uo / (2 * PI)) * (sqrt(3) / 2) * (current)**2 * (support_distance / phase_distance)
    return mf

if __name__ == '__main__':
    r = magnetic_mid_force(30600, 1, 0.202)
    print(round(r, 2))
