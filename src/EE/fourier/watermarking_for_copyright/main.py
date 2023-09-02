from PIL import Image
import numpy as np


def get_watermark_text():
    return input("Enter the watermark text: ")


def load_image():
    image_path = input("Enter the path to the image file: ")
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print("Image not found. Please check the path and try again.")
        return None
def fourier_transform(image):
    grayscale_image = image.convert("L")
    image_matrix = np.array(grayscale_image)

    frequency_domain = np.fft.fft2(image_matrix)

    return frequency_domain

def embed_watermark(frequency_domain, watermark_text):
    watermark_array = np.array([[ord(char) for char in watermark_text]])

    frequency_domain[0:1,0:watermark_array.shape[1]] = watermark_array

    return frequency_domain

def inverse_fourier_transform(frequency_domain):
    spatial_domain = np.fft.ifft2(frequency_domain)
    spatial_domain = np.real(spatial_domain)
    spatial_domain = np.uint8(spatial_domain)

    return Image.fromarray(spatial_domain, "L")

def save_image(image, watermark_text):
    try:
        image.save(f"watermaked_{watermark_text}.png")
        print(f"Watermarked image saved as 'watermaked_{watermark_text}.png'")
    except Exception as e:
        print(f"Failed to save image: {e}")

def main():
    watermark_text = get_watermark_text()
    image = load_image()

    if image:
        print(f"Successfully loaded image. Watermark text is: {watermark_text}")

        frequency_domain_image = fourier_transform(image)
        print("Successfully loaded image to frequency domain.")

        watermark_frequency = embed_watermark(frequency_domain_image, watermark_text)
        print("Successfully embedded watermark into frequency domain.")

        watermarked_image = inverse_fourier_transform(watermark_frequency)
        print("Successfully transformed image back to spatial domain.")

        save_image(watermarked_image,watermark_text)
    else:
        print("Failed to load image. Exiting.")


if __name__ == "__main__":
    main()
