import win32api  
 
WM_APPCOMMAND = 0x319

APPCOMMAND_VOLUME_MAX = 0x0a
APPCOMMAND_VOLUME_MIN = 0x09

def mute_windows():

    #音量最大
    #win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MAX * 0x10000)

    #音量最小
    win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, APPCOMMAND_VOLUME_MIN * 0x10000)




if __name__ == "__main__":
    mute_windows()
    print("muted")








