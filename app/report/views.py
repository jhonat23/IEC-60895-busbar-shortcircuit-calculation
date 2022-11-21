from . import report
from flask import send_from_directory
from app.calcs.views import context_values
from .pdfTemplate import create_report

@report.route('/pdfreport', methods=['GET', 'POST'])
def pdf_report():
    context = context_values.pop()

    create_report(context)

    return send_from_directory('/home/jhonat23/Pyth/Flask/IEC-60895-busbar-shortcircuit-calculation/', f"{context['project_title'].replace(' ', '_')}_shortcircuit_report.pdf")