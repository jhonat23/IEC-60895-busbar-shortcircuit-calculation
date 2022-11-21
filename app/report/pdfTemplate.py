from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

# width :612 heigth: 792
doc_width, doc_heigth = letter

def create_report(data: dict) -> None:

    # Creation of document
    rep = Canvas(f"{data['project_title'].replace(' ', '_')}_shortcircuit_report.pdf", pagesize=letter, verbosity=1)

    # Drawing string methods
    # Title:
    rep.drawString(doc_width - 412, doc_heigth - 100, f"{data['project_title']} Shortcircuit Withstand Calculation Report")

    # Intro text
    rep.drawString(doc_width - 412, doc_heigth - 200, 'This document shows the calculation results of shortcircuit withstand on specified busbar arrangement. The busbar arrangement data are this:')

    rep.showPage()
    rep.save()

if __name__ == '__main__':

    def hello(c: Canvas):
        c.drawString(100, 100, 'Hello World')

    rep = Canvas('testReport.pdf', pagesize=letter, verbosity=1)
    hello(rep)
    rep.showPage()
    rep.save()
