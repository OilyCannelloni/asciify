##############################################
# Live camera preview converted to ASCII Art #
##############################################

from asciify import VideoAsciifier, IACurves

"""
OPTIMAL PARAMETERS:
func=IACurves.CONTRAST_L
resize depends on camera resolution, in my case 0.3
fps=30 works fine and smooth
For larger sizes the preview may glitch, try lowering resize

Feel free to experiment with different settings and images!

Set console font size to something like 7 or resize even further down!
"""

vidAscii = VideoAsciifier(func=IACurves.binary(127))
vidAscii.start_preview(fps=30, resize=0.25)
# exit using CTRL+C
