from utils import log


filename = "gif/sample_1.gif"
# filename = "gif\Dancing.gif"
# filename = "gif\sample_2_animation.gif"
# filename = "gif/sample_1_enlarged.gif"


def read_gif_hex():
    with open(filename, 'rb') as f:
        res = f.read().hex()
        # log("读取的十六进制字符串:", res)
        return res
