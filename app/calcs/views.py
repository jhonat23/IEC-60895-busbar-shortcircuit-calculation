from . import calcs
from flask import render_template, redirect, make_response, url_for, request
from .forms import CalcForm
from .operations import magnetic_mid_force, face_type, mechanical_stress, elastic_limit, support_flexural_strength

# Global variable used to save context values
context_values = []

@calcs.route('/calc', methods=['GET', 'POST'])
def calc():
    calc_form = CalcForm()
    context = {
        'calc_form': calc_form
    }

    if calc_form.validate_on_submit():
        return redirect(url_for('results'))

    return render_template('calc.html', **context)

@calcs.route('/results', methods=['GET', 'POST'])
def results():
    calc_form = CalcForm()

    project_title = calc_form.project_title.data
    current = calc_form.shortcircuit_current.data
    support_distance = calc_form.support_distance.data
    phase_distance = calc_form.phase_distance.data
    busbar_width, busbar_thickness = face_type(calc_form.facing_type.data, calc_form.busbar_width.data, calc_form.busbar_thickness.data)
    # busbar_width = calc_form.busbar_width.data
    # busbar_thickness = calc_form.busbar_thickness.data
    span_number = calc_form.span_number.data

    if not project_title:
        magnetic_force = 0
        mech_stress = 0
        on_support_strength_A = 0
        on_support_strength_B = 0
        is_busbar_ok = 'N/A'
    else:
        magnetic_force = magnetic_mid_force(current, support_distance, phase_distance)
        mech_stress = mechanical_stress(magnetic_force, support_distance, busbar_width, busbar_thickness, span_number)
        on_support_strength = support_flexural_strength(mech_stress, span_number, magnetic_force)

        on_support_strength_A = round(on_support_strength['FdA'], 2)
        on_support_strength_B = round(on_support_strength['FdB'], 2)

        is_busbar_ok = elastic_limit(mech_stress)

    # print('spans', span_number)
    # print('estres mecánico: ', mech_stress)

    context = {
        'magnetic_force': magnetic_force,
        'mech_stress': mech_stress,
        'is_busbar_ok': is_busbar_ok,
        'on_support_strength_A': on_support_strength_A,
        'on_support_strength_B': on_support_strength_B
    }

    context_values.append(context)

    return render_template('results.html', **context)