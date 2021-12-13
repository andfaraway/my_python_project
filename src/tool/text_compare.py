# path1和path2是比较的文件路径,result_path是保存对比结果的文件.


def compare(path1, path2, result_path):
    with open(path1) as f1:
        aset = set(f1)
    with open(path2) as f2:
        bset = set(f2)
    with open(result_path, 'a') as f3:
        f3.write(path1 + '===' + path2 + '\n')
        f3.writelines(bset - aset)


path_1 = '/Users/libin/Downloads/jslog2_1451/js_log__optimized out_#58a69(0).txt'
result_text = '/Users/libin/Downloads/jslog2_1451/result.txt'
for index in range(500):
    try:
        path_2 = '/Users/libin/Downloads/jslog2_1451/js_log__optimized out_#58a69({}).txt'.format(index)
        compare(path_1, path_2, result_text)
        print(index)
    except Exception as error:
        print(error)
