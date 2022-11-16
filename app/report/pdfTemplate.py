from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

doc_width, doc_heigth = letter

def hello(c):
    c.drawString(100, 100, 'Hello World')


if __name__ == '__main__':
    rep = canvas.Canvas('testReport.pdf', pagesize=letter, verbosity=1)
    hello(rep)
    rep.showPage()
    rep.save()
