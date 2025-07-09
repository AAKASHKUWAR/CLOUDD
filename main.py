# main.py
from utils import load_image, cloud_shadow_mask, visualize_masks

def main():
    image_path = "sample_image.tif"  # Make sure this file exists
    image, transform = load_image(image_path)

    cloud_mask, shadow_mask = cloud_shadow_mask(image)

    visualize_masks(image, cloud_mask, shadow_mask)
    print("✅ Cloud and shadow detection completed. Output saved to output.png.")

if __name__ == "__main__":
    main()
