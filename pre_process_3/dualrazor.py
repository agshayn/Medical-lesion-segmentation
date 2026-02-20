from scipy.ndimage import convolve
import numpy as np
import skimage
from skimage import io
from skimage import morphology 
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import interpolate
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import os

def matmax(img):

  """
  :param img : l'image RGB
  :return: tuple des masques (pour R, G et B de l'image) des pixels de poils
  """

  R = img[:,:,0]
  G = img[:,:,1]
  B = img[:,:,2]

  s0 = morphology.rectangle(50,10)
  s1 = morphology.rectangle(10,50)

  r0 = morphology.closing(R, footprint=s0)
  r1 = morphology.closing(R, footprint=s1)

  g0 = morphology.closing(G, footprint=s0)
  g1 = morphology.closing(G, footprint=s1)

  b0 = morphology.closing(B, footprint=s0)
  b1 = morphology.closing(B, footprint=s1)

  matmaxr = np.zeros(R.shape)
  matmaxg = np.zeros(R.shape)
  matmaxb = np.zeros(R.shape)
  nlin, ncol = R.shape

  for i in range(nlin):
    for j in range(ncol):
      matmaxr[i,j] = max(r0[i,j], r1[i,j])
      matmaxg[i,j] = max(g0[i,j], g1[i,j])
      matmaxb[i,j] = max(b0[i,j], b1[i,j])

  return (matmaxr, matmaxg, matmaxb)

def hair_mask(img, matmax):

  """
  :param img : l'image RGB
  :param matmax: tuple des trois masques de poils R, G et B
  :return: tuple des masques (pour R, G et B de l'image) des pixels de poils (avec des zones de poils élargies)
  """

  R = img[:,:,0]
  G = img[:,:,1]
  B = img[:,:,2]

  matmaxr, matmaxg, matmaxb = matmax
  Mr = np.zeros(matmaxr.shape)
  Mg = np.zeros(matmaxr.shape)
  Mb = np.zeros(matmaxr.shape)

  Mr[:,:] = np.abs(R[:,:]-matmaxr[:,:]) > 40
  Mg[:,:] = np.abs(G[:,:]-matmaxg[:,:]) > 40
  Mb[:,:] = np.abs(B[:,:]-matmaxb[:,:]) > 40

  square = morphology.rectangle(20, 20)
  Mr = morphology.binary_dilation(Mr, square)
  Mb = morphology.binary_dilation(Mb, square)
  Mg = morphology.binary_dilation(Mg, square)

  return (Mr, Mg, Mb)

#FONCTION PRISE SUR INTERNET 
def interpolate_missing_pixels(
        image: np.ndarray,
        mask: np.ndarray,
        method: str = 'nearest',
        fill_value: int = 0
):
    """
    :param image: a 2D image
    :param mask: a 2D boolean image, True indicates missing values
    :param method: interpolation method, one of
        'nearest', 'linear', 'cubic'.
    :param fill_value: which value to use for filling up data outside the
        convex hull of known pixel values.
        Default is 0, Has no effect for 'nearest'.
    :return: the image with missing values interpolated
    """
    
    h, w = image.shape[:2]
    xx, yy = np.meshgrid(np.arange(w), np.arange(h))

    known_x = xx[~mask]
    known_y = yy[~mask]
    known_v = image[~mask]
    missing_x = xx[mask]
    missing_y = yy[mask]

    interp_values = interpolate.griddata(
        (known_x, known_y), known_v, (missing_x, missing_y),
        method=method, fill_value=fill_value
    )

    interp_image = image.copy()
    interp_image[missing_y, missing_x] = interp_values

    return interp_image

def hairRemoval(img, mask):

  """
  :param img : l'image RGB
  :return: l'image sans les poils
  """
  
  matmax_ = matmax(img)
  (matmaxr, matmaxg, matmaxb) = matmax_
  (Mr, Mg, Mb) = hair_mask(img, matmax_)

  hairDetection = morphology.erosion(np.abs(img[:,:,0]-matmaxr), footprint=morphology.disk(12))
  if hairDetection.sum() / mask.sum() < 0.2:
    return img

  R = img[:,:,0]
  G = img[:,:,1]
  B = img[:,:,2]

  newR = interpolate_missing_pixels(R, Mr > 0)
  newB = interpolate_missing_pixels(B, Mb > 0)
  newG = interpolate_missing_pixels(G, Mg > 0)

  square = morphology.rectangle(20, 20)
  Rf = skimage.filters.median(newR, square)
  Gf = skimage.filters.median(newG, square)
  Bf = skimage.filters.median(newB, square)

  final_img = np.copy(img)
  final_img[:,:,0]=Rf
  final_img[:,:,1]=Gf
  final_img[:,:,2]=Bf

  return final_img
