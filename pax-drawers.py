# Import required libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import box as shapely_box

# Define sizes for main drawers (in millimetres)
large_drawer = (928, 301)
small_drawer = (428, 301)

# Boxes available with height x width in millimetres
boxes = [
    (220, 180), (180, 220), (120, 125), (350, 185), (185, 350),
    (213, 210), (120, 213), (210, 123), (350, 240), (240, 350),
    (245, 355), (355, 245), (365, 240), (123, 210), (123, 95),
    (280, 200), (210, 125), (155, 120), (120, 155), (95, 123)
]

# Remove duplicates with the same area, regardless of orientation
unique_oriented_boxes = list({tuple(sorted((w, h))) for w, h in boxes})
unique_oriented_boxes.sort(key=lambda b: b[0] * b[1], reverse=True)


def fill_drawer(drawer_size, boxes):
    placed_boxes = []
    occupied_areas = []

    for box in boxes:
        for orientation in [(box[0], box[1]), (box[1], box[0])]:
            w, h = orientation
            placed = False
            for y in range(0, drawer_size[1] - h + 1, 5):
                for x in range(0, drawer_size[0] - w + 1, 5):
                    new_box = shapely_box(x, y, x + w, y + h)
                    if all(not new_box.intersects(existing) for existing in occupied_areas):
                        occupied_areas.append(new_box)
                        placed_boxes.append((x, y, w, h))
                        placed = True
                        break
                if placed:
                    break
    return placed_boxes


def main():
    layout_1 = fill_drawer(large_drawer, unique_oriented_boxes)
    layout_2 = fill_drawer(small_drawer, unique_oriented_boxes)


if __name__ == "__main__":
    main()
