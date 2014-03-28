from ctypes import *
from time import sleep
user32 = windll.user32


class MouseInput(Structure):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646273(v=vs.85).aspx
    _fields_ = [('dx', c_long),  # in pixels (unless in abs)
                ('dy', c_long),
                ('mouseData', c_ulong),  #
                ('dwFlags', c_ulong),
                ('time', c_ulong),  # timestamp 0->system provides
                ('dwExtraInfo', POINTER(c_ulong))]
    ''' dx, dy '''
    MaxPos = 65535  # lower/right (primary monitor)
    ''' mouseData '''
    # if dwFlag = Wheel (or HWheel), mouseData = dist (+) -> forward (right)
    WheelDelta = 120  # one wheel click
    
    ''' dwFlags '''
    Absolute = 0x8000  # dx dy are absolute coordinates
    VirtualDesk = 0x4000  # req absolute flag
    # maps coords to entire virtual desktop (multi monitor?)
    
    HWheel = 0x01000  # horiz, data in mouseData
    Wheel = 0x0800  # vert, data in mouseData
    Move = 0x0001
    MoveNoCoalesce = 0x2000
    
    LDown = 0x0002
    LUp = 0x0004
    RDown = 0x008
    RUp = 0x0010
    MDown = 0x0008  # mid
    MUp = 0x0040
    XDown = 0x0080  # ??
    XUp = 0x0100  # ??
    
    
    
class KeyBdInput(Structure):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646271(v=vs.85).aspx
    _fields_ = [('wVk', c_ushort),  # virtual key code
                ('wScan', c_ushort),  # hardware scan code 
                ('dwFlags', c_uint), 
                ('time', c_uint),
                ('dwExtraInfo', POINTER(c_ulong))]
    ''' dwFlags '''
    ExtendedKey = 0x0001 # scan code preceded by 0xE0
    KeyUp = 0x0002 # otherwise = down
    ScanCode = 0x0008 # use wScan not wVk
    Unicode = 0x004 # VK_PACKET keystroke?
    
class HardwareInput(Structure):
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ms646269(v=vs.85).aspx
    _fields_ = [('uMsg', c_uint),
                ('wParamL', c_ushort),
                ('wParamH', c_ushort)]
        
class InputU(Union):
    _fields_ = [('mi', MouseInput),
                ('ki', KeyBdInput),
                ('hi', HardwareInput)]

class Input(Structure):
    _fields_ = [('type', c_uint),
                ('input', InputU)]
    Mouse = 0
    KeyBoard = 1
    Hardward = 2
    
# SAMPLE CODE
#
# sleep(2)
# FInputs = Input * 4
# extra = c_ulong(0)
#  
#  
# click = InputU()
# click.mi = MouseInput(0, 0, 0, MouseInput.LDown, 0, pointer(extra))
# release = InputU()
# release.mi = MouseInput(0, 0, 0, MouseInput.LUp, 0, pointer(extra))
# keyD = InputU()
# keyD.ki = KeyBdInput(ord('A'), 0, 0, 0, pointer(extra))
# keyU = InputU()
# keyU.ki = KeyBdInput(ord('A'), 0, KeyBdInput.KeyUp, 0, pointer(extra))
# x = FInputs((Input.Mouse, click), (Input.Mouse, release), (Input.KeyBoard, keyD), (Input.KeyBoard, keyU))
# user32.SendInput(4, pointer(x), sizeof(x[0]))
