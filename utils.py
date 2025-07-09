# utils.py
import numpy as np
import rasterio
import matplotlib.pyplot as plt

def load_image(path):
    with rasterio.open(path) as src:
        red = src.read(1).astype(np.float32) / 10000
        green = src.read(2).astype(np.float32) / 10000
        nir = src.read(3).astype(np.float32) / 10000
        transform = src.transform
    return {'red': red, 'green': green, 'nir': nir}, transform

def cloud_shadow_mask(image):
    red = image['red']
    green = image['green']
    nir = image['nir']

    # Cloud = bright in all bands
    cloud_mask = (red > 0.2) & (green > 0.2) & (nir > 0.3)

    # Shadow = very dark in NIR and not cloud
    shadow_mask = (nir < 0.1) & (~cloud_mask)

    return cloud_mask, shadow_mask

def visualize_masks(image, cloud_mask, shadow_mask):
    combined = cloud_mask.astype(np.uint8) * 1 + shadow_mask.astype(np.uint8) * 2

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 3, 1)
    plt.title("NIR Band")
    plt.imshow(image['nir'], cmap='gray')
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.title("Cloud Mask")
    plt.imshow(cloud_mask, cmap='Reds')

    plt.subplot(1, 3, 3)
    plt.title("Shadow Mask")
    plt.imshow(shadow_mask, cmap='Blues')

    plt.tight_layout()
    plt.savefig("output.png")
    plt.show()
