from flask import Flask, render_template, redirect, url_for, send_file
import io
from PIL import Image
import base64
import numpy as np
from cap_ffmpeg_no_pc_image import VideoRecorder, update_img_path, cap_index
# from mute import mute_windows

# mute_windows()


app = Flask(__name__)

recorder = VideoRecorder()

def get_image_data():
    image = Image.open(update_img_path)
    original_size = image.size
    new_size = (original_size[0] // 3, original_size[1] // 3)
    image = image.resize(new_size, Image.ANTIALIAS)
    # 保存图像到内存
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)  # 将游标移动到流的开头
    # 将图像转换为 Base64 格式
    image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return image_data

# 打开按钮的后台函数
@app.route('/open', methods=['POST'])
def open_action():
    print("打开操作执行")
    result = recorder.start()
    image_data = get_image_data()
    if result:
        text = '正在打开'
    else:
        text = '摄像头被占用'
    return render_template('index.html', image_data=image_data, text=text)

# 关闭按钮的后台函数
@app.route('/close', methods=['POST'])
def close_action():
    print("关闭操作执行")
    recorder.stop()
    image_data = get_image_data()
    return render_template('index.html', image_data=image_data, text='正在关闭')

# 更新按钮的后台函数
@app.route('/update', methods=['POST'])
def update_action():
    print("更新操作执行")
    # image = generate_image()
    image_data = get_image_data()
    if recorder.is_recording:
        text = '运行中, 摄像头序号={}, 帧率={}'.format(cap_index, recorder.curr_fps)
    else:
        text = '停止中'
    return render_template('index.html', image_data=image_data, text=text)

# 退出按钮的后台函数
@app.route('/exit', methods=['POST'])
def exit_action():
    print("退出操作执行")
    recorder.quit()
    # 你可以在这里执行一些清理操作
    return redirect(url_for('index'))

# 首页，包含四个按钮
@app.route('/')
def index():
    image_data = get_image_data()
    return render_template('index.html', image_data=image_data, text="初始化")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
