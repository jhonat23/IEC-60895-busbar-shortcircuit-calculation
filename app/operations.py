from math import pi, sqrt, log, atan

# Constants
PI = pi # 3.1415...
Uo = 4 * PI * (10)**-7 # Vacuum permeability (H/m)
k = 1.35 # Value from R/X=0.3 relation in 4.3.1 of IEC 60909
q = 1.5 # Plasticity factor for rectangular busbars
CuR02 = 180 # MPa, elastic limit for cooper 

# Internal functions

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

def _span_factor(number_of_spans: str) -> dict:
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

def _Vf_Vr(mech_stress: float, R02: int) -> float:
    """Returns factor VfxVr related with supports flexural strength"""

    factor = mech_stress / (0.8 * R02)

    if factor <= 0.37 and factor > 0:
        return 2.7
    elif factor > 0.37 and factor <= 1.0:
        return 1 / factor
    elif factor > 1.0:
        return 1.0

# Functions
def face_type(facing_type: str, busbar_width: int, busbar_thickness: int) -> tuple:
    """Returns a tuple of busbar width and thickness depending of facing type"""

    if facing_type == 'Witdh faced' or facing_type == 'N/A':
        return busbar_width, busbar_thickness
    elif facing_type == 'Thickness faced':
        busbar_width, busbar_thickness = busbar_thickness, busbar_width
        return busbar_width, busbar_thickness
    else:
        return 1, 1

def magnetic_mid_force(current: int, support_distance: int, phase_distance: int) -> float:
    """Calculates de the maximum theoric magnetic force on mid busbar on 3-phase shortcircuit"""

    # Magnetic force calculation
    mf = (Uo / (2 * PI)) * (sqrt(3) / 2) * (current * 1000 * k * sqrt(2))**2 * (support_distance / phase_distance)
    result = round(mf, 2)

    return result

def mechanical_stress(magnetic_force: float, support_distance: int, busbar_width: int, busbar_thickness: int, span_number: str) -> float:
    """Calculates the busbar maximum mechanical stress. If mechanical stress is XXXXX the busbar arrangement cannot be installed"""

    span_factors = _span_factor(span_number)
    ms = span_factors['beta'] * ((magnetic_force * support_distance) / (8 * ((2 * (busbar_width * busbar_thickness**3) / 12) / busbar_thickness)))
    result = round(ms, 2)

    return result

def elastic_limit(mechanical_stress: float) -> str:
    """Show if a busbar arrangement accomplish with elastic limit"""
    limit = q * CuR02

    if mechanical_stress <= limit:
        return 'YES'
    else:
        return 'NO, CHECK THE BUSBAR DESING'

def support_flexural_strength(mech_stress: float, span_number: str, magnetic_force: float) -> dict:
    """Returns the support flexural strength of external and internal supports of busbar arrangement"""

    supports_flex_strength = {}

    VfxVr = _Vf_Vr(mech_stress, CuR02)
    span_factors = _span_factor(span_number)

    supports_flex_strength['FdA'] = VfxVr * span_factors['alfa']['A'] * magnetic_force
    supports_flex_strength['FdB'] = VfxVr * span_factors['alfa']['B'] * magnetic_force

    return supports_flex_strength

if __name__ == '__main__':
    r = magnetic_mid_force(16, 1000, 200)
    #m = mechanical_stress(r, 1000, 60, 10)
    print(round(r, 2))

    assert 3 == 2


    #-----------------------------------------------

    #testing sympy (PLEASE IF YOU WANT TO CHECK THE EQUATION, PLEASE INSTALL sympy AND IMPORT MODULE HERE, IT IS POSSIBLE THAT APP DOES NOT WORK DUE A CONFLICT WITH MODULES DATA TYPE USING sympy)

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