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
    application_extension,
)
from gif_struct.image_descriptor import reslove_image_descriptor, skip_image_descriptor
from gif_struct.logical_screen_descriptor import (
    canvas_data,
    packed_field_data,
    reslove_lsd_packed_field,
)
from render import (
    parse_palette,
    draw_frame,
    show_animation
)
import pygame
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
        self.application_extension = {}
        self.index_stream = []

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
    
    def reslove_application_extension(self):
        d = application_extension(self.hex_str)
        self.application_extension = d
        self.hex_str = self.hex_str[38:]

    def get_image_descriptor(self):
        image_descriptor = reslove_image_descriptor(self.hex_str)
        print("Image Descriptor:", image_descriptor)
        # self.image_descriptor = image_descriptor
        self.image_descriptor.append(image_descriptor)
        self.hex_str = self.hex_str[20:]

    def get_local_color_table(self):
        image_descriptor = self.image_descriptor[-1]
        packed_filed = image_descriptor["packed_filed"]
        size = packed_filed["size_of_local_color_table"]
        flag = packed_filed["local_color_table_flag"]
        if flag == '0':
            log("no local color table")
            self.local_color_table.append('')
            return
        hex_str = self.hex_str
        local_color_table = hex_str[0 : size * 3 * 2]
        self.local_color_table.append(local_color_table)
        self.hex_str = hex_str[size * 3 * 2 :]
    
    # 用于跳过 纯文本扩展(2101) 和 评论扩展(21fe)
    def skip_extensions(self):
        # log("skip_extensions inside", self.hex_str)
        index = other_extension_nums(self.hex_str)
        self.hex_str = self.hex_str[index:]

    def get_image_data(self):
        local_color_table = self.local_color_table[-1]
        hex_str = self.hex_str
        data = skip_local_color_table(local_color_table, hex_str)
        all_data, min_code_size, len_for_skip = get_all_data(data)
        print("min_code_size =", min_code_size)
        print("len(all_data) =", len(all_data) // 2)
        print("all_data head =", all_data[:100])
        print("len_for_skip =", len_for_skip)
        self.image_data.append(all_data)
        index_stream = decoding_bytes(all_data, min_code_size)
        self.index_stream.append(index_stream)
        self.min_code_size.append(min_code_size)
        self.hex_str = self.hex_str[len_for_skip:]
    

    def test(self):
        log("==============================================================")
        log('logical_screen_descriptor', self.logical_screen_descriptor_data)
        log('global_color_table', self.global_color_table)
        log('graphic_control_extension', self.graphic_control_extension)
        log('application_extension', self.application_extension)
        log('image_descriptor', self.image_descriptor)
        log('local_color_table', self.local_color_table)
        log('image_data', self.image_data)
        log('min_code_size', self.min_code_size)
        log('hex_str', self.hex_str)
        log('index_stream', self.index_stream)
        pass

    
def main(file_path):
    clear_log_file()
    gifParser = GifParser(file_path)
    gifParser.signature_and_version()
    gifParser.logical_screen_descriptor()
    gifParser.get_global_color_table()
    gifParser.reslove_hex_str() # 处理完上面三个后的str
    def get_image_descriptor_path():
        gifParser.get_image_descriptor()
        gifParser.get_local_color_table()
        gifParser.get_image_data()

    process_map = {
        "21f9": gifParser.reslove_graphic_control_extension,
        "2c": get_image_descriptor_path,
        "2101": gifParser.skip_extensions,
        "21ff": gifParser.reslove_application_extension,
        "21fe": gifParser.skip_extensions,
    }

    while not gifParser.hex_str.startswith("3b"):
        print("=" * 60)
        print("Next Block:", gifParser.hex_str[:40])
        if gifParser.hex_str.startswith("2c"):
            func = process_map["2c"]
        else:
            key = gifParser.hex_str[:4]
            func = process_map.get(key)
            if func is None:
                raise ValueError(f"Unknown block: {key}")
        # gifParser.test()
        func()        
    gifParser.test()
    ###################################################
    # GIF Animation 渲染
    ###################################################

    palette = parse_palette(
        gifParser.global_color_table
    )


    # GIF逻辑屏幕大小
    canvas_width = gifParser.logical_screen_descriptor_data[
        "canvas_width"
    ]

    canvas_height = gifParser.logical_screen_descriptor_data[
        "canvas_height"
    ]


    ###################################################
    # 创建 GIF 总画布
    ###################################################

    canvas = pygame.Surface(
        (
            canvas_width,
            canvas_height
        )
    )


    # 背景颜色
    background_index = int(
        gifParser.logical_screen_descriptor_data[
            "background_color_index"
        ],
        16
    )


    canvas.fill(
        palette[background_index]
    )



    ###################################################
    # 保存每一帧
    ###################################################

    frames = []


    for i, index_stream in enumerate(
            gifParser.index_stream
    ):


        print("======================")
        print("render frame:", i)


        descriptor = gifParser.image_descriptor[i]


        print(
            "frame size:",
            descriptor["image_size"]
        )


        ###################################################
        # 关键:
        # 当前帧不是重新生成图片
        # 而是在上一帧canvas基础上更新
        ###################################################

        draw_frame(
            canvas,
            index_stream,
            palette,
            descriptor
        )


        ###################################################
        # 保存当前完整画面
        ###################################################

        frame = canvas.copy()


        frames.append(
            frame
        )



    ###################################################
    # GIF delay
    ###################################################

    delays = []


    for gce in gifParser.graphic_control_extension:
        delay_hex = gce["delay_time"]
        # GIF是小端序
        delay = int(
            delay_hex[2:4] + delay_hex[0:2],
            16
        )
        # GIF规范:
        # delay单位是1/100秒
        delays.append(
            delay
        )

    print("frame count:", len(frames))
    print("delays:", delays)

    ###################################################
    # 播放动画
    ###################################################

    show_animation(
        frames,
        delays
    )

if __name__ == "__main__":
    # file_path = "gif/sample_1.gif"
    # file_path = "gif/sample_1_enlarged.gif"
    # file_path = "gif/sample_2_animation.gif"
    file_path = "gif/Dancing.gif"
    main(file_path)