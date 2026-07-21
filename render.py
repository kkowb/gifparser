import pygame


def parse_palette(hex_color_table):
    """
    十六进制颜色表:

    ff000000ff00ffff00

    转换:

    [
        (255,0,0),
        (0,255,0),
        ...
    ]
    """

    palette = []

    for i in range(0, len(hex_color_table), 6):

        r = int(hex_color_table[i:i+2], 16)
        g = int(hex_color_table[i+2:i+4], 16)
        b = int(hex_color_table[i+4:i+6], 16)

        palette.append(
            (r, g, b)
        )

    return palette



def render_image(
        pixel_indices,
        palette,
        width,
        height
):

    """
    index像素流 + 调色板
    生成pygame Surface
    """

    surface = pygame.Surface(
        (
            width,
            height
        )
    )


    for y in range(height):

        for x in range(width):

            index = pixel_indices[
                y * width + x
            ]


            color = palette[index]


            surface.set_at(
                (x, y),
                color
            )


    return surface




def show_gif_frame(
        pixel_indices,
        palette,
        width,
        height
):

    pygame.init()


    # 获取当前屏幕大小
    info = pygame.display.Info()

    screen_width = info.current_w
    screen_height = info.current_h



    # 最大显示区域
    max_width = 500
    max_height = 500


    # 自动计算缩放比例
    scale = min(
        max_width / width,
        max_height / height
    )


    show_width = int(
        width * scale
    )

    show_height = int(
        height * scale
    )



    screen = pygame.display.set_mode(
        (
            show_width,
            show_height
        )
    )


    pygame.display.set_caption(
        "GIF Parser"
    )



    # 原始像素渲染
    surface = render_image(
        pixel_indices,
        palette,
        width,
        height
    )



    # 根据屏幕缩放
    surface = pygame.transform.smoothscale(
        surface,
        (
            show_width,
            show_height
        )
    )



    # 居中显示位置
    x = (
        show_width - surface.get_width()
    ) // 2

    y = (
        show_height - surface.get_height()
    ) // 2



    running = True


    while running:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False



        screen.fill(
            (0,0,0)
        )


        screen.blit(
            surface,
            (
                x,
                y
            )
        )


        pygame.display.flip()



    pygame.quit()