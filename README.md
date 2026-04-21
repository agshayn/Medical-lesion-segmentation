# IM01 - Skin Lesion Segmentation

> **Academic project - Télécom Paris (2025-2026)**
> **Authors:** Théophile NADIEDJOA & Agshay NADANAKUMAR
> **Supervisor:** M. Pietro GORI

## Description

This project aims to develop an automated image processing pipeline for the segmentation of skin lesions (melanomas and nevi) from dermoscopic images.

**Key constraint:** Exclusive use of **classical image processing** techniques (Computer Vision).
**Deep Learning is strictly forbidden** (no CNN, U-Net, etc.).

The goal is to produce an accurate binary mask isolating the lesion to assist medical diagnosis (CAD - Computer Aided Diagnosis).

---

## Methodology

We implemented and compared three distinct approaches to segment the lesions:

### 1. Preprocessing

Before segmentation, each image undergoes rigorous cleaning:

- **Black frame removal (Vignetting):** Adaptive detection of the skin disk via connected components.
- **Hair removal:** Improved **"Macro-DullRazor"** algorithm (morphological closing with large structuring elements and interpolation-based reconstruction).

### 2. Segmentation Algorithms

We developed and tested 3 methods:

| Method | Type | Description |
| :--- | :--- | :--- |
| **Multi-Channel Otsu** | Histogram | Optimal automatic thresholding on combined R, G and B channels, refined by active contours (Chan-Vese). |
| **LBP Clustering** | Texture | Uses **Local Binary Patterns** (texture) and the **CIE Lab** color space, segmented by **K-Means**. |
| **SRM (Statistical Region Merging)** | Region | Statistical region merging based on brightness, contrast, and saturation (optimized for skin). |

### 3. Post-processing

- Morphological cleanup (Opening/Closing).
- Hole filling.
- Edge smoothing.

---

## Results

Methods were evaluated using the **Dice score**.

- **Best method:** The texture-based approach (**LBP Clustering**) offers the best robustness/precision trade-off.
- **Otsu:** Very fast and effective on high-contrast lesions, but sensitive to shadows.
- **SRM:** Performs well on simple cases, but struggles with complex (heterogeneous) melanomas.

---

## Installation & Usage

### Requirements

The project requires Python and standard scientific libraries.

```bash
pip install numpy matplotlib scikit-image scipy scikit-learn opencv-python-headless
```

### Clone the repository

```bash
git clone https://github.com/agshayn/Medical-lesion-segmentation.git
cd Medical-lesion-segmentation/segmentation
```

### Run the main notebook

```bash
jupyter notebook code_final.ipynb
```
