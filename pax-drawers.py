# Import required libraries
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define drawer sizes (width, height)
large_drawer = (928, 301)
small_drawer = (428, 301)

# Define all box sizes (width, height)
boxes = [
    (60, 120), (120, 60), (95, 123), (95, 125), (120, 125), (120, 155), (120, 213),
    (123, 95), (123, 210), (125, 95), (155, 120), (180, 220), (185, 350),
    (210, 123), (210, 125), (213, 210), (220, 180), (215, 125), (125, 215),
    (240, 350), (245, 355), (280, 200), (350, 185), (350, 240),
    (355, 245), (365, 240)
]

# Identify the 3 smallest for gap filling
filler_box_set = {(60, 120), (95, 123), (95, 125)}
main_box_set = {b for b in boxes if b not in filler_box_set}

# Normalise orientation
main_boxes = [tuple(sorted(b)) for b in main_box_set]
filler_boxes = [tuple(sorted(b)) for b in filler_box_set]

box_color = "#e8a6b1"


def ensure_output_folder(folder_name="outputs"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


def can_place(grid, x, y, w, h, drawer_w, drawer_h):
    if x + w > drawer_w or y + h > drawer_h:
        return False
    return all(not grid[x + dx][y + dy] for dx in range(w) for dy in range(h))


def mark_occupied(grid, x, y, w, h):
    for dx in range(w):
        for dy in range(h):
            grid[x + dx][y + dy] = True


def place_boxes(drawer_size, box_sizes, grid=None, max_repeats=999):
    width, height = drawer_size
    if grid is None:
        grid = [[False for _ in range(height)] for _ in range(width)]
    placed_boxes = []

    for box in sorted(box_sizes, key=lambda b: b[0] * b[1], reverse=True):
        w, h = box
        count = 0
        while count < max_repeats:
            placed = False
            for x in range(0, width - w + 1):
                for y in range(0, height - h + 1):
                    if can_place(grid, x, y, w, h, width, height):
                        placed_boxes.append((x, y, w, h))
                        mark_occupied(grid, x, y, w, h)
                        placed = True
                        break
                if placed:
                    break
            if not placed:
                break
            count += 1

    return placed_boxes, grid


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


def layout_signature(layout):
    return tuple(sorted((w, h) for _, _, w, h in layout))


def generate_unique_best_layouts(drawer_size, num_layouts=3):
    best_layouts = []
    seen_signatures = set()

    # Use varied sorting strategies to help generate diverse layouts
    sorting_strategies = [
        lambda b: -b[0] * b[1],  # by area
        lambda b: -max(b),      # by max dimension
        lambda b: -min(b),      # by min dimension
        lambda b: b[0],         # by width
        lambda b: b[1],         # by height
    ]

    attempts = 0
    while len(best_layouts) < num_layouts and attempts < 20:
        strategy = sorting_strategies[attempts % len(sorting_strategies)]

        grid = [[False for _ in range(drawer_size[1])] for _ in range(drawer_size[0])]
        ordered_main = sorted(main_boxes, key=strategy)
        ordered_fillers = sorted(filler_boxes, key=strategy)

        layout_main, grid = place_boxes(drawer_size, ordered_main, grid)
        layout_fillers, _ = place_boxes(drawer_size, ordered_fillers, grid)
        layout_total = layout_main + layout_fillers
        used_area = sum(w * h for (_, _, w, h) in layout_total)

        sig = layout_signature(layout_total)
        if sig not in seen_signatures:
            seen_signatures.add(sig)
            best_layouts.append((used_area, layout_total))

        attempts += 1

    best_layouts.sort(key=lambda x: x[0], reverse=True)
    return [layout for _, layout in best_layouts]


def print_unique_box_sizes():
    all_boxes = [tuple(sorted(b)) for b in boxes]
    unique_boxes = sorted(set(all_boxes))
    print("Unique box sizes (HxW):")
    for w, h in unique_boxes:
        print(f"  {h} x {w}")


def run_layouts():
    print_unique_box_sizes()
    output_dir = ensure_output_folder()
    summaries = {}

    for drawer_name, drawer_size in [("large_drawer", large_drawer), ("small_drawer", small_drawer)]:
        layouts = generate_unique_best_layouts(drawer_size, num_layouts=3)
        for i, layout in enumerate(layouts, 1):
            filename = f"{drawer_name}_{i}"
            save_path = os.path.join(output_dir, f"{filename}.png")
            draw_layout(drawer_size, layout, filename.replace("_", " ").title(), save_path)

            area_used = sum(w * h for (_, _, w, h) in layout)
            drawer_area = drawer_size[0] * drawer_size[1]
            fill_percentage = round(100 * area_used / drawer_area, 2)

            summaries[filename] = {
                "boxes_used": len(layout),
                "area_used_mm2": area_used,
                "drawer_area_mm2": drawer_area,
                "fill_percentage": fill_percentage
            }

    print("\nSummary of Layouts:")
    for name, stats in summaries.items():
        print(f"  {name}: {stats['fill_percentage']}% fill with {stats['boxes_used']} boxes "
              f"({stats['area_used_mm2']} mm² used of {stats['drawer_area_mm2']} mm²)")


# Run it!
run_layouts()
