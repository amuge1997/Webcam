import ctypes
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def mute_windows():
    # 初始化 COM 库
    ctypes.windll.ole32.CoInitialize(None)

    # 获取系统的音频设备
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # 设置静音
    volume.SetMute(1, None)

    # 清理 COM 库
    ctypes.windll.ole32.CoUninitialize()


def is_muted():
    # 调用 CoInitialize 初始化 COM 库
    ctypes.windll.ole32.CoInitialize(None)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # 获取是否静音
    is_muted = volume.GetMute()
    
    # 调用 CoUninitialize 清理 COM 库
    ctypes.windll.ole32.CoUninitialize()

    return is_muted

def get_system_volume():
    # 初始化 COM 库
    ctypes.windll.ole32.CoInitialize(None)

    # 获取系统的音频设备
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # 获取当前音量值（0.0 到 1.0）
    current_volume = volume.GetMasterVolumeLevelScalar()
    
    # 清理 COM 库
    ctypes.windll.ole32.CoUninitialize()

    return round(current_volume*100)

if __name__ == "__main__":
    if is_muted():
        print("The system is currently muted.")
    else:
        print("The system is not muted.")

    
    mute_windows()
    print("muted")








