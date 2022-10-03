from app import create_app
from flask import render_template, redirect, make_response
from app.forms import SystemForm, BusbarForm, DisposalForm

app = create_app()

@app.route('/')
def root():
    response = make_response(redirect('/home'))
    return response

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/step_one', methods=['GET', 'POST'])
def step_one():
    system_form = SystemForm()
    context = {
        'system_form': system_form
    }
    return render_template('stepone.html', **context)

@app.route('/step_two', methods=['GET', 'POST'])
def step_two():
    busbar_form = BusbarForm()
    context = {
        'busbar_form': busbar_form
    }
    return render_template('steptwo.html', **context)

@app.route('/step_three', methods=['GET', 'POST'])
def step_three():
    disposal_form = DisposalForm()
    context = {
        'disposal_form': disposal_form
    }
    return render_template('stepthree.html', **context)

@app.route('/results', methods=['GET', 'POST'])
def results():

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)