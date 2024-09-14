
from PIL import Image

def generate_image():
    width, height = 1280, 720
    image = Image.new('RGB', (width, height), color='black')
    return image
from cap_fuck import update_img_path
image = generate_image()
image.save(update_img_path, 'JPEG')

