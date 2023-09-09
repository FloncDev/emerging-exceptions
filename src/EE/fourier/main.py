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
def shift_to_center(frequency_domain):
    return np.fft.fftshift(frequency_domain)

def shift_to_corners(frequency_domain):
    return np.fft.ifftshift(frequency_domain)



def fourier_transform_color(image):
    image_array = np.array(image)
    red, green, blue = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
    red_freq = shift_to_center(np.fft.fft2(red))
    green_freq = shift_to_center(np.fft.fft2(green))
    blue_freq = shift_to_center(np.fft.fft2(blue))
    return red_freq, green_freq, blue_freq



def embed_watermark_to_color_channel(magnitude, phase, watermark_array):
    # Embed watermark into magnitude
    magnitude[0:1, 0:watermark_array.shape[1]] = watermark_array

    # Print debug information
    # print("Debug: Portion of magnitude where watermark is embedded:")
    # print(magnitude[0:1, 0:watermark_array.shape[1]])
    print(f"Debug: Portion of magnitude where watermark is embedded:\n{magnitude[0:1, 0:watermark_array.shape[1]]}")
    frequency_domain_watermarked = magnitude * np.exp(1j * phase)

    return frequency_domain_watermarked


def inverse_fourier_transform_color(red_freq, green_freq, blue_freq):
    red = np.fft.ifft2(shift_to_corners(red_freq))
    green = np.fft.ifft2(shift_to_corners(green_freq))
    blue = np.fft.ifft2(shift_to_corners(blue_freq))
    color_image_array = np.stack([np.real(red), np.real(green), np.real(blue)], axis=2)
    color_image_array = np.uint8(color_image_array)
    return Image.fromarray(color_image_array, 'RGB')


def save_image(image, watermark_text):
    try:
        image.save(f"watermaked_{watermark_text}.tiff")
        print(f"Watermarked image saved as 'watermaked_{watermark_text}.tiff'")

    except Exception as e:
        print(f"Failed to save image: {e}")

def main():
    watermark_text = get_watermark_text()
    image = load_image()

    if image:
        print(f"Successfully loaded image. Watermark text is: {watermark_text}")

        red_freq, green_freq, blue_freq = fourier_transform_color(image)
        print("Successfully loaded image to frequency domain.")


        watermark_array = np.array([[ord(char) for char in watermark_text]])

        # Separate magnitude and phase for each color channel
        red_magnitude, red_phase = np.abs(red_freq), np.angle(red_freq)
        green_magnitude, green_phase = np.abs(green_freq), np.angle(green_freq)
        blue_magnitude, blue_phase = np.abs(blue_freq), np.angle(blue_freq)

        # Embed the watermark and get the watermarked frequency domain
        red_freq_watermarked = embed_watermark_to_color_channel(red_magnitude, red_phase, watermark_array)
        green_freq_watermarked = embed_watermark_to_color_channel(green_magnitude, green_phase, watermark_array)
        blue_freq_watermarked = embed_watermark_to_color_channel(blue_magnitude, blue_phase, watermark_array)
        # Save the frequency domain data to disk
        np.save(f"red_freq_watermarked_{watermark_text}.npy", red_freq_watermarked)

        print("Successfully embedded watermark into frequency domain.")
        print(f"Debug: Red frequency domain after watermark: {np.abs(red_freq_watermarked)[0, 0:10]}")

        watermarked_image = inverse_fourier_transform_color(
            red_freq_watermarked, green_freq_watermarked, blue_freq_watermarked
        )
        print("Successfully transformed image back to spatial domain.")

        save_image(watermarked_image, watermark_text)

        loaded_image = Image.open(f"watermaked_{watermark_text}.tiff")
        loaded_red_freq, _, _ = fourier_transform_color(loaded_image)
        print(f"Debug: Loaded red frequency domain: {np.abs(loaded_red_freq)[0, 0:10]}")
    else:
        print("Failed to load image. Exiting.")

if __name__ == "__main__":
    main()