import os


def run_cmd(cmd: str):
    val = os.system(cmd)
    if val == 0:
        return cmd + ' ->success'
    else:
        return cmd + ' ->failure'


# 当前目录下创建新目录
def create(name):
    os.makedirs(name, exist_ok=True)

# 获取当前目录 os.getcwd()
