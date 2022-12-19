from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader

# A4 size: width :210mm heigth: 297mm
# in points: width: 595, heigth: 842. (doc_width, doc_heigth)
# factor: 2.8 points per mm. 
doc_width, doc_heigth = A4

# Creation of document
def create_document(project_title: str) -> Canvas:

    rep = Canvas(
        f"app/report/samples/"\
        f"{project_title.replace(' ', '_')}_shortcircuit_report.pdf", 
        pagesize=A4,
        verbosity=1)

    return rep

# Internal and aux functions
# Line decorator
def lines(func) -> None:

    def wrapper(
        my_string, rep, 
        relative_width, 
        relative_heigth
        ):

        rep.line(
            doc_width-580, doc_heigth - relative_heigth + 18, 
            doc_width - 15, doc_heigth-relative_heigth + 18
            )

        func(
            my_string, rep, 
            relative_width, relative_heigth
            )

        rep.line(
            doc_width-580, doc_heigth-relative_heigth - 12, 
            doc_width - 15, doc_heigth-relative_heigth - 12
            )

    return wrapper


@lines
def make_title(
    subtitle_string: str, 
    rep: Canvas, 
    relative_width: int, 
    relative_heigth: int
    ) -> None:

    rep.drawString(
        doc_width - relative_width, 
        doc_heigth - relative_heigth, 
        subtitle_string
        )


def load_info(
    subs: dict, 
    rep: Canvas, 
    relative_heigth: int
    ) -> None:

    space = 20
    for k, v in subs.items():
        # data
        rep.drawRightString(
            doc_width - 80, 
            doc_heigth - relative_heigth - space,
            f'{v[0]} {v[1]}'
            )
        # data_title
        rep.drawString(
            doc_width - 515, 
            doc_heigth - relative_heigth - space,
            k
            )
        # add space between lines
        space += 15
        
# Start with document
def create_report(data: dict, rep: Canvas) -> None:

    # -----------------------------Header----------------------------------
    # Image
    image = ImageReader(
        'app/static/'\
        'images/Header.jpg'
        )

    rep.drawImage(
        image, 
        0, 0, 
        doc_width, 1700, 
        preserveAspectRatio=True
        )

    # Title:
    rep.setFont('Times-Roman', 16)

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 100, 
        f"{data['project_title']} Shortcircuit Withstand Calculation Report"
        )

    rep.line(
        doc_width - 580, doc_heigth - 110, 
        doc_width - 15, doc_heigth - 110
        )

    # Intro text
    rep.setFont('Times-Roman', 12)

    intro_text = f'This document shows the calculation results of shortcircuit withstand on specified busbar arrangement'

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 145, 
        intro_text
        )

    # -----------------------------Body----------------------------------
    # Project data
    subtitle = 'Project info:'

    make_title(subtitle, rep, 550, 188)

    subs = {
        'Project name': [
            data['project_title'], 
            ''
            ], 
        'System Voltage': [
            data['system_voltage'], 
            'V'
            ], 
        'System frecuency': [
            data['system_frecuency'], 
            'Hz'
            ], 
        'Initial symmetric shorcirtuit current': [
            data['shortcircuit_current'], 
            'kA'
            ]}

    load_info(subs, rep, 210)

    # Project results
    subtitle2 = 'Calculation results:'

    make_title(subtitle2, rep, 550, 320)

    subs2 = {
        'Maximun magnetic force on mid-busbar': [
            data['magnetic_force'], 
            'N'
            ], 
        'Mechanical stress on busbars': [
            data['mech_stress'], 
            'MPa'
            ],
        'Maximmun internal supports strength': [
            data['on_support_strength_A'], 
            'N'
            ],
        'Maximmun external supports strength': [
            data['on_support_strength_B'], 
            'N'
            ]}

    load_info(subs2, rep, 344)

    # Conclusion
    subtitle3 = 'Conclusion'

    make_title(subtitle3, rep, 550, 452)
    
    if data['is_busbar_ok'] == 'YES':

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 490, 
            'The arrangement proposed can resist the shortcircuit event.'
            )

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 505, 
            'For better results, check if you can reduce de support distances and/or increase the phase distance.'
            ) 

    else:

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 490, 
            'The arrangement proposed can NOT resist the shortcircuit event.'
            )

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 505, 
            'For better results, check if you can reduce de support distances and/or increase the phase distance.'
            )

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 520, 
            'Check if the width and thickness of busbar can are appropiate for the application'
            )

        rep.drawCentredString(
            doc_width // 2,
            doc_heigth - 560, 
            'CAUTION: the failure of busbar arrangement could generate other system issues'
            )

        rep.drawCentredString(
            doc_width // 2, 
            doc_heigth - 575, 
            'and could be dangerous for the enviroment and staff'
            )

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 620, 
        'WARNING: these result are totally theoretical and maybe they not represent all the reality.'
        )

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 635, 
        'Consider others environment variables to make better approaches to the arrangement calculated'
        )

    # -----------------------------Footer----------------------------------
    rep.line(doc_width-580,
            doc_heigth - 760, 
            doc_width - 15, 
            doc_heigth - 760
            )

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 780, 
        'If you have any questions or issues about results please contact me:'
        )

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 795, 
        'joosorio@utp.edu.co'
        )

    rep.setFont('Times-Roman', 10)

    rep.drawCentredString(
        doc_width // 2, 
        doc_heigth - 820, 
        f"NOTE: the use of this app is ONLY for educational purposes, not for commercial or industrial use."
        )

    # finishing page and save it
    rep.showPage()
    rep.save()

if __name__ == '__main__':
    pass
    