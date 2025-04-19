# Import required libraries
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define drawer sizes (width, height in mm)
large_drawer = (928, 301)
small_drawer = (428, 301)

# Define available box sizes (width, height in mm)
boxes = [
    (60, 120), (95, 123), (95, 125), (120, 60), (120, 125), (120, 155),
    (120, 213), (123, 95), (123, 210), (125, 95), (125, 215), (155, 120),
    (180, 220), (185, 350), (210, 123), (210, 125), (213, 210), (215, 125),
    (220, 180), (240, 350), (245, 355), (280, 200), (350, 185), (350, 240),
    (355, 245), (365, 240)
]

# Separate out smaller boxes that can be used as "filler"
filler_box_set = {(60, 120), (95, 123), (95, 125)}

# Normalize box orientation (shortest side = height), and separate main vs filler
main_boxes = [tuple(sorted(b)) for b in boxes if b not in filler_box_set]
filler_boxes = [tuple(sorted(b)) for b in boxes if b in filler_box_set]

# Color used for boxes in the output image
box_color = "#e8a6b1"

# Ensure output folder exists to store layout images


def ensure_output_folder(folder_name="outputs"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Check if a box can be placed at (x, y) without going outside drawer or overlapping


def can_place(grid, x, y, w, h, dw, dh):
    if x + w > dw or y + h > dh:
        return False
    return all(not grid[x + dx][y + dy] for dx in range(w) for dy in range(h))

# Mark a section of the grid as occupied after placing a box


def mark_occupied(grid, x, y, w, h):
    for dx in range(w):
        for dy in range(h):
            grid[x + dx][y + dy] = True

# Greedy box placement: try to fit boxes one by one, rotating if needed


def place_boxes(drawer_size, sorted_boxes):
    dw, dh = drawer_size
    grid = [[False] * dh for _ in range(dw)]  # 2D occupancy grid
    layout = []

    for box in sorted_boxes:
        for (w, h) in [(box[0], box[1]), (box[1], box[0])]:  # Try both rotations
            for y in range(dh - h + 1):
                for x in range(dw - w + 1):
                    if can_place(grid, x, y, w, h, dw, dh):
                        mark_occupied(grid, x, y, w, h)
                        layout.append((x, y, w, h))
                        break  # Break once placed
                else:
                    continue
                break
            else:
                continue
            break

    return layout  # Return list of placed boxes with position and size

# Draw and save the layout as a .png file


def draw_layout(drawer_size, layout, name, save_path):
    fig, ax = plt.subplots(figsize=(drawer_size[0] / 100, drawer_size[1] / 100))
    ax.set_xlim(0, drawer_size[0])
    ax.set_ylim(0, drawer_size[1])
    ax.set_title(name)
    ax.set_aspect('equal')
    ax.set_facecolor('#f5f5f5')
    ax.add_patch(patches.Rectangle((0, 0), *drawer_size, fill=False, edgecolor='black'))

    for (x, y, w, h) in layout:
        ax.add_patch(patches.Rectangle((x, y), w, h, linewidth=0.5, edgecolor='black', facecolor=box_color))
        ax.text(x + w / 2, y + h / 2, f"{w}x{h}", color="white", fontsize=7, ha="center", va="center")

    plt.axis('off')
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Try different layout strategies and generate visual + summary outputs


def run_strategies():
    # Three strategies: prioritize large area, tall height, or wide width
    strategies = {
        "area": sorted(main_boxes, key=lambda b: b[0] * b[1], reverse=True),
        "height": sorted(main_boxes, key=lambda b: b[1], reverse=True),
        "width": sorted(main_boxes, key=lambda b: b[0], reverse=True),
    }

    output_dir = ensure_output_folder()
    summaries = {}

    for drawer_name, drawer_size in [("large_drawer", large_drawer), ("small_drawer", small_drawer)]:
        for i, (strategy, box_order) in enumerate(strategies.items(), start=1):
            # Multiply filler boxes to make them available in abundance
            layout = place_boxes(drawer_size, box_order + filler_boxes * 50)

            # Calculate fill statistics
            used_area = sum(w * h for (_, _, w, h) in layout)
            total_area = drawer_size[0] * drawer_size[1]
            fill_pct = round(100 * used_area / total_area, 2)

            # Save layout image and collect summary
            filename = f"{drawer_name}_{i}_{strategy}"
            path = os.path.join(output_dir, f"{filename}.png")
            draw_layout(drawer_size, layout, filename.replace("_", " ").title(), path)

            summaries[filename] = {
                "fill_percent": fill_pct,
                "boxes": len(layout),
                "used_mm²": used_area,
                "total_mm²": total_area,
            }

    # Print out summary of all layouts
    for name, stat in summaries.items():
        print(f"{name}: {stat['fill_percent']}% fill | {stat['boxes']} boxes")


# Run everything
run_strategies()
