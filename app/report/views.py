import os
from . import report
from flask import send_from_directory
from app.calcs.views import context_values
from .pdfTemplate import create_document, create_report

@report.route(
    '/pdfreport', 
    methods=['GET', 'POST']
    )

def pdf_report():

    context = context_values.pop()

    doc = create_document(context['project_title'])
    create_report(context, doc)

    # Create response an retrieve pdf file
    response = send_from_directory(
        '/home/jhonat23/Pyth/Flask/IEC-60895-busbar-shortcircuit-calculation/app/report/samples', 
        f"{context['project_title'].replace(' ', '_')}_shortcircuit_report.pdf"
        )
    
    # Delete de pdf file
    os.remove(f"/home/jhonat23/Pyth/Flask/"\
        f"IEC-60895-busbar-shortcircuit-calculation/app/report/samples/"\
        f"{context['project_title'].replace(' ', '_')}_shortcircuit_report.pdf")

    return response