
from PIL import Image
import os
from send2trash import send2trash


def move_to_recycle_bin(path):
    if not os.path.isdir(path):
        raise ValueError(f"路径 {path} 不是有效的目录")
    
    # 遍历目录中的所有文件和子目录
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        # 检查是文件还是目录，并移动到回收站
        if os.path.isfile(item_path):
            send2trash(item_path)
        elif os.path.isdir(item_path):
            send2trash(item_path)
        else:
            print(f"无法处理 {item_path}")


def generate_image():
    width, height = 1280, 720
    image = Image.new('RGB', (width, height), color='black')
    return image


def run():
    
    dir1 = './image'
    dir2 = './out'

    move_to_recycle_bin(dir1)
    move_to_recycle_bin(dir2)

    from cap_fuck import update_img_path
    image = generate_image()
    image.save(update_img_path, 'JPEG')


if __name__ == "__main__":
    run()
