from utils import log


def global_color_table(str, res):
    flag = res["global_color_table_flag"]
    size = res["size_of_global_color_table"]
    if flag == "1":
        index = int(size, 2)
        table_size = 2 ** (index + 1) * 3 * 2
        table = str[0 : table_size]
        return table
    else:
        return None