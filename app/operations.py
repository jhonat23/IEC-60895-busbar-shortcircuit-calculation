from math import pi, sqrt, log, atan
from sympy import *

# Constants
PI = pi # 3.1415...
Uo = 4 * PI * (10)**-7 # Vacuum permeability (H/m)
k = 1.35 # Value from R/X=0.3 relation in 4.3.1 of IEC 60909
q = 1.5 # Plasticity factor
CuR02 = 69 # MPa elastic limit for cooper 

# Calculate k1s factor
def _k1s(busbar_width: int, busbar_thickness: int, phase_distance: int) -> float:

    """Returns factor k1s required for find equivalent phase distance. NOTE: the equation given from
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

def _span_factor(number_of_spans: int) -> float:
    """Returns a span factor depending of the number of spans of arrangement"""

    span_factors = {'alfa': {'A': 0, 'B':0}, 'beta': 0, 'gamma': 0}

    if number_of_spans == '1':
        span_factors['alfa']['A'] = 0.5
        span_factors['alfa']['B'] = 0.5
        span_factors['beta'] = 1
        span_factors['gamma'] = 1.57
    elif number_of_spans == '2':
        span_factors['alfa']['A'] = 0.375
        span_factors['alfa']['B'] = 1.25
        span_factors['beta'] = 0.73
        span_factors['gamma'] = 2.45
    elif number_of_spans >= '3 or more':
        span_factors['alfa']['A'] = 0.4
        span_factors['alfa']['B'] = 1.1
        span_factors['beta'] = 0.73
        span_factors['gamma'] = 3.56 

    return span_factors


# Functions
def magnetic_mid_force(current: int, support_distance: int, phase_distance: int) -> float:
    """Calculates de the maximum theoric magnetic force on mid busbar on 3-phase shortcircuit"""

    # Magnetic force calculation
    mf = (Uo / (2 * PI)) * (sqrt(3) / 2) * (current * 1000 * k * sqrt(2))**2 * (support_distance / phase_distance)

    return mf

def mechanical_stress(magnetic_force: float, support_distance: int, busbar_width: int, busbar_thickness: int, span_number) -> float:
    """Calculates the busbar maximum mechanical stress. If mechanical stress is XXXXX the busbar arrangement cannot be installed"""

    span_factors = _span_factor(span_number)
    ms = span_factors['beta'] * ((magnetic_force * support_distance) / (8 * ((2 * (busbar_width * busbar_thickness**3) / 12) / busbar_thickness)))

    return ms

def elastic_limit(mechanical_stress: float) -> str:
    """Show if a busbar arrangement accomplish with elastic limit"""
    limit = q * CuR02

    if mechanical_stress <= limit:
        return 'The busbar arrange can resist the shortcircuit'
    else:
        return 'The busbar arrange cannot resist the shortcircuit'

if __name__ == '__main__':
    r = magnetic_mid_force(16, 1000, 200)
    m = mechanical_stress(r, 1000, 60, 10)
    print(round(r, 2), round(m, 2))


    #testing sympy:

    # ad, bd, adbd = symbols('ad bd adbd')
    # init_printing(use_unicode=True)

    # A = ((((ad + 1) / bd)**3) * log((((ad + 1)**2) + (bd**2)) / ((ad + 1)**2)))
    # B = (2 * (adbd**3) * log((ad**2 + bd**2) / ad**2))
    # C = (((ad - 1) / bd)**3 * log((((ad - 1)**2) + (bd**2)) / ((ad - 1)**2)))

    # Da = ((adbd) * log(((ad + 1)**2 + bd**2) / (ad**2 + bd**2)))
    # Db = ((1 / bd) * log(((ad + 1)**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    # Dc = ((adbd) * log((ad**2 + bd**2) / ((ad - 1)**2 + bd**2)))
    # D = (Da + Db - Dc)

    # Ea = ((((ad + 1) / bd)**2) * atan(bd / (ad + 1)))
    # Eb = (2 * adbd**2 * atan(1 / adbd))
    # Ec = ((((ad - 1) / bd)**2) * atan(bd / (ad - 1)))
    # E = (Ea - Eb + Ec)

    # Fa = (atan((ad + 1) / bd))
    # Fb = (2 * atan(adbd))
    # Fc = (2 * atan((ad - 1) / bd))
    # F = (Fa - Fb + Fc)

    # # Equation
    # k = (- A + B - C + (3* D) + (6 * E) + (2 * F))
    # ka = k * ((ad * bd) / 6)
    # pprint(ka)

    # kb = ka.subs([(ad, 20), (bd, 6), (adbd, 3.34)])
    # print(kb)
    # print(kb.evalf())
    
