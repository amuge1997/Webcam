import cv2
import threading
import time
import datetime
update_img_path = './image/pc.jpg'
cap_index = 1
width = 1920
height = 1080


class VideoRecorder:
    def __init__(self):
        print("录像程序正在初始化")
        self.cap = cv2.VideoCapture(cap_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.is_recording = False
        self.curr_fps = 0
        self.out_dir = './out'
        print("录像程序初始化完成")
    
    def make_avi_file_name(self):
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 格式化时间为 "yyyy-mm-dd-hhmmss" 格式
        file_name = current_time.strftime("%Y-%m-%d-%H%M%S")
        file_name += '.avi'
        return file_name
    
    def start(self):
        if not self.is_recording:
            self.is_recording = True
            self.out = cv2.VideoWriter(self.out_dir + '/' + self.make_avi_file_name(), cv2.VideoWriter_fourcc(*'XVID'), 30.0, (width, height))
            self.recording_thread = threading.Thread(target=self.record)
            self.recording_thread.start()
            return True
        print("已经启动")

    def record(self):
        start = time.perf_counter()
        count = 0
        save_start = time.perf_counter()
        while self.is_recording:
            try:
                curr = time.perf_counter()
                count += 1
                if curr - start > 1:
                    print(count)
                    self.curr_fps = count
                    start = curr
                    count = 0
                ret, frame = self.cap.read()
                if ret:
                    save_curr = time.perf_counter()
                    if save_curr - save_start > 1:
                        cv2.imwrite(update_img_path, frame)
                        save_start = save_curr
                    self.out.write(frame)
            except Exception as e:
                print(f"record()错误: {e}")

    def stop(self):
        if self.is_recording:
            self.is_recording = False
            self.recording_thread.join()
            self.out.release()
        print("已经关闭")
    
    def quit(self):
        if self.is_recording:
            self.is_recording = False
            self.recording_thread.join()
            self.out.release()
        self.cap.release()
        print("已经退出")



# if __name__ == "__main__":
#     # 启动录像线程
#     recorder = VideoRecorder()
#     recorder.start()

#     # 停止录制
#     input("按下 Enter 停止录像...")
#     recorder.stop()
#     print("quit")
#     recorder.quit()
