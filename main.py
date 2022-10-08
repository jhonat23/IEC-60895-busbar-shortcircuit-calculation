from app import create_app
from flask import render_template, redirect, make_response
from app.forms import SystemForm, BusbarForm, DisposalForm
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
    system_form = SystemForm()
    busbar_form = BusbarForm()
    disposal_form = DisposalForm()
    context = {
        'system_form': system_form,
        'busbar_form': busbar_form,
        'disposal_form': disposal_form
    }

    if disposal_form.validate_on_submit():

        current = system_form.shortcircuit_current.data
        support_distance = disposal_form.support_distance.data
        phase_distance = busbar_form.phase_distance.data

        print(current)

        result = magnetic_mid_force(current, support_distance, phase_distance)

        return render_template('results.html', result=result)

    return render_template('calc.html', **context)

@app.route('/results', methods=['GET', 'POST'])
def results():

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)