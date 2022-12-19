# IEC-60895-busbar-shortcircuit-calculation
Tool for shortcircuit calculation based on IEC60895 applied on switchgear busbars

This web app is designed for estimate and verification of busbar arrangement agains electro-mechanical stress generated by shortcircuit currents inside a switchgear and control gear assemblies.

Notice firstly that most of constrains shown below are related with size and number of subconductors per phase, so you may consider the maximun commercial sizes of busbars depending of your region.

##Scope

- The calcs are based on IEC60865 standard of 1993.
- This app only shows the mechanical effects upon busbars arrangement in switchgears and controlgears assemblies.
- Busbar arrangement consists on three cooper busbars (one per phase) symmetrically spaced with same facing type (width or thickness) at each side of central phase.
- The calcs are applied to a rectangular copper bar per phase.
- At realease of this app the maximun elastic limit of cooper is 180 MPa, in next versions this would be changeable.
- Others mechanical strenghts caused by other situations or from colateral effects of shortcircuit are despised.
- The shortcircuit peak current required to obtain the maximun strength is calculated using a k factor of 1.35 from R/X = 0.3 based on IEC60609
- The effects of re-switching are not considered

####[See report example](app/report/samples/Success_Example_shortcircuit_report.pdf)

If you have any questions about this app, please feel free to send a email: joosorio@utp.edu.co

####NOTE: the use of this app is only for educational purposes, not for commercial or industrial use.