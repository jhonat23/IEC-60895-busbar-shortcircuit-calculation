from app import create_app
from flask import render_template, redirect, make_response
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

        current = calc_form.shortcircuit_current.data
        support_distance = calc_form.support_distance.data
        phase_distance = calc_form.phase_distance.data

        print('SUBMIT DATA: ', current, support_distance, phase_distance)

        result = round(magnetic_mid_force(current, support_distance, phase_distance), 2)

        return render_template('results.html', result=result)

    return render_template('calc.html', **context)

@app.route('/results', methods=['GET', 'POST'])
def results():

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)