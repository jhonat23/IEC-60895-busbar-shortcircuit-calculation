from app import create_app
from flask import render_template, redirect, make_response, url_for
from app.forms import CalcForm
from app.operations import magnetic_mid_force

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

    if phase_distance == 0 or phase_distance == None:
        magnetic_force = 0
    else:
        magnetic_force = magnetic_mid_force(current, support_distance, phase_distance)

    context = {
        'magnetic_force': magnetic_force
    }

    return render_template('results.html', **context)

if __name__ == '__main__':
    app.run(debug=True)