# Assignment 3 — Image Classification: CNN from Scratch and Transfer Learning

Custom CNN implementation for 10-class animal image classification, followed by transfer learning experiments with ResNet18 and MobileNetV2.
Part of **BBM409 – Machine Learning**, Hacettepe University.

## Tech Stack

- Python 3
- PyTorch, torchvision
- scikit-learn (metrics)
- NumPy, matplotlib, pandas
- Jupyter Notebook (ran on Kaggle GPU)

## Dataset

**Animal-10** (10-class animal dataset): dog, horse, elephant, butterfly, chicken, cat, cow, sheep, spider, squirrel. 300 training / 75 validation / 75 test samples per class (3,750 total).

## Prerequisites

```bash
pip install torch torchvision scikit-learn numpy matplotlib pandas jupyter
```

GPU (CUDA) recommended. The notebook was developed on Kaggle with a T4 GPU.

## How to Run

```bash
jupyter notebook assignment3.ipynb
```

Update `dataset_path` to point to your local dataset. The notebook trains three model variants (CNN from scratch, ResNet18 fine-tuned in 3 configurations, MobileNetV2) and evaluates them on the test set.

## Key Learnings

- Designed a 4-block CNN (Conv → BN → MaxPool) with adaptive average pooling; achieved ~67% test accuracy on a 10-class problem
- Fine-tuning pre-trained ResNet18 (all layers unfrozen) outperformed the custom CNN (~74% vs 67%), confirming the value of ImageNet pre-trained features
- MobileNetV2 fine-tuned end-to-end achieved the best result (~83%), demonstrating that lightweight architectures with pre-trained weights generalize well on small datasets
