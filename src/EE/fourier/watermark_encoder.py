import PIL.Image
import numpy as np
from PIL import Image


def embed_watermark(image_in, watermark_text):
    imgarr = np.array(image_in)
    watermark_data = ''.join(format(ord(char), '08b')
                             for char in watermark_text)
    i = 0
    for x in range(imgarr.shape[0]):
        for y in range(imgarr.shape[1]):
            pixel = list(imgarr[x, y])
            for n in range(3):
                if i < len(watermark_data):
                    pixel[n] = int(format(pixel[n], '08b')[
                                   :-1] + watermark_data[i], 2)
                    i += 1
            imgarr[x, y] = tuple(pixel)
    # cv2.imwrite("watermarked_image.png", image)
    return Image.fromarray(imgarr)

    # print("Watermark embedded and saved to watermarked_image.png.")


def main(image, watermark_text):
    out_image = embed_watermark(image, watermark_text)
    return out_image

if __name__ == "__main__":
    image_path = input('Image path for the original image: ')
    text = input('Input text that you want to watermark: ')
    image_obj = main(PIL.Image.open(image_path), text)
    out_path = input('The output path for the image:')
    image_obj.save(out_path)
    print('For reminder, You will require the original image, the watermarked image '+\
          'and the length of the watermarked text to get the text you watermarked.')
    print(f"Your length of watermark is:{len(text)}")
