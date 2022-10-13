from math import pi, sqrt, log, atan
from sympy import *

# Constants
PI = pi # 3.1415...
Uo = 4 * PI * (10)**-7 # Vacuum permeability (H/m)
k = 1.35 # Value from R/X=0.3 relation in 4.3.1 of IEC 60909

# For calculate k1s factor
def k1s(busbar_width: int, busbar_thickness: int, phase_distance: int) -> float:

    """Returns factor k1s required for find equivalent phase distance. NOTE: the equation from
    IEC 60895 that is used below in this function, is setting wrong values. So this function
    is used only for validation pursopes"""

    # Equation constants
    bd = busbar_width / busbar_thickness
    ad = phase_distance / busbar_thickness
    adbd = ad / bd

    # Equation components
    A = ((((ad + 1) / bd)**3) * log((((ad + 1)**2) + (bd**2)) / ((ad + 1)**2)))
    B = (2 * (adbd**3) * log((ad**2 + bd**2) / ad**2))
    C = (((ad - 1) / bd)**3 * log((((ad - 1)**2) + (bd**2)) / ((ad - 1)**2)))

    Da = ((adbd) * log(((ad + 1)**2 + bd**2) / (ad**2 + bd**2)))
    Db = ((1 / bd) * log(((ad + 1)**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    Dc = ((adbd) * log((ad**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    D = (Da + Db - Dc)

    Ea = ((((ad + 1) / bd)**2) * atan(bd / (ad + 1)))
    Eb = (2 * adbd**2 * atan(1 / adbd))
    Ec = ((((ad - 1) / bd)**2) * atan(bd / (ad - 1)))
    E = (Ea - Eb + Ec)

    Fa = (atan((ad + 1) / bd))
    Fb = (2 * atan(adbd))
    Fc = (2 * atan((ad - 1) / bd))
    F = (Fa - Fb + Fc)

    # Equation
    k = (- A + B - C + (3* D) + (6 * E) + (2 * F))
    ka = k * ((ad * bd) / 6)

    return ka

# Functions
def magnetic_mid_force(current: int, support_distance: int, phase_distance: int, busbar_width: int, busbar_thickness: int) -> float:

    """Calculates de the maximun theoric magnetic force on mid busbar on 3-phase shortcircuit"""

    # Magnetic force calculation
    mf = (Uo / (2 * PI)) * (sqrt(3) / 2) * (current * 1000 * k * sqrt(2))**2 * (support_distance / phase_distance)

    return mf

if __name__ == '__main__':
    r = magnetic_mid_force(16, 1000, 200, 60, 10)
    print(round(r, 2))

    #testing sympy:

    ad, bd, adbd = symbols('ad bd adbd')
    init_printing(use_unicode=True)

    A = ((((ad + 1) / bd)**3) * log((((ad + 1)**2) + (bd**2)) / ((ad + 1)**2)))
    B = (2 * (adbd**3) * log((ad**2 + bd**2) / ad**2))
    C = (((ad - 1) / bd)**3 * log((((ad - 1)**2) + (bd**2)) / ((ad - 1)**2)))

    Da = ((adbd) * log(((ad + 1)**2 + bd**2) / (ad**2 + bd**2)))
    Db = ((1 / bd) * log(((ad + 1)**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    Dc = ((adbd) * log((ad**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    D = (Da + Db - Dc)

    Ea = ((((ad + 1) / bd)**2) * atan(bd / (ad + 1)))
    Eb = (2 * adbd**2 * atan(1 / adbd))
    Ec = ((((ad - 1) / bd)**2) * atan(bd / (ad - 1)))
    E = (Ea - Eb + Ec)

    Fa = (atan((ad + 1) / bd))
    Fb = (2 * atan(adbd))
    Fc = (2 * atan((ad - 1) / bd))
    F = (Fa - Fb + Fc)

    # Equation
    k = (- A + B - C + (3* D) + (6 * E) + (2 * F))
    ka = k * ((ad * bd) / 6)
    pprint(ka)

    kb = ka.subs([(ad, 20), (bd, 6), (adbd, 3.34)])
    print(kb)
    print(kb.evalf())
    
