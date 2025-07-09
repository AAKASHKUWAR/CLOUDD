# generate_fake_image.py
import numpy as np
import rasterio
from rasterio.transform import from_origin

# Create synthetic Red, Green, NIR bands
width, height = 256, 256
red = np.random.rand(height, width) * 10000
green = np.random.rand(height, width) * 10000
nir = np.random.rand(height, width) * 10000

transform = from_origin(0, 0, 10, 10)  # dummy geo-transform

with rasterio.open(
    'sample_image.tif',
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=3,
    dtype='float32',
    transform=transform
) as dst:
    dst.write(red.astype('float32'), 1)   # Red band
    dst.write(green.astype('float32'), 2) # Green band
    dst.write(nir.astype('float32'), 3)   # NIR band

print("✅ sample_image.tif generated successfully.")
