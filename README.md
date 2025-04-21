# 📦 Drawer Organisation with Python

This project helps visualise how to optimally pack various box sizes into IKEA PAX drawers, ideal for moving or organising efficiently hehe.

---

## 🧠 Project Design Goals

- Avoid slow or infinite loops for fast layout generation.
- Greedy algorithms ensure speed while achieving close to optimal coverage.
- Allow boxes to be rotated to best fit in the drawer.
- Provide **three best layout options** for each drawer, based on space usage.
- Optimise for **area filled**, **box height**, or **box width**.
- Each box can be rotated to fit the layout.
- Prioritise use of **larger boxes**, using smaller boxes as fillers.
- No overlap is allowed, boxes **must fit flat** and within drawer bounds.

---

## 🚀 Get Started

### 1. Clone the repo

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Run the project

```bash
pip install -r requirements.txt
python pax-drawers.py
```
