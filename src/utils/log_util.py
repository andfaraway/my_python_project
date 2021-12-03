import time


def debug_print(text):
    print('[{}]{}'.format(current_time(), text))


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
