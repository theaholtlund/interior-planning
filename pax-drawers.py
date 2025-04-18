# Importer moduler
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import box as shapely_box

# Skuffestørrelser
drawer_1 = (928, 301)
drawer_2 = (428, 301)

# Tilgjengelige bokser med høyde og bredde i millimeter
boxes = [
    (220, 180), (180, 220), (120, 125), (350, 185), (185, 350),
    (213, 210), (120, 213), (210, 123), (350, 240), (240, 350),
    (245, 355), (355, 245), (365, 240), (123, 210), (123, 95),
    (280, 200), (210, 125), (155, 120), (120, 155), (95, 123)
]
