from . import calcs
from flask import render_template, redirect, make_response, url_for, request
from .forms import CalcForm
from .operations import magnetic_mid_force, face_type, mechanical_stress, elastic_limit, support_flexural_strength

# Global variable used to save context values
context_values = []

@calcs.route(
    '/calc', 
    methods=['GET', 'POST']
    )

def calc():

    # Get the form
    calc_form = CalcForm()
    context = {
        'calc_form': calc_form
        }

    # Check submit and redirect
    if calc_form.validate_on_submit():
        return redirect(url_for('results'))

    return render_template('calc.html', **context)

@calcs.route(
    '/results', 
    methods=['GET', 'POST']
    )

def results():

    # Get the form
    calc_form = CalcForm()

    # Retrieve all the form data
    project_title = calc_form.project_title.data
    system_voltage = calc_form.system_voltage.data
    system_frecuency = calc_form.system_frecuency.data
    current = calc_form.shortcircuit_current.data
    support_distance = calc_form.support_distance.data
    phase_distance = calc_form.phase_distance.data
    busbar_width, busbar_thickness = face_type(
        calc_form.facing_type.data, 
        calc_form.busbar_width.data, 
        calc_form.busbar_thickness.data
        )
    span_number = calc_form.span_number.data

    # Check data and obtain calcs
    if not project_title:

        magnetic_force = 0
        mech_stress = 0
        on_support_strength_A = 0
        on_support_strength_B = 0
        is_busbar_ok = 'N/A'

    else:

        magnetic_force = magnetic_mid_force(
            current, 
            support_distance, 
            phase_distance
            )

        mech_stress = mechanical_stress(
            magnetic_force, 
            support_distance, 
            busbar_width, 
            busbar_thickness, 
            span_number
            )

        on_support_strength = support_flexural_strength(
            mech_stress, 
            span_number, 
            magnetic_force
            )

        on_support_strength_A = round(on_support_strength['FdA'], 2)
        on_support_strength_B = round(on_support_strength['FdB'], 2)

        is_busbar_ok = elastic_limit(mech_stress)

    context = {
        # project data
        'project_title': project_title,
        'system_voltage': system_voltage,
        'system_frecuency': system_frecuency,
        'shortcircuit_current': current,
        # project calcs
        'magnetic_force': magnetic_force,
        'mech_stress': mech_stress,
        'on_support_strength_A': on_support_strength_A,
        'on_support_strength_B': on_support_strength_B,
        'is_busbar_ok': is_busbar_ok
        }

    # Adding context to context values for other routes
    context_values.append(context)

    return render_template('results.html', **context)