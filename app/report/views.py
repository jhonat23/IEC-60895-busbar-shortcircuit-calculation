from . import report
from flask import send_from_directory
from app.calcs.views import context_values

@report.route('/pdfreport', methods=['GET', 'POST'])
def pdf_report():
    context = context_values.pop()

    

    return send_from_directory('/home/jhonat23/Pyth/Flask/IEC-60895-busbar-shortcircuit-calculation/', 'testReport.pdf')