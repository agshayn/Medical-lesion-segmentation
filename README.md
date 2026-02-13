# IM01 - Segmentation de Lésions Cutanées 🩺📸

> **Projet académique - Télécom Paris (2025-2026)** > **Auteurs :** Théophile NADIEDJOA & Agshay NADANAKUMAR  
> **Encadrant :** M. Pietro GORI  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Scikit-Image](https://img.shields.io/badge/Library-Scikit--Image-orange) ![Status](https://img.shields.io/badge/Status-Completed-success)

## 📋 Description

Ce projet vise à développer une chaîne de traitement d'image automatisée pour la segmentation de lésions cutanées (mélanomes et nævus) à partir d'images dermoscopiques.

**La contrainte majeure :** Utilisation exclusive de techniques de **traitement d'image classique** (Computer Vision).  
🚫 **Interdiction stricte d'utiliser du Deep Learning** (pas de CNN, U-Net, etc.).

L'objectif est de produire un masque binaire précis isolant la lésion pour aider au diagnostic médical (CAD - Computer Aided Diagnosis).

---

## 🛠️ Méthodologie

Nous avons implémenté et comparé trois approches distinctes pour segmenter les lésions :

### 1. Prétraitement (Preprocessing)
Avant la segmentation, chaque image subit un nettoyage rigoureux :
* **Suppression du cadre noir (Vignettage) :** Détection adaptative du disque de peau via composantes connexes.
* **Suppression des poils (Hair Removal) :** Algorithme **"Macro-DullRazor"** amélioré (Fermeture morphologique avec éléments structurants larges et reconstruction par interpolation).

### 2. Algorithmes de Segmentation
Nous avons développé et testé 3 méthodes :

| Méthode | Type | Description |
| :--- | :--- | :--- |
| **Otsu Multi-Canal** | Histogramme | Seuillage automatique optimal sur les canaux R, G et B combinés, affiné par contours actifs (Chan-Vese). |
| **LBP Clustering** | Texture | Utilisation des **Local Binary Patterns** (Texture) et de l'espace couleur **CIE Lab**, segmentés par **K-Means**. |
| **SRM (Statistical Region Merging)** | Région | Fusion statistique de régions basée sur la luminosité, le contraste et la saturation (optimisé pour la peau). |

### 3. Post-traitement
* Nettoyage morphologique (Ouverture/Fermeture).
* Remplissage des trous (Hole filling).
* Lissage des bords.

---

## 📊 Résultats

Les méthodes ont été évaluées via le score **Dice**.

* **Meilleure méthode :** L'approche par Texture (**LBP Clustering**) offre le meilleur compromis robustesse/précision.
* **Otsu :** Très rapide et efficace sur les lésions contrastées, mais sensible aux ombres.
* **SRM :** Performant sur les cas simples, mais décroche sur les mélanomes complexes (hétérogènes).

---

## 💻 Installation et Utilisation

### Pré-requis
Le projet nécessite Python et les librairies scientifiques classiques.

```bash
pip install numpy matplotlib scikit-image scipy scikit-learn opencv-python-headless
```

### Clonez ce dépot
```bash
git clone https://github.com/agshayn/Medical-lesion-segmentation.git
cd Medical-lesion-segmentation/segmentation
```

### Lancez le notebook princpal
```bash
jupyter notebook code_final.ipynb
```
