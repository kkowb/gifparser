from gif_struct.logical_screen_descriptor import packed_field_data
from utils import log, hex_to_bin


def skip_global_color_table(table, hex_str):
    if table is None:
        str = hex_str[26:]
    else:
        table_length = len(table)
        # log("table_length", table_length)
        index = 26 + table_length
        str = hex_str[index:]
    return str


def reslove_gce_packed_field(filed):
    filed_bin = hex_to_bin(filed)
    res = {
        "reserved_for_future_use": filed_bin[0:3],
        "disposal_method": filed_bin[3:5],
        "user_input_flag": filed_bin[5:6],
        "transparent_color_flag": filed_bin[6:7],
    }
    return res


def graphic_control_extension(hex_str):
    # hex_str = hex_str[4:]
    byte_size = hex_str[4:6]
    p = hex_str[6:8]
    packed_field = reslove_gce_packed_field(p)
    delay_time = hex_str[8:12]
    transparent_color_index = hex_str[12:14]
    res = {
        "byte_size": byte_size,
        "packed_field": packed_field,
        "delay_time": delay_time,
        "transparent_color_index": transparent_color_index,
    }
    return res

# 21 01 0C 00 00 00 00 64 00 64 00 14 14 01 00 0B 68 65 6C 6C 6F 20 77 6F 72 6C 64 00
def other_extension_nums(hex_str):
    data = hex_str[4:]
    data_len = 4
    while True:
        num_of_bytes = int(data[0:2], 16)
        data_len += 2
        if num_of_bytes == 0:
            break
        num = num_of_bytes * 2
        data_len += num
        data = data[2 + num_of_bytes * 2 :]
    return data_len


# def skip_extensions(hex_str):
#     extensions_name = ("21f9", "21fe", "21ff", "2101")
#     data = hex_str
#     str_begin = data[0 : 4]
#     log("str_begin", str_begin)
#     while data and str_begin in extensions_name:
#         if data.startswith("21f9"):
#             res = reslove_graphic_control_extension(data)
#             str_begin = res[0 : 4]
#         else:
#             res = reslove_other_extension(data)
#             str_begin = res[0 : 4]
#         data = res
#     return data
#     pass