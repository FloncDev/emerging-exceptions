import cv2
import numpy as np

def extract_watermark(watermarked_image, original_image, watermark_length):
    watermarked_image = np.array(watermarked_image)
    original_image = np.array(original_image)
    if watermarked_image is None or original_image is None:
        print("Could not open one of the images. Check the paths.")
        return None

    extracted_data = []
    for x in range(watermarked_image.shape[0]):
        for y in range(watermarked_image.shape[1]):
            pixel = list(watermarked_image[x, y])
            original_pixel = list(original_image[x, y])
            for n in range(3):
                extracted_data.append(bin(pixel[n])[-1])

    # Validate and convert the binary string to characters
    extracted_watermark = ''.join(
        [chr(int(''.join([str(bit) for bit in extracted_data[i:i + 8]]), 2))
         for i in range(0, watermark_length * 8, 8) if ''.join(extracted_data[i:i + 8]).isdigit()]
    )

    return extracted_watermark

# def main():
#     watermarked_image_path = input("Enter the path to the watermarked image file: ")
#     original_image_path = input("Enter the path to the original image file: ")
#     watermark_length = int(input("Enter the length of the watermark text: "))

#     extracted_watermark = extract_watermark(watermarked_image_path, original_image_path, watermark_length)
#     print(f"Extracted watermark is: {extracted_watermark}")

# if __name__ == "__main__":
#     main()
