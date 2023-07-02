from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
x, y, w, h = work_area


def getWorkAreaHeight():
    return h


def getWorkAreaWidth():
    return w


def getWorkArea():
    return work_area
