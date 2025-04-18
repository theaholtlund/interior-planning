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


def draw_drawer(drawer_size, drawer_name):
    fig, ax = plt.subplots(figsize=(drawer_size[0]/100, drawer_size[1]/100))
    ax.set_xlim(0, drawer_size[0])
    ax.set_ylim(0, drawer_size[1])
    ax.set_title(f"{drawer_name} ({drawer_size[0]} x {drawer_size[1]} mm)")
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f0f0')
    ax.add_patch(patches.Rectangle((0, 0), drawer_size[0], drawer_size[1], fill=False, edgecolor='black'))
    return fig, ax


def draw_boxes(ax, layout, color="#4a90e2"):
    for (x, y, w, h) in layout:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)


def main():
    layout_1 = fill_drawer(large_drawer, unique_oriented_boxes)
    layout_2 = fill_drawer(small_drawer, unique_oriented_boxes)

    # Drawer 1
    fig1, ax1 = draw_drawer(large_drawer, "Drawer 1")
    draw_boxes(ax1, layout_1)
    fig1.savefig("drawer_1_layout.png", dpi=300)

    # Drawer 2
    fig2, ax2 = draw_drawer(small_drawer, "Drawer 2")
    draw_boxes(ax2, layout_2)
    fig2.savefig("drawer_2_layout.png", dpi=300)

    print(f"Drawer 1: {len(layout_1)} boxes placed.")
    print(f"Drawer 2: {len(layout_2)} boxes placed.")


if __name__ == "__main__":
    main()
