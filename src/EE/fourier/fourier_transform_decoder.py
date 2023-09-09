from PIL import Image
import numpy as np

def load_image():
    image_path = input("Enter the path to the watermarked image file: ")
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print("Image not found. Exiting.")
        exit()

def fourier_transform_color(image):
    image_array = np.array(image)
    red, green, blue = image_array[:,:,0], image_array[:,:,1], image_array[:,:,2]
    red_freq = np.fft.fft2(red)
    green_freq = np.fft.fft2(green)
    blue_freq = np.fft.fft2(blue)
    return red_freq, green_freq, blue_freq

def extract_watermark(frequency_domain, watermark_length):
    magnitude = np.abs(frequency_domain)
    watermark_data = magnitude[0, 0:watermark_length]
    print(f"Debug: Extracted data from magnitude: {watermark_data}")
    watermark_text = ''.join([chr(int(round(x))) for x in watermark_data])
    return watermark_text



def main():
    watermark_text = input("Enter the watermark text that was used for encoding: ")
    image = load_image()
    watermark_length = len(watermark_text)

    try:
        loaded_red_freq_watermarked = np.load(f"red_freq_watermarked_{watermark_text}.npy")
        watermark_text_red = extract_watermark(loaded_red_freq_watermarked, watermark_length)
        print(f"Extracted watermark text from the red channel is: {watermark_text_red}")
    except FileNotFoundError:
        print("Frequency domain data not found. Exiting.")
        exit()

if __name__ == "__main__":
    main()
