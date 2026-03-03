from utils import log
from gif_struct.logical_screen_descriptor import hex_to_bin


def image_size(str):
    # log("image_descriptor inside", str)
    left = int(str[4 : 6] + str[2 : 4], 16)
    top = int(str[8 : 10] + str[6 : 8], 16)
    width = int(str[12 : 14] + str[10 : 12], 16)
    height = int(str[16 : 18] + str[14 :16], 16)
    res = {
        "left": left,
        "top": top,
        "width": width,
        "height": height,
    }
    return res


def image_descriptor_packed_filed(str):
    skip_image_size = str[18:]
    filed = skip_image_size[0:2]
    bin_8bit = hex_to_bin(filed)
    res = {
        "local_color_table_flag": bin_8bit[0],
        "interlace_flag": bin_8bit[1],
        "sort_flag": bin_8bit[2],
        "reserved_for_future_use": bin_8bit[3:5],
        "size_of_local_color_table": int(bin_8bit[5:8], 2),
    }
    return res


def reslove_image_descriptor(str):
    size = image_size(str)
    packed_filed = image_descriptor_packed_filed(str)
    res = {
        "image_size": size,
        "packed_filed": packed_filed,
    }
    return res