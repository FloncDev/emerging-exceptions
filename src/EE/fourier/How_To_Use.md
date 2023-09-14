# User Guide: How to Watermark Your Digital Art or Photography Using Fourier Transform

## Introduction

Hello, dear artist or photographer! Want to protect your magnificent creations with some tech magic? You're in the right place! This guide will walk you through watermarking your images using a technique called Fourier Transform. This method embeds the watermark into the frequency domain of the image, making it difficult to remove without specialized knowledge. In simpler terms, it's a robust way to safeguard your work without affecting its visual quality.

---

## Requirements

- Python installed on your computer
- The encoder and decoder scripts
- The image you want to watermark (in `.png`, `.jpg`, or `.tiff` formats)

---

## Step-by-Step Instructions

### Watermarking Your Image (Encoding)

1. **Open the Terminal or Command Prompt**
    - Navigate to the folder where the encoder script is located.

2. **Run the Encoder Script**
    - Type `python encoder.py` and press Enter.

3. **Enter the Watermark Text**
    - You'll be prompted to enter the text you want to use as a watermark. This could be your name, brand, or any other identifying info.
  
4. **Select the Image File**
    - You'll be prompted to provide the path to the image file you want to watermark. Enter the full path to the image.

5. **Check for Success**
    - If everything goes well, you'll see messages indicating that the watermark has been successfully embedded. The watermarked image will be saved in the same folder with the suffix `_watermarked`.

### Verifying the Watermark (Decoding)

1. **Open the Terminal or Command Prompt**
    - Navigate to the folder where the decoder script is located.

2. **Run the Decoder Script**
    - Type `python decoder.py` and press Enter.

3. **Enter the Original Watermark Text**
    - You'll be prompted to enter the original text that was used for watermarking. Make sure to enter it exactly as you did during the encoding process.

4. **Select the Watermarked Image File**
    - You'll be prompted to provide the path to the watermarked image file. Enter the full path to the image.

5. **Check for Success**
    - If all goes well, the script will display the watermark text extracted from the image. It should match the text you originally entered.

---

## Final Thoughts

And there you have it! You've successfully watermarked your artwork using Fourier Transform methods. While this watermark is not visible, it's embedded in a technically complex way that makes it difficult to remove, providing an extra layer of security for your creations.

Remember, this is not a 100% foolproof method, but it adds a layer of protection that can deter unauthorized use of your work.

