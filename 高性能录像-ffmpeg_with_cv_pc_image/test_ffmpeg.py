import subprocess

def capture_frame_from_camera():
    # ffmpeg 命令
    ffmpeg_command = [
        'ffmpeg', 
        '-f', 'dshow', 
        '-i', 'video=WEB CAM', 
        '-frames:v', '1', 
        './out/output_image.jpg'
    ]
    
    # 执行 ffmpeg 命令
    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("图像捕获并保存为 output_image.jpg")

# 调用函数
capture_frame_from_camera()
