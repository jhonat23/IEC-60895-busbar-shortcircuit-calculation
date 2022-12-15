from app import create_app
from flask import make_response, redirect, render_template

app = create_app()

print(app.url_map)

@app.route('/')
def root():
    response = make_response(redirect('/intro'))
    return response

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/aboutapp')
def about_app():
    return render_template('aboutapp.html')

@app.route('/about/me')
def about_me():
    return render_template('aboutme.html')

if __name__ == '__main__':
    app.run(debug=True)