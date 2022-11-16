from app import create_app
from flask import send_from_directory

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)