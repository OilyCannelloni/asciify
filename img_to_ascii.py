########################################################
# A basic example which converts an image to ASCII Art #
########################################################

from asciify import ImageAsciifier, IACurves

p = "./images/you_are_free.jpg"  # Enter image path here

"""
OPTIMAL PARAMETERS:
rose.jpg: func=IACurves.shift(-25), resize=0.04
sunset.jpg: func=IACurves.shift(-20), resize=0.06
you_are_free.jpg: func=IACurves.CONTRAST_L, resize=0.05

Feel free to experiment with different settings and images!

Set console font size to something like 7 or resize even further down!
"""

imgAscii = ImageAsciifier(func=IACurves.CONTRAST_M)
imgAscii.img_to_ascii(load=p, resize=0.05, draw=True)
