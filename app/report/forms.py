from flask_wtf import FlaskForm
from wtforms import SubmitField

#Download report form
class DownloadForm(FlaskForm):
    download = SubmitField('Download report')