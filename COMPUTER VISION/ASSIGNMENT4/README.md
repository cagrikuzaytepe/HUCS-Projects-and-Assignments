# Assignment 4 — Pedestrian Detection with TinyDETR

Ablation study on a DETR-inspired transformer-based pedestrian detector (TinyDETR). Four experiments vary the backbone (ResNet18 vs MobileNetV2), number of object queries (50 vs 100), and the use of data augmentation.
Part of **BBM418 / AIN433 – Computer Vision Lab**, Hacettepe University.

## Tech Stack

- Python 3
- PyTorch, torchvision
- SciPy (Hungarian matching via `linear_sum_assignment`)
- NumPy, matplotlib, PIL
- Jupyter Notebook (ran on Google Colab)

## Dataset

**Penn-Fudan Pedestrian Detection Dataset**: images with per-instance bounding box annotations. Pre-split into train/val/test using the text files in `splits/`.

## Prerequisites

```bash
pip install torch torchvision scipy numpy matplotlib pillow jupyter
```

Place the `PennFudanPed/` dataset folder in the same directory as the notebook.

## How to Run

```bash
jupyter notebook b2210356036.ipynb
```

The `main()` function runs all 4 ablation experiments sequentially and prints a comparison table with validation and test mAP@0.5, plus training time per epoch.

## Key Learnings

- Implemented Hungarian matching loss (classification + L1 bbox + GIoU) from scratch, which is the key insight that makes set-based detection (DETR) work
- Data augmentation (color jitter + horizontal flip) consistently improved mAP; the ablation confirmed its value even on a small dataset
- MobileNetV2 backbone was faster per epoch but ResNet18 achieved better mAP, illustrating the accuracy-efficiency trade-off in backbone selection
