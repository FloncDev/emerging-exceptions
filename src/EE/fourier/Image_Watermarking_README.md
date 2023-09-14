# Image Watermarking using Fourier Transform

## Encoder

### Overview
The encoder program takes an image and a watermark text from the user. It then performs the following steps:
1. Converts the image to the frequency domain using Fourier Transform for each color channel (red, green, blue).
2. Embeds the watermark into the magnitude of the frequency domain.
3. Transforms the image back to the spatial domain and saves it.

### How to Use
1. Run the program.
2. Enter the watermark text when prompted.
3. Enter the path to the image file you want to watermark.

### Code Explanation
- `get_watermark_text()`: Gets watermark text from the user.
- `load_image()`: Loads an image from a file path given by the user.
- `fourier_transform_color()`: Performs Fourier Transform on each color channel.
- `embed_watermark_to_color_channel()`: Embeds the watermark into the magnitude of the frequency domain.
- `inverse_fourier_transform_color()`: Performs inverse Fourier Transform to get the image back to the spatial domain.
- `save_image()`: Saves the watermarked image.

---

## Decoder

### Overview
The decoder program extracts the watermark text from a watermarked image. It uses the frequency domain data saved during the encoding process.

### How to Use
1. Run the program.
2. Enter the watermark text that was used for encoding when prompted.
3. Enter the path to the watermarked image file.

### Code Explanation
- `load_image()`: Loads the watermarked image.
- `fourier_transform_color()`: Performs Fourier Transform on each color channel of the image.
- `extract_watermark()`: Extracts the watermark from the magnitude of the frequency domain.
- `main()`: Orchestrates the watermark extraction process.

The decoder does not read the watermark directly from the watermarked image. Instead, it loads the frequency domain data from a `.npy` file saved during the encoding process.
