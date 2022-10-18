from app import create_app
from flask import render_template, redirect, make_response, url_for
from app.forms import CalcForm
from app.operations import magnetic_mid_force, mechanical_stress, elastic_limit

app = create_app()

@app.route('/')
def root():
    response = make_response(redirect('/home'))
    return response

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    calc_form = CalcForm()
    context = {
        'calc_form': calc_form
    }

    if calc_form.validate_on_submit():
        return redirect(url_for('results'))

    return render_template('calc.html', **context)

@app.route('/results', methods=['GET', 'POST'])
def results():
    calc_form = CalcForm()

    current = calc_form.shortcircuit_current.data
    support_distance = calc_form.support_distance.data
    phase_distance = calc_form.phase_distance.data
    busbar_width = calc_form.busbar_width.data
    busbar_thickness = calc_form.busbar_thickness.data
    span_number = calc_form.span_number.data

    if not phase_distance:
        magnetic_force = 0
        mech_stress = 0
    else:
        magnetic_force = round(magnetic_mid_force(current, support_distance, phase_distance), 2)
        mech_stress = round(mechanical_stress(magnetic_force, support_distance, busbar_width, busbar_thickness, span_number), 2)

    is_busbar_ok = elastic_limit(mech_stress)

    # print('spans', span_number)
    # print('estres mecánico: ', mech_stress)

    context = {
        'magnetic_force': magnetic_force,
        'mech_stress': mech_stress,
        'is_busbar_ok': is_busbar_ok
    }

    return render_template('results.html', **context)

@app.route('/about/me')
def about_me():
    return render_template('aboutme.html')

if __name__ == '__main__':
    app.run(debug=True)