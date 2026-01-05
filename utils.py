import time

def hex_to_bin(hex_str):
    hex_to_ten = int(hex_str, 16)
    ten_to_bin = bin(hex_to_ten)
    bin_data = ten_to_bin[2:]
    bin_8bit = bin_data.zfill(8)
    return bin_8bit


def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def clear_log_file():
    with open('log.txt', 'w') as file:
        file.write('')  # 写入空字符串
    print("log.txt 文件已清空")