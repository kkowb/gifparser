import pygame

def render_image(pixel_indices, palette, width, height):
    # 创建一个和画布一样大小的 Surface
    surface = pygame.Surface((width, height))

    # 把索引映射成颜色，并逐像素写入
    for y in range(height):
        for x in range(width):
            idx = pixel_indices[y * width + x]   # 取像素索引
            color = palette[idx]                 # 查调色板
            surface.set_at((x, y), color)        # 写到 Surface

    return surface


def main():
    pygame.init()
    width, height = 10, 10  # 原始像素大小
    scale =  20      # 缩放倍数
    screen = pygame.display.set_mode((width * scale, height * scale))  # 窗口大小 100x100
    pygame.display.set_caption("GIF 索引图像渲染")

    # --- 全局颜色表 ---
    palette = {
        0: (255, 255, 255),  # 白色
        1: (255, 0, 0),      # 红色
        2: (0, 0, 255)       # 蓝色
    }

    # --- 索引流（10x10） ---
    pixel_indices = [
        1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
        1, 1, 1, 1, 1, 2, 1, 2, 2, 2,
        1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
        1, 1, 1, 0, 0, 0, 0, 2, 2, 2,
        1, 1, 1, 0, 0, 0, 0, 2, 2, 2,
        2, 2, 2, 0, 0, 0, 0, 1, 1, 1,
        2, 2, 2, 0, 0, 0, 0, 1, 1, 1,
        2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 1, 1, 1, 1, 1
    ]

    # 渲染 Surface（10x10）
    surface = render_image(pixel_indices, palette, width, height)

    # 缩放成 100x100
    surface_scaled = pygame.transform.scale(surface, (width * scale, height * scale))

    # --- 主循环 ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(surface_scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
