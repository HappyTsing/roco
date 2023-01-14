# -*-coding:UTF-8 -*-
from pyautogui import click,press,doubleClick,moveTo
from win32gui import EnumWindows, GetClassName, SendMessage, SetForegroundWindow, GetWindowRect, GetWindowText, DeleteObject, GetWindowDC
from win32ui import CreateBitmap,CreateDCFromHandle
from win32con import WM_SYSCOMMAND,SC_RESTORE
from multiprocessing import Process, Pipe
from win32con import SRCCOPY
from loguru import logger
from numpy import uint8,frombuffer
"""
游戏窗口，不断获取窗口截图
"""


class Window(Process):
    def __init__(self):
        super().__init__(daemon=True)
        # hwnd = win32gui.FindWindow("TForm1","窗口标题") # 标题会变化，这种方法窗口标题必须固定！
        hwnd_list = []
        EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)
        for hwnd in hwnd_list:
            if GetClassName(hwnd) == "TForm1" and "悟空神辅" in GetWindowText(hwnd):
                # 窗口置顶
                SendMessage(hwnd, WM_SYSCOMMAND,SC_RESTORE, 0)
                SetForegroundWindow(hwnd)

                # 获取游戏窗口分辨率
                rect = GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                w = rect[2] - x
                h = rect[3] - y
                logger.info("窗口分辨率: (%d, %d)" % (w, h))
                logger.info("窗口位置: (%d, %d)" % (x, y))
                logger.info("窗口名称: {}".format(GetWindowText(hwnd)))
                self.hwnd = hwnd

        # 创建两个Pipe，通过sender.send()写入，receiver.recv()取出
        self.receiver, self.sender = Pipe(False)
        self.start()

    def screencap(self):
        # 返回屏幕截图
        return self.receiver.recv()

    # bloonstd无法获取通过win32获取屏幕截图，采用pyautogui的方式
    # def run(self):
    #     while True:
    #         # 截图
    #         screenshot = pyautogui.screenshot()
    #         # 先转换为numpy数组，再将rgb格式转换为opencv的bgr格式
    #         image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #         # 将图片数组写入管道中
    #         self.sender.send(image)

    # win32方式截图，参考：https://blog.csdn.net/weixin_40875387/article/details/127716504
    def run(self):
        hwnd_dc = GetWindowDC(self.hwnd)
        mfc_dc = CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        while True:
            # 屏幕截图
            bitmap = CreateBitmap()
            rect = GetWindowRect(self.hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(bitmap)
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), SRCCOPY)
            ints_array = bitmap.GetBitmapBits(True)
            DeleteObject(bitmap.GetHandle())
            image = frombuffer(ints_array, dtype=uint8)
            image.shape = (height, width, 4)

            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 转换RGB顺序
            # cv2.imshow('baofeng', image)
            # cv2.imwrite("main1.png", intdata)
            # cv2.waitKey()

            self.sender.send(image)

    def get_absolute_position(self, relative_x, relative_y):
        rect = GetWindowRect(self.hwnd)
        window_x = rect[0]
        window_y = rect[1]
        absolute_x = window_x + relative_x
        absolute_y = window_y + relative_y
        return absolute_x, absolute_y

    def move(self, relative_x, relative_y, movetime=0):  # 鼠标移动 x,y_移动位置，movetime_移动时间
        absolute_x, absolute_y = self.get_absolute_position(
            relative_x, relative_y)
        moveTo(absolute_x, absolute_y, duration=movetime)

    def click(self, relative_x, relative_y, times, type="left"):		# left right middle
        absolute_x, absolute_y = self.get_absolute_position(
            relative_x, relative_y)
        click(absolute_x, absolute_y, clicks=int(times), button=type)

    def doubleClick(self, relative_x, relative_y, type="left"):
        absolute_x, absolute_y = self.get_absolute_position(
            relative_x, relative_y)
        doubleClick(absolute_x, absolute_y, button=type)

    def press(self, key, times):
        press(key, presses=times)

    # dpi 缩放级别会影响 win32gui.GetWindowRect，故换用此实现
    # todo: 似乎没啥影响，暂时先不用这种方法
    # def get_window_rect(self, hwnd):
    #     rect = wintypes.RECT()
    #     DWMWA_EXTENDED_FRAME_BOUNDS = 9
    #     ctypes.windll.dwmapi.DwmGetWindowAttribute(
    #         wintypes.HWND(hwnd),
    #         ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
    #         ctypes.byref(rect),
    #         ctypes.sizeof(rect)
    #     )
    #     return rect.left, rect.top, rect.right, rect.bottom
