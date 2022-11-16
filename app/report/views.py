from . import report
from flask import render_template, send_from_directory
from .forms import DownloadForm

@report.route('/pdfreport')
def pdf_report():
    return send_from_directory('/home/jhonat23/Pyth/Flask/IEC-60895-busbar-shortcircuit-calculation/', 'testReport.pdf')