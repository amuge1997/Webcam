import time
import datetime
import subprocess
import cv2
import threading
update_video_path = './image/pc.mp4'
update_img_path = './image/pc.jpg'

width = 2560
height = 1440

cap_name = "BisonCam,NB Pro"
cap_index = 0

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
        self.cap_show_lock = threading.Lock()

        self.now_status = 'none'
        print("录像程序初始化完成")
    
    def change_status(self, status):
        if status == 'none':
            self.now_status = 'none'
        elif status == 'show':
            self.now_status = 'show'
        elif status == 'run':
            self.now_status = 'run'
        else:
            raise Exception("状态转换出错")
    
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
            if self.cap_show_lock.acquire(blocking=False):
                    self.cap_show_lock.release()
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
                    print(f"摄像头 首次 启动")
                    self.change_status("run")
                    return True
            else:
                print(f"摄像头 被占用")
                return False
        else:
            print(f"摄像头 已经 启动")
            return True

    def stop(self):
        if self.is_recording:
            self.close_recording()
            if self.process:
                self.process.stdin.write(b'q')  # 发送 'q' 给 ffmpeg，结束录制
                self.process.stdin.flush()
                self.process.wait()  # 等待进程结束
                self.process = None
                self.change_status("none")
                print("录制结束")
        print("已经关闭")
    
    
    def get_last_frame(self, video_path):
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        # 检查视频是否成功打开
        if not cap.isOpened():
            print("无法打开视频文件")
            return None
        # 获取视频的总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 如果视频为空
        if total_frames == 0:
            print("视频为空")
            return None
        # 跳转到最后一帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
        # 读取最后一帧
        ret, last_frame = cap.read()
        if not ret:
            print("无法读取最后一帧")
            return None
        # 释放视频资源
        cap.release()
        return last_frame

    def capture_and_save_one_frame(self):
        if self.is_recording:
            print("SHOW:摄像头被占用")
            return False
        # 打开摄像头
        if self.cap_show_lock.acquire(blocking=False):
            self.change_status('show')
            ###########################################################

            ffmpeg_cmd = [
                'ffmpeg',
                '-y',                              # 自动覆盖已有文件
                '-f', 'dshow',                     # 使用 DirectShow 作为输入格式（适用于 Windows）
                '-i', f'video={self.default_cap_name}',       # 指定摄像头名称
                '-t', '1',                          # 录制时长为 1 秒
                '-vcodec', 'libx264',               # 使用 H.264 编码
                '-preset', 'fast',                  # 快速预设
                '-crf', '23',                       # 质量设置，数值越低质量越好
                update_video_path                         # 输出文件名
            ]
            
            try:
                # 调用 ffmpeg 命令
                result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                # 输出 ffmpeg 执行结果
                if result.returncode == 0:
                    print(f"capture_and_save_one_frame() 录制成功 保存为{update_video_path}")
                    pc_image = self.get_last_frame(update_video_path)
                    cv2.imwrite(update_img_path, pc_image)
                else:
                    print(f"capture_and_save_one_frame() 录制错误: {result.stderr}")
            
            except Exception as e:
                print(f"capture_and_save_one_frame() 发生意外: {e}")
            
            ##########################################################
            # 释放摄像头
            self.change_status('none')
            self.cap_show_lock.release()

if __name__ == "__main__":
    recorder = VideoRecorder()
    recorder.start()
    time.sleep(5)  # 假设用户决定录制5秒，实际可以根据需要更长或更短
    input("按下 Enter 停止录像...")
    recorder.stop()


