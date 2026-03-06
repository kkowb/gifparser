from utils import hex_to_bin


def canvas_data(hex_str):
    data = hex_str[0:8]
    width = int(data[2:4] + data[0:2], 16)
    height = int(data[6:8] + data[4:6], 16)
    return width, height


def packed_field_data(hex_str):
    data = hex_str[8:10]
    data_bin = hex_to_bin(data)
    return data_bin


def reslove_lsd_packed_field(packed_field):
    global_color_table_flag = packed_field[0]
    color_resolution = packed_field[1:4]
    sort_flag = packed_field[4]
    size_of_global_color_table = packed_field[5:8]
    res = {
        "global_color_table_flag": global_color_table_flag,
        "color_resolution": color_resolution,
        "sort_flag": sort_flag,
        "size_of_global_color_table": size_of_global_color_table,
    }
    return res