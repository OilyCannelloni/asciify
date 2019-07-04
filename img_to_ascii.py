########################################################
# A basic example which converts an image to ASCII Art #
########################################################

from asciify import ImageAsciifier, IACurves

p = "./images/rose.jpg"  # Enter image path here

"""
OPTIMAL PARAMETERS:
rose.jpg: func=IACurves.shift(-20), resize=0.2
sunset.jpg: func=IACurves.shift(-20), resize=0.16
you_are_free.jpg: func=IACurves.CONTRAST_L, resize=0.16

Feel free to experiment with different settings and images!

Set console font size to something like 7 or resize even further down!
"""

imgAscii = ImageAsciifier(func=IACurves.shift(-20))
imgAscii.img_to_ascii(load=p, resize=0.09, draw=True)
