import requests
import gc

def get_image(index):
    """
    Function for getting a random image from Unsplash.com

    :param index: Index of the image (just for naming purposes when saving image to a folder)
    :return: Path to the saved image in a folder
    """
    imname = 'img_' + str(index)
    impath = './content_images/' + imname + '.jpg'

    try:
        # Get an image from internet, save it to path and return path
        with open(impath, 'wb') as handle:
                response = requests.get('https://source.unsplash.com/random/1920x1080', stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                del response, handle
                gc.collect()
        return impath

    except:
        print("error in fetching image")
        pass



