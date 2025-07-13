import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
from PIL import Image
import matplotlib.pyplot as plt

def convert_rgb_to_tiff(input_path, output_dir):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{filename}_rgb_as_satellite.tif")

    img = Image.open(input_path).convert("RGB").resize((256, 256))
    rgb = np.array(img).astype("float32") / 255.0

    red = rgb[:, :, 0]
    green = rgb[:, :, 1]
    nir = rgb[:, :, 2]  # using Blue as fake NIR

    transform = from_origin(0, 0, 10, 10)

    os.makedirs(output_dir, exist_ok=True)
    with rasterio.open(
        output_path, "w", driver="GTiff", height=256, width=256,
        count=3, dtype="float32", transform=transform
    ) as dst:
        dst.write(red, 1)
        dst.write(green, 2)
        dst.write(nir, 3)

    print(f"TIFF created: {output_path}")
    return output_path

def load_image(path):
    with rasterio.open(path) as src:
        red = src.read(1).astype(np.float32)
        green = src.read(2).astype(np.float32)
        nir = src.read(3).astype(np.float32)
        red /= red.max()
        green /= green.max()
        nir /= nir.max()
        return {'red': red, 'green': green, 'nir': nir}, src.transform

def cloud_shadow_mask(image):
    red = image['red']
    green = image['green']
    nir = image['nir']

    brightness = (red + green + nir) / 3.0
    ndvi = (nir - red) / (nir + red + 1e-6)

    cloud_mask = (brightness > 0.6) & (ndvi < 0.2)
    shadow_mask = (brightness < 0.2) & (ndvi < 0.2) & (~cloud_mask)

    return cloud_mask, shadow_mask, ndvi

def visualize_masks(image, cloud_mask, shadow_mask, ndvi, output_dir, base_name):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 3, 1)
    plt.title("NIR Band (Input)")
    plt.imshow(image['nir'], cmap='gray')
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.title("Cloud Mask (Improved)")
    plt.imshow(cloud_mask, cmap='Reds')

    plt.subplot(1, 3, 3)
    plt.title("Shadow Mask (Improved)")
    plt.imshow(shadow_mask, cmap='Blues')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{base_name}_output.png"))
    plt.show()

    plt.figure()
    plt.title("NDVI (Debug View)")
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar()
    plt.savefig(os.path.join(output_dir, f"{base_name}_ndvi_debug.png"))
    plt.show()

def main():
    image_path = r"C:\Users\Dell\Documents\BAH\Cloud_\input_image\europe.jpg"  # Set your default input image here
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = os.path.join("output_image", base_name)

    print(f"Processing image: {image_path}")

    tiff_path = convert_rgb_to_tiff(image_path, output_dir)
    image, _ = load_image(tiff_path)
    cloud_mask, shadow_mask, ndvi = cloud_shadow_mask(image)

    visualize_masks(image, cloud_mask, shadow_mask, ndvi, output_dir, base_name)

    total_pixels = np.prod(cloud_mask.shape)
    cloud_pixels = np.sum(cloud_mask)
    cloud_percent = (cloud_pixels / total_pixels) * 100

    print(f"Cloud Cover: {cloud_percent:.2f}%")
    if cloud_percent >= 10:
        print("Cloud is detected")
    if cloud_percent > 15:
        print("Cloudy image detected (cloud cover > 15%)")
    else:
        print("Cloud cover acceptable")

    print(f"Output saved in folder: {output_dir}")

# Run directly
main()
