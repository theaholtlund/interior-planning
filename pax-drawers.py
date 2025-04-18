# Import required libraries
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import box as shapely_box

# Define sizes for the two drawers, height x width in millimetres
large_drawer = (928, 301)
small_drawer = (428, 301)

# List of available smaller box sizes, height x width in millimetres
boxes = [
    (220, 180), (180, 220), (120, 125), (350, 185), (185, 350),
    (213, 210), (120, 213), (210, 123), (350, 240), (240, 350),
    (245, 355), (355, 245), (365, 240), (123, 210), (123, 95),
    (280, 200), (210, 125), (155, 120), (120, 155), (95, 123)
]

# Remove duplicate sizes with the same area, ignoring orientation
unique_oriented_boxes = list({tuple(sorted((w, h))) for w, h in boxes})
# Sort by descending area, larger boxes first
unique_oriented_boxes.sort(key=lambda b: b[0] * b[1], reverse=True)


def fill_drawer(drawer_size, boxes):
    """
    Attempt to fill a drawer with boxes to maximise coverage.
    Boxes are placed using a simple greedy algorithm, checking every 5mm step.
    """
    placed_boxes = []
    occupied_areas = []

    for box in boxes:
        # Try both orientations, rotated and unrotated
        for orientation in [(box[0], box[1]), (box[1], box[0])]:
            w, h = orientation
            placed = False

            # Try to place box at every (x, y) coordinate in 5mm steps
            for y in range(0, drawer_size[1] - h + 1, 5):
                for x in range(0, drawer_size[0] - w + 1, 5):
                    new_box = shapely_box(x, y, x + w, y + h)

                    # Check if it overlaps any already placed box
                    if all(not new_box.intersects(existing) for existing in occupied_areas):
                        occupied_areas.append(new_box)
                        placed_boxes.append((x, y, w, h))
                        placed = True
                        break
                if placed:
                    break
    return placed_boxes


def draw_drawer(drawer_size, drawer_name):
    """
    Create a matplotlib figure representing the drawer space.
    """
    fig, ax = plt.subplots(figsize=(drawer_size[0] / 100, drawer_size[1] / 100))
    ax.set_xlim(0, drawer_size[0])
    ax.set_ylim(0, drawer_size[1])
    ax.set_title(f"{drawer_name} ({drawer_size[0]} x {drawer_size[1]} mm)")
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f0f0')
    # Outline the drawer
    ax.add_patch(patches.Rectangle((0, 0), drawer_size[0], drawer_size[1], fill=False, edgecolor='black'))
    return fig, ax


def draw_boxes(ax, layout, color="#4a90e2"):
    """
    Draw all the placed boxes inside the drawer layout.
    """
    for (x, y, w, h) in layout:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)


def ensure_output_folder(folder_name="outputs"):
    """
    Create the outputs folder if it doesn't exist.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


def main():
    # Fill each drawer with boxes
    layout_large = fill_drawer(large_drawer, unique_oriented_boxes)
    layout_small = fill_drawer(small_drawer, unique_oriented_boxes)

    # Ensure output folder exists
    output_dir = ensure_output_folder()

    # Visualise and save layout for the large drawer
    fig1, ax1 = draw_drawer(large_drawer, "Large Drawer")
    draw_boxes(ax1, layout_large)
    fig1.savefig(os.path.join(output_dir, "large_drawer_layout.png"), dpi=300)

    # Visualise and save layout for the small drawer
    fig2, ax2 = draw_drawer(small_drawer, "Small Drawer")
    draw_boxes(ax2, layout_small)
    fig2.savefig(os.path.join(output_dir, "small_drawer_layout.png"), dpi=300)

    # Summary output
    print(f"Large Drawer: {len(layout_large)} boxes placed.")
    print(f"Small Drawer: {len(layout_small)} boxes placed.")
    print(f"Layouts saved to: {output_dir}/")


if __name__ == "__main__":
    main()
