# Assignment 2 — Feature Detection and Matching

Implementation and comparison of feature detection and matching algorithms (SIFT, ORB, BRISK) for image correspondence tasks.
Part of **BBM418 / AIN433 – Computer Vision Lab**, Hacettepe University.

## Tech Stack

- Python 3
- OpenCV (`opencv-contrib-python`)
- NumPy, matplotlib, pandas
- Jupyter Notebook / Python script (ran on Kaggle)

## Dataset

Dataset available via Kaggle (`arkuzaytepe/pa2-data`).

## Prerequisites

```bash
pip install "opencv-contrib-python" "numpy==1.26.4" matplotlib pandas kagglehub jupyter
```

`opencv-contrib-python` is required for SIFT (patented descriptor support).

## How to Run

```bash
python assignment2.py
# or open as Jupyter notebook if using the .ipynb export
```

Configure the Kaggle dataset path at the top of the script.

## Key Learnings

- Compared SIFT, ORB, and BRISK detectors across keypoint count, repeatability, and matching accuracy (ratio test)
- Implemented keypoint visualization and descriptor matching pipelines; analyzed how illumination and scale changes affect detector performance
- Explored the trade-off between accuracy and computational cost across the three algorithms
