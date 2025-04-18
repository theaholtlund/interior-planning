# Import required libraries
import os
import random
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import box as shapely_box

# Define drawer sizes (width, height)
large_drawer = (928, 301)
small_drawer = (428, 301)

# Define box sizes (width, height)
boxes = [
    (60, 120), (120, 60), (95, 123), (95, 125), (120, 125), (120, 155), (120, 213),
    (123, 95), (123, 210), (125, 95), (155, 120), (180, 220), (185, 350),
    (210, 123), (210, 125), (213, 210), (220, 180), (215, 125), (125, 215),
    (240, 350), (245, 355), (280, 200), (350, 185), (350, 240),
    (355, 245), (365, 240)
]
unique_boxes = sorted({(min(w, h), max(w, h)) for w, h in boxes}, key=lambda b: b[0] * b[1], reverse=True)

# Show the unique box sizes
print("Unique inner box sizes, height x width:")
for h, w in unique_boxes:
    print(f"  {h} x {w}")

# Visualisation color
box_color = "#e8a6b1"


def place_boxes_grid(drawer_size, boxes):
    width, height = drawer_size
    grid = [[False for _ in range(height)] for _ in range(width)]
    placed_boxes = []

    def can_place(x, y, w, h):
        if x + w > width or y + h > height:
            return False
        return all(not grid[x + dx][y + dy] for dx in range(w) for dy in range(h))

    def mark_occupied(x, y, w, h):
        for dx in range(w):
            for dy in range(h):
                grid[x + dx][y + dy] = True

    for w, h in boxes:
        for x in range(width):
            for y in range(height):
                if can_place(x, y, w, h):
                    placed_boxes.append((x, y, w, h))
                    mark_occupied(x, y, w, h)
                    break  # Place one and move on

    return placed_boxes


def draw_layout(drawer_size, layout, name, save_path):
    fig, ax = plt.subplots(figsize=(drawer_size[0] / 100, drawer_size[1] / 100))
    ax.set_xlim(0, drawer_size[0])
    ax.set_ylim(0, drawer_size[1])
    ax.set_title(name)
    ax.set_aspect('equal')
    ax.set_facecolor('#f5f5f5')
    ax.add_patch(patches.Rectangle((0, 0), drawer_size[0], drawer_size[1], fill=False, edgecolor='black'))

    for (x, y, w, h) in layout:
        rect = patches.Rectangle((x, y), w, h, linewidth=0.5, edgecolor='black', facecolor=box_color)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, f"{w}x{h}", color="white", fontsize=7, ha="center", va="center")

    plt.axis('off')
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def ensure_output_folder(folder_name="outputs"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


output_dir = ensure_output_folder()

# Generate 3 layouts per drawer with shuffled box order
summaries = {}
for drawer_name, drawer_size in [("large_drawer", large_drawer), ("small_drawer", small_drawer)]:
    for i in range(1, 4):
        shuffled = unique_boxes.copy()
        random.shuffle(shuffled)
        layout = place_boxes_grid(drawer_size, shuffled)
        filename = f"{drawer_name}_{i}"
        draw_layout(drawer_size, layout, filename.replace("_", " ").title(),
                    os.path.join(output_dir, f"{filename}.png"))

        area_used = sum(w * h for (_, _, w, h) in layout)
        drawer_area = drawer_size[0] * drawer_size[1]
        summaries[filename] = {
            "boxes_used": len(layout),
            "area_used_mm2": area_used,
            "drawer_area_mm2": drawer_area,
            "fill_percentage": round(100 * area_used / drawer_area, 2)
        }

# Print summaries
print("\nSummary of Layouts:")
for name, stats in summaries.items():
    print(f"  {name}: {stats['fill_percentage']}% fill with {stats['boxes_used']} boxes "
          f"({stats['area_used_mm2']} mm² used of {stats['drawer_area_mm2']} mm²)")

# Optional: Save to JSON for reference
with open(os.path.join(output_dir, "summaries.json"), "w") as f:
    json.dump(summaries, f, indent=4)
