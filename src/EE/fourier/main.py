import asyncio
import random

import numpy as np
import PIL.Image
from PIL import Image

try:
    from .. import utils
except ImportError:
    from EE import utils


def get_watermark_text():
    """Basic CLI prompt to enter text, Deprecated."""
    return input("Enter the watermark text: ")


def load_image():
    """Load Image object, Deprecated."""
    image_path = input("Enter the path to the image file: ")
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print("Image not found. Please check the path and try again.")
        return None


def shift_to_center(frequency_domain):  # noqa: D103
    return np.fft.fftshift(frequency_domain)


def shift_to_corners(frequency_domain):  # noqa: D103
    return np.fft.ifftshift(frequency_domain)


def fourier_transform_color(image):  # noqa: D103
    image_array = np.array(image)
    red, green, blue = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
    red_freq = shift_to_center(np.fft.fft2(red))
    green_freq = shift_to_center(np.fft.fft2(green))
    blue_freq = shift_to_center(np.fft.fft2(blue))
    return red_freq, green_freq, blue_freq


def embed_watermark_to_color_channel(magnitude, phase, watermark_array):
    """Encode watermark by colour channel."""
    # Embed watermark into magnitude
    magnitude[0:1, 0: watermark_array.shape[1]] = watermark_array

    # Print debug information
    # print("Debug: Portion of magnitude where watermark is embedded:")
    # print(magnitude[0:1, 0:watermark_array.shape[1]])
    print(
        f"Debug: Portion of magnitude where watermark is embedded:\n{magnitude[0:1, 0:watermark_array.shape[1]]}"
    )
    frequency_domain_watermarked = magnitude * np.exp(1j * phase)

    return frequency_domain_watermarked


def inverse_fourier_transform_color(red_freq, green_freq, blue_freq):  # noqa: D103
    red = np.fft.ifft2(shift_to_corners(red_freq))
    green = np.fft.ifft2(shift_to_corners(green_freq))
    blue = np.fft.ifft2(shift_to_corners(blue_freq))
    color_image_array = np.stack([np.real(red), np.real(green), np.real(blue)], axis=2)
    color_image_array = np.uint8(color_image_array)
    return Image.fromarray(color_image_array, "RGB")


def save_image(image, save_path):
    """Save PIL.Image.Image by path."""
    try:
        image.save(save_path)
        print(f"Watermarked image saved as '{save_path}'")

    except Exception as e:
        print(f"Failed to save image: {e}")


def encode_fourier(watermark_text, img_path, save_path):
    """Code to dncode watermark to the image."""
    if not isinstance(img_path, PIL.Image.Image):
        image = Image.open(img_path)
    else:
        image = img_path

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
        red_freq_watermarked = embed_watermark_to_color_channel(
            red_magnitude, red_phase, watermark_array
        )
        green_freq_watermarked = embed_watermark_to_color_channel(
            green_magnitude, green_phase, watermark_array
        )
        blue_freq_watermarked = embed_watermark_to_color_channel(
            blue_magnitude, blue_phase, watermark_array
        )
        # Save the frequency domain data to disk
        np.save(f"red_freq_watermarked_{watermark_text}.npy", red_freq_watermarked)

        print("Successfully embedded watermark into frequency domain.")
        print(
            f"Debug: Red frequency domain after watermark: {np.abs(red_freq_watermarked)[0, 0:10]}"
        )

        watermarked_image = inverse_fourier_transform_color(
            red_freq_watermarked, green_freq_watermarked, blue_freq_watermarked
        )
        print("Successfully transformed image back to spatial domain.")

        save_image(watermarked_image, save_path)

        loaded_image = Image.open(save_path)
        loaded_red_freq, _, _ = fourier_transform_color(loaded_image)
        print(f"Debug: Loaded red frequency domain: {np.abs(loaded_red_freq)[0, 0:10]}")
    else:
        print("Failed to load image. Exiting.")


class Fourier(utils.LibraryBase):
    """Class to run Fourier Library"""

    def __init__(self):
        super().__init__()
        self.enc_input = [
            {"field": "Watermark content", 'type': 'text_large', 'id': 'msg'},
            {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.dec_input = [
            {"field": "Image", 'type': 'image_button', 'id': 'img'},
            {"field": "Length of watermark content", 'type': 'text_small', 'id': 'len'}]
        self.enc_output = [{"type": "image_button", "id": "img_down"}, {'type': 'int', 'id': 'len'}]
        self.dec_output = [{"type": "msg", "id": "msg"}]

    async def routine(self, func_mode: utils.mode, data_input: dict):
        """Routine of running Fourier watermark."""
        # If both code have something in common, the proprtion of those code is here
        if func_mode == utils.MODE_ENCRYPTION:
            data = data_input['msg']
            pathname_gen = ''.join(random.choices('0123456789abcdef', k=32)) + '.tiff'
            encode_fourier(data, data_input['img'], pathname_gen)
            return {'img_down': pathname_gen, 'len': len(data)}

        if func_mode == utils.MODE_DECRYPTION:  # {'len':'4', 'img;<object: PIL.Image.Image>} -> {'msg':'test'}
            # data = fourier_transform_decoder.main(data_input['msg'],data_input["img"] )
            # return {'img_down': name}
            # disconnected code
            pass


if __name__ == "__main__":
    lib = Fourier()
    out_data = asyncio.run(lib.routine(utils.MODE_ENCRYPTION, {'msg': 'test', 'img': PIL.Image.open('img.png')}))
    out_data_2 = asyncio.run(
        lib.routine(utils.MODE_DECRYPTION, {'img': PIL.Image.open(out_data['img_down']), 'len': str(out_data['len'])}))
    print(out_data_2)
