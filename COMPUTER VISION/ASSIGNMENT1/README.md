# Assignment 1 — Generalized Hough Transform for Object Detection

Implementation of the Generalized Hough Transform (GHT) to detect template objects in scene images across multiple scales and rotations.
Part of **BBM418 / AIN433 – Computer Vision Lab**, Hacettepe University.

## Tech Stack

- Python 3
- OpenCV (`cv2`)
- NumPy, matplotlib
- Jupyter Notebook (ran on Kaggle)

## Dataset

Two datasets provided via Kaggle (`bbm418-1st-assignment-ds`):
- `dataset_daisy/` — daisy template + scene images (PNG)
- `dataset_fish/` — fish template + scene images (PNG)

## Prerequisites

```bash
pip install opencv-python numpy matplotlib jupyter
```

## How to Run

```bash
jupyter notebook assignment1.ipynb
```

Update `DATASET_DIR` and `OUTPUT_DIR` to point to your local paths (or mount from Kaggle). The notebook processes both datasets automatically and saves detection visualizations to the output directory.

## Key Learnings

- Built the full GHT pipeline from scratch: R-table construction, 4D accumulator voting (x, y, scale, rotation), and non-maximal suppression for peak detection
- Templates with more R-table entries (daisy: 429 vs fish: 186) have higher detection potential but also higher sensitivity to scene clutter
- Discrete rotation search (15° steps) is a practical trade-off; rotation quantization causes vote splitting and reduces peak strength for objects at intermediate angles
