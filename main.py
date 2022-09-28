from app import create_app

app = create_app()

@app.route('/')
def root():
    return 'Hi everyone'

if __name__ == '__main__':
    app.run(debug=True)