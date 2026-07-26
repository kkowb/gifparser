import pygame
import time



def parse_palette(hex_color_table):

    palette=[]

    for i in range(0,len(hex_color_table),6):

        r=int(hex_color_table[i:i+2],16)
        g=int(hex_color_table[i+2:i+4],16)
        b=int(hex_color_table[i+4:i+6],16)

        palette.append(
            (r,g,b)
        )

    return palette




def draw_frame(
        canvas,
        index_stream,
        palette,
        descriptor
):

    left = descriptor["image_size"]["left"]
    top = descriptor["image_size"]["top"]

    width = descriptor["image_size"]["width"]
    height = descriptor["image_size"]["height"]


    for y in range(height):

        for x in range(width):

            index = index_stream[
                y * width + x
            ]

            color = palette[index]


            canvas.set_at(
                (
                    left+x,
                    top+y
                ),
                color
            )




def create_frame(
        canvas_width,
        canvas_height,
        index_stream,
        palette,
        descriptor
):

    """
    创建一帧完整canvas
    """


    canvas = pygame.Surface(
        (
            canvas_width,
            canvas_height
        )
    )


    canvas.fill(
        palette[0]
    )


    draw_frame(
        canvas,
        index_stream,
        palette,
        descriptor
    )


    return canvas




def show_animation(
        frames,
        delays
):


    pygame.init()


    width,height = frames[0].get_size()


    max_size=500


    scale=min(
        max_size/width,
        max_size/height
    )


    show_width=int(width*scale)
    show_height=int(height*scale)



    screen=pygame.display.set_mode(
        (
            show_width,
            show_height
        )
    )


    pygame.display.set_caption(
        "GIF Parser"
    )


    index=0


    clock=pygame.time.Clock()


    last_time=time.time()



    running=True


    while running:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running=False



        now=time.time()


        # delay_time 单位是 1/100 秒
        if now-last_time >= max(delays[index],1)/100:
            index += 1

            if index >= len(frames):
                index=0

            last_time=now



        surface=pygame.transform.scale(
            frames[index],
            (
                show_width,
                show_height
            )
        )


        screen.blit(
            surface,
            (0,0)
        )


        pygame.display.flip()



    pygame.quit()