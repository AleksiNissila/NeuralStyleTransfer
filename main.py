import glob
import random
import time
import image_fetch
import show_image
import gc

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image, ImageFilter

sharpen = False
img_index = 1
image_time = 10.0
style_image_size = 256
#stylized_image_size = (360, 640)
stylized_image_size = (1080, 1920)
model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
generated_folder_path = ['./generated_images/*.jpg']
style_folder_path = ['./style_images/style_images_' + str(style_image_size) + '/*.jpg']
style_image_path = ''

# Function for loading image from given path. Also converts it to right format.
def load_image(img_path):
    """
    Function for loading an image from specified path location

    :param img_path: The path to the image.
    :return: image as EagerTensor
    """
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

def get_random_img_path(path):
    """
    Function for getting a name of a randomized file from specified directory

    :param path: path containing the files
    :return: path to a random file from the inputted path
    """
    random_image_path = random.choice(glob.glob(random.choice(path)))
    return random_image_path

def tensor_to_image(tensor):
    """
    Function for converting a tensor-variable to PIL Image

    :param tensor: Image file as a tensor array
    :return: Image file as PIL Image
    """
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    img = Image.fromarray(tensor)
    return img


# Get first image from older generated images
# (only the first image of runtime is pre-generated)
first_image_path = get_random_img_path(generated_folder_path)
image_to_show = Image.open(first_image_path)

try:
    while True:
        # Show the image saved in image_to_show
        root = show_image.showPIL(image_to_show)

        # After the image is presented, start generating the next image

        # Get random image and random style
        content_image_path = image_fetch.get_image(img_index)


        # Show older, already generated image if image fetching does not work
        if (content_image_path is None):
            impath = get_random_img_path(generated_folder_path)
            image_to_show = Image.open(impath)

            # Show a new image every 30 seconds
            time.sleep(image_time - time.time() % image_time)

            # Close the old image to prepare presenting next image
            show_image.destroyPIL(root)

        # If image fetch worked properly, proceed normally with processing
        else:

            style_image_path = get_random_img_path(style_folder_path)

            # You can specify style or content image  for testing purposes by uncommenting and specifying the path to a specific image
            #style_image_path = './style_images/style_images_256/M-Maybe (Custom).jpg'
            #content_image_path = './content_images\img_test4.jpg'

            # Load content and style images
            content_image = load_image(content_image_path)
            content_image = tf.image.resize(content_image, stylized_image_size)
            style_image = load_image(style_image_path)

            # Generate image using pretrained model
            stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
            image = tensor_to_image(stylized_image[0])

            del content_image, style_image, stylized_image
            gc.collect()

            # Save image temporarily before upscaling
            imname = 'img_' + str(img_index)
            impath = './generated_images/' + imname + '.jpg'
            image.save(impath, format='PNG')

            image = Image.open(impath)

            # Upscaling when images are processed as low resolution
            if sharpen:
                image\
                    .resize((1920, 1080), Image.BICUBIC)\
                    .filter(ImageFilter.EDGE_ENHANCE_MORE)\
                    .filter(ImageFilter.SHARPEN)\
                    .filter(ImageFilter.MedianFilter(size=3))


            # Save generated image to a folder
            imname = 'img_' + str(img_index)
            impath = './generated_images/' + imname + '.jpg'
            image.save(impath, format='PNG')

            image_to_show = image
            del image
            gc.collect()

            time.sleep(image_time - time.time() % image_time)

            if (img_index == 10):
                img_index = 1
            else:
                img_index += 1

            # Close the old image
            try:
                show_image.destroyPIL(root)
            except:
                pass


except KeyboardInterrupt:
    show_image.destroyPIL(root)
