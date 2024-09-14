import time
import datetime
import subprocess
import cv2
update_img_path = './image/pc.jpg'

width = 2560
height = 1440

# cap_name = "BisonCam,NB Pro"
# cap_index = 0

cap_name = 'WEB CAM'
cap_index = 1


class VideoRecorder:
    def __init__(self):
        print("录像程序正在初始化")
        self.default_fps = 30
        self.default_resolution = f"{width}x{height}"
        self.default_cap_name = cap_name
        self.default_cap_index = cap_index

        self.is_recording = False
        self.curr_fps = 0
        self.out_dir = './out'
        self.process = None
        print("录像程序初始化完成")
    
    def make_avi_file_name(self):
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 格式化时间为 "yyyy-mm-dd-hhmmss" 格式
        file_name = current_time.strftime("%Y-%m-%d-%H%M%S")
        file_name += '.avi'
        return file_name

    def open_recording(self):
        self.is_recording = True
    def close_recording(self):
        self.is_recording = False
    
    def start(self):
        if not self.is_recording:
            if not self.check_camera_status(self.default_cap_index):
                print(f"摄像头 {self.default_cap_index} 被占用")
                return False
            else:
                self.open_recording()
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-f', 'dshow',  # 使用 DirectShow 捕获摄像头
                    '-i', f'video={self.default_cap_name}',  # 替换为你的摄像头设备名称
                    '-r', str(self.default_fps),  # 设置帧率
                    '-s', self.default_resolution,  # 设置分辨率
                    '-q:v', '1',                       # 设置视频质量
                    self.out_dir + '/' + self.make_avi_file_name()  # 输出文件名
                ]
                self.process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
                print(f"摄像头首次启动")
                return True
        else:
            print(f"摄像头已经启动")
            return True

    def stop(self):
        if self.is_recording:
            self.close_recording()
            if self.process:
                self.process.stdin.write(b'q')  # 发送 'q' 给 ffmpeg，结束录制
                self.process.stdin.flush()
                self.process.wait()  # 等待进程结束
                self.process = None
                print("录制结束")
        print("已经关闭")
    
    def check_camera_status(self, camera_index):
        # 尝试打开摄像头
        cap = cv2.VideoCapture(camera_index)

        # 检查摄像头是否成功打开
        print(cap.isOpened())
        if cap.isOpened():
            print(f"摄像头 {camera_index} 可用")
            cap.release()  # 释放摄像头资源
            return True
        else:
            print(f"摄像头 {camera_index} 被占用或不可用")
            return False

if __name__ == "__main__":
    recorder = VideoRecorder()
    recorder.start()
    time.sleep(5)  # 假设用户决定录制5秒，实际可以根据需要更长或更短
    input("按下 Enter 停止录像...")
    recorder.stop()


