import os
from . import report
from flask import current_app, send_from_directory
from app.calcs.views import context_values
from .pdfTemplate import create_document, create_report

@report.route(
    '/pdfreport', 
    methods=['GET', 'POST']
    )

def pdf_report():

    # Obtaining calculation data
    context = context_values.pop()

    # Creating pdf file 
    doc = create_document(context['project_title'])
    create_report(context, doc)
    
    # Adding download folder to root path
    download_folder = os.path.join(current_app.root_path, 'report/samples/')
    #print(download_folder)
     
    # Sending response as a pdf file
    response = send_from_directory(
        download_folder,
        f"{context['project_title'].replace(' ', '_')}_shortcircuit_report.pdf"
        )

    # Deleting pdf file after download
    os.remove("app/report/samples/"\
        f"{context['project_title'].replace(' ', '_')}_shortcircuit_report.pdf"
        )

    return response