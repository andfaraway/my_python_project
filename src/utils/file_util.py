# 读取数据
def read(path):
    with open(path, 'r') as f:
        text = f.read()
        return text


# 写入数据
def write(path, text: str):
    with open(path, 'w') as f:
        result = text
        f.write(result)


# 追加写入
def add(path, text: str):
    with open(path, 'a') as f:
        result = text
        f.write(result)

