from utils import log


def image_data(local_color_table, data):
    if local_color_table is None:
        local_color_table_len = 0
    else:
        local_color_table_len = len(local_color_table)
    data = data[local_color_table_len :]
    return data
