import subprocess

def get_camera_names():
    # 执行 ffmpeg 命令来列出设备
    command = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
    
    try:
        # 在 Windows 上设置 encoding='utf-8' 避免 GBK 解码错误
        result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
        
        # 打印完整的 stderr 输出，便于调试
        print("Captured stderr:", result.stderr)
        
        # 检查 stderr 是否为空
        if not result.stderr:
            print("没有捕获到任何设备信息")
            return []
        
        # 解析 stderr 输出
        devices = result.stderr.splitlines()
        video_devices = []
        for line in devices:
            if "DirectShow video devices" in line:
                print("发现视频设备：")
            if 'video="' in line:  # 查找包含摄像头的行
                # 提取设备名称
                device_name = line.split('"')[1]
                video_devices.append(device_name)
                print(device_name)
        
        return video_devices

    except subprocess.CalledProcessError as e:
        print(f"执行命令时出错: {e}")
        return []

# 调用函数获取摄像头名称
camera_names = get_camera_names()
print(f"可用的摄像头: {camera_names}")
