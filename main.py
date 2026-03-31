from utils import log, clear_log_file
from gif_struct.get_header import get_header 
from gif_struct.read_gif_hex import read_gif_hex 
from gif_struct.global_color_table import global_color_table 
from gif_struct.image_data import skip_local_color_table
from lzw_decompression.decompression import decoding_bytes, get_all_data
from gif_struct.reslove_extensions import (
    skip_global_color_table, 
    graphic_control_extension,
    other_extension_nums,
)
from gif_struct.image_descriptor import reslove_image_descriptor, skip_image_descriptor
from gif_struct.logical_screen_descriptor import (
    canvas_data,
    packed_field_data,
    reslove_lsd_packed_field,
)


# def get_image_data():
#     str = reslove_extensions()
#     local_color_table = get_local_color_table()
#     data = skip_image_descriptor(str)
#     res = image_data(local_color_table, data)
#     return res


# def decoding_image_data():
#     res = get_image_data()
#     decoding_bytes(res)


class GifParser():
    def __init__(self, gif_path):
        self.hex_str = read_gif_hex(gif_path)
        self.logical_screen_descriptor_data = {}
        self.global_color_table = ''
        self.graphic_control_extension = []
        self.image_descriptor = []
        self.local_color_table = []
        self.image_data = []
        self.min_code_size = []

    def signature_and_version(self):
        signature, version = get_header(self.hex_str)
        log("signature and version", signature, version)         
        pass
    
    def logical_screen_descriptor(self):
        hexStr = self.hex_str[12:26]
        canvas_width, canvas_height = canvas_data(hexStr)
        packed_field = packed_field_data(hexStr)
        rpf = reslove_lsd_packed_field(packed_field)
        background_color_index = hexStr[10:12]
        pixel_aspect_ratio = hexStr[12:14]
        r = {
            "canvas_width": canvas_width,
            "canvas_height": canvas_height,
            "global_color_table_flag": rpf["global_color_table_flag"],
            "color_resolution": rpf["color_resolution"],
            "sort_flag": rpf["sort_flag"],  
            "size_of_global_color_table": rpf["size_of_global_color_table"],
            "background_color_index": background_color_index,
            "pixel_aspect_ratio": pixel_aspect_ratio,
        }
        self.logical_screen_descriptor_data = r
    
    def get_global_color_table(self):
        hex_str = self.hex_str[26:]
        data = self.logical_screen_descriptor_data
        table = global_color_table(hex_str, data)
        self.global_color_table = table

    def reslove_hex_str(self):
        table = self.global_color_table
        self.hex_str = skip_global_color_table(table, self.hex_str)

    def reslove_graphic_control_extension(self):
        d = graphic_control_extension(self.hex_str)
        # self.graphic_control_extension = d
        self.graphic_control_extension.append(d)
        self.hex_str = self.hex_str[16:]
    
    def get_image_descriptor(self):
        image_descriptor = reslove_image_descriptor(self.hex_str)
        # self.image_descriptor = image_descriptor
        self.image_descriptor.append(image_descriptor)
        self.hex_str = self.hex_str[20:]

    def get_local_color_table(self):
        image_descriptor = self.image_descriptor[-1]
        packed_filed = image_descriptor["packed_filed"]
        size = packed_filed["size_of_local_color_table"]
        if size == 0:
            log("no local color table")
            self.local_color_table.append('')
            return
        hex_str = self.hex_str
        local_color_table = hex_str[0 : size * 3 * 2]
        self.local_color_table.append(local_color_table)
        self.hex_str = hex_str[size * 3 * 2 :]
    
    def skip_extensions(self):
        index = other_extension_nums(self.hex_str)
        self.hex_str = self.hex_str[index:]

    def get_image_data(self):
        local_color_table = self.local_color_table[-1]
        hex_str = self.hex_str
        data = skip_local_color_table(local_color_table, hex_str)
        log('hex_str0', data)
        all_data, min_code_size, len_for_skip = get_all_data(data)
        log('all_data and min_code_size', all_data, min_code_size)
        self.image_data.append(all_data)
        self.min_code_size.append(min_code_size)
        self.hex_str = self.hex_str[len_for_skip:]

    def test(self):
        log('logical_screen_descriptor', self.logical_screen_descriptor_data)
        log('global_color_table', self.global_color_table)
        log('graphic_control_extension', self.graphic_control_extension)
        log('image_descriptor', self.image_descriptor)
        log('local_color_table', self.local_color_table)
        log('image_data', self.image_data)
        log('min_code_size', self.min_code_size)
        log('hex_str', self.hex_str)
        log('global_color_table next 4 string', self.hex_str[0:4])
    

def main():
    clear_log_file()
    # file_path = "gif/sample_1.gif"
    file_path = "gif/sample_1_enlarged.gif"
    # file_path = "gif/sample_1_animation.gif"
    gifParser = GifParser(file_path)
    gifParser.signature_and_version()
    gifParser.logical_screen_descriptor()
    gifParser.get_global_color_table()
    gifParser.reslove_hex_str()
    gifParser.reslove_graphic_control_extension()
    gifParser.get_image_descriptor()
    gifParser.get_local_color_table()
    gifParser.get_image_data()
    gifParser.test()
    # process_pic = {
    #     "21f9":skip_extensions,
    #     "extensions":skip_extensions,

    # }
    # while True:

    #     trailer = '3b'
    #     if gifParser.hex_str == trailer:
    #         break



if __name__ == "__main__":
    main()

