import time
import datetime
import subprocess
import cv2
import threading
import numpy as np
update_img_path = './image/pc.jpg'

width = 1920
height = 1080

cap_name = "BisonCam,NB Pro"

cap_index = 0


class VideoRecorder:
    def __init__(self):
        print("录像程序正在初始化")
        self.default_fps = 30
        # self.default_resolution = f"{width}x{height}"
        self.default_resolution = f"{width}:{height}"
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
                    '-f', 'dshow',                    # 使用 DirectShow (Windows 摄像头接口)
                    '-i', f'video={self.default_cap_name}',  # 替换为你的摄像头设备名称'-vcodec', 'mjpeg',                # 使用 MJPEG 编码
                    '-vf', f'scale={self.default_resolution}',            # 设置输出视频分辨率
                    '-f', 'image2pipe',                # 输出到管道
                    '-pix_fmt', 'bgr24',               # 指定输出格式为 OpenCV 支持的 BGR 格式
                    '-q:v', '1',                       # 设置视频质量
                    'pipe:1',                          # 通过管道输出到 stdout
                    self.out_dir + '/' + self.make_avi_file_name()  # 输出文件名
                ]
                self.process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
                threading.Thread(target=self.read_frames_from_ffmpeg).start()
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
    
    def read_frames_from_ffmpeg(self):
        try:
            while self.is_recording and self.process:
                # 尝试读取每一帧 (BGR 格式，640x480)
                raw_image = self.process.stdout.read(640 * 480 * 3)

                if len(raw_image) == 0:
                    break

                # 将读取的字节数据转换为 NumPy 数组并重塑为图像
                image = np.frombuffer(raw_image, dtype=np.uint8).reshape((480, 640, 3))

                # 显示图像
                cv2.imshow('Recording', image)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # 关闭 OpenCV 窗口
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"read_frames_from_ffmpeg()错误: {e}")
    
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
    # time.sleep(5)  # 假设用户决定录制5秒，实际可以根据需要更长或更短
    # input("按下 Enter 停止录像...")
    # recorder.stop()


