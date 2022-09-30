from app import create_app
from flask import render_template

app = create_app()

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)