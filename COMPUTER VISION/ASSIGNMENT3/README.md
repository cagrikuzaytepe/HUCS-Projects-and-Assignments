# Assignment 3 — Image Colorization with Deep Convolutional Neural Networks

Progressive implementation of image colorization models, from a baseline Encoder-Decoder to a GAN with PatchGAN discriminator. The task is to predict the a* and b* color channels from a grayscale L* input in CIELAB color space.
Part of **BBM418 / AIN433 – Computer Vision Lab**, Hacettepe University.

## Tech Stack

- Python 3
- PyTorch, torchvision
- scikit-image (CIELAB conversion, PSNR/SSIM metrics)
- PIL, NumPy, matplotlib
- Jupyter Notebook (ran on Google Colab with T4 GPU)

## Dataset

Custom dataset of 5,000 natural scene images (hosted on Google Drive). Split: 4,000 train / 1,000 validation. Images resized to 256×256.

## Prerequisites

```bash
pip install torch torchvision scikit-image pillow numpy matplotlib tqdm jupyter
```

GPU (CUDA) recommended. Mount Google Drive in Colab and update `DATASET_PATH`.

## How to Run

Open in Google Colab and run cells in order. Update `DATASET_PATH` to your Drive folder.

```python
DATASET_PATH = '/content/drive/MyDrive/BBM418_Assignment3/images/color'
```

All models are trained sequentially. Saved checkpoints are stored in `/content` by default.

## Key Learnings

- Working in CIELAB color space is essential: the L* channel captures structure, and the model only needs to predict the 2 chromatic channels (a*, b*)
- L1 loss produces safe, desaturated colors by averaging over all plausible color solutions; perceptual loss and adversarial training produce significantly more vivid output
- The GAN model (ResNet backbone + PatchGAN discriminator) achieved the best visual quality; the 70×70 patch discriminator forces local texture realism rather than global averaging
