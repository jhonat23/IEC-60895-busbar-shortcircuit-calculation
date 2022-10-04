from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

#forms
class SystemForm(FlaskForm):
    project_title = StringField('Project title', validators=[DataRequired()])
    system_voltage = SelectField('System Voltage (V)', validators=[DataRequired()], choices=['120', '220', '440', '480'], default='440')
    system_frecuency = SelectField('System frecuency (Hz)', validators=[DataRequired()], choices=['60', '50'], default='60')
    shortcircuit_current = IntegerField('Shortcircuit current (kA)', validators=[DataRequired()])
    submit = SubmitField('Next step (2)')

class BusbarForm(FlaskForm):
    facing_type = SelectField('Facing type', validators=[DataRequired()], choices=['Witdh faced', 'Thickness faced'])
    busbar_width = IntegerField('Busbar width w (mm)', validators=[DataRequired()], default='0')
    busbar_thickness = IntegerField('Busbar thickness t (mm)', validators=[DataRequired()], default='0')
    phase_distance = IntegerField('Phase distance a (mm)', validators=[DataRequired()], default='0')
    submit = SubmitField('Next step (3)')

class DisposalForm(FlaskForm):
    span_number = SelectField('Number of spans', validators=[DataRequired()], choices=['1', '2', '3 o more'])
    support_distance = IntegerField('Support distance (mm)', validators=[DataRequired()], default='0')
    submit = SubmitField('Next step (Results)')
