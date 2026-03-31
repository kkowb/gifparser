from utils import log

class DecoderBytes():
    def __init__(self, binary, min_code_size):
        self.binary = binary
        self.min_code_size = min_code_size
        self.code_table = []
        self.nbits = min_code_size + 1
        self.clear_code = 2 ** min_code_size
        self.eoi_code = self.clear_code + 1
        self.index_stream = ''
        #decompression_lzw
        self.prevcode = 0 
        self.next_number = 0
        # code_stream 是真正要解析出来的东西，和 code_table 是两个东西
        # 解析 code 位增加的依据是依据code_stream里的值来决定
        self.code_stream = ''

    def parse_code(self, code_bin):
        reversed_bits = code_bin[::-1]
        log("reversed_bits", reversed_bits)
        code = int(reversed_bits, 2)
        return code
    
    def init_table(self):
        clear_code = self.clear_code
        eoi_code = self.eoi_code
        self.code_table = []
        self.nbits = self.min_code_size + 1
        # d 是一个临时变量，用于定义一个空数组
        for i in range(2 ** self.min_code_size):
            d = {}
            d[f"#{i}"] = f"{i}"
            self.code_table.append(d)
        clear_code = {}
        clear_code_value = len(self.code_table)
        clear_code[f"#{clear_code_value}"] = f"{clear_code_value}"
        eoi_code = {}
        eoi_code[f"#{clear_code_value + 1}"] = f"{clear_code_value + 1}"
        self.code_table.append(clear_code)
        self.code_table.append(eoi_code)
        log("init code_table", self.code_table)

    def update_binary(self):
        nbits = self.nbits
        self.binary = self.binary[nbits:]

    def create_new_code(self, new_code_stream):
        len_code_table = len(self.code_table)
        d = {}
        d[f'#{len_code_table}'] = new_code_stream
        return d
    
    def prevcode_stream(self):
        prevcode = self.code_table[self.prevcode]
        steam = prevcode[f"#{self.prevcode}"]
        return steam
    
    def decompression_lzw(self, parse_code):
        len_index_stream = len(self.index_stream)
        if len_index_stream == 0:
            # 第一个总是直接加入 index_stream
            self.index_stream += str(parse_code)
            self.prevcode = parse_code
        else:
            exit_flag = len(self.code_table) - 1
            log('exit_flag', exit_flag)
            if parse_code <= exit_flag:
                log('存在')
                code = self.code_table[parse_code]
                steam_value = code[f"#{parse_code}"]
                self.index_stream += steam_value
                k = steam_value[0]
                prevcode_stream = self.prevcode_stream()
                new_code_stream = prevcode_stream + k
                new_code = self.create_new_code(new_code_stream)
                self.code_table.append(new_code)
                self.prevcode = parse_code
                log("code_table", self.code_table)
                # return new_code
            else:
                log("不存在")
                prevcode = self.prevcode
                code = self.code_table[prevcode]
                steam_value = code[f"#{prevcode}"]
                k = steam_value[0]
                prevcode_stream = self.prevcode_stream()
                new_code_stream = prevcode_stream + k
                self.index_stream += new_code_stream 
                new_code = self.create_new_code(new_code_stream)
                self.code_table.append(new_code)
                self.prevcode = parse_code
                log("code_table", self.code_table)

    def update_nbits(self):
        len_code_table = len(self.code_table) - 1
        log("len_code_table", len_code_table)
        nbits_flag = 2 ** self.nbits - 1
        if len_code_table == nbits_flag:
            self.nbits += 1
        log("nbits_flag", nbits_flag)
        log("*****************************")

    def start(self):
        log("binary", self.binary)
        log("min_code_size", self.min_code_size)
        while True:
            code_to_parse = self.binary[0:self.nbits]
            self.update_binary()

            parse_code = self.parse_code(code_to_parse)
            if parse_code == self.eoi_code:
                log("解码结束index_stream是", self.index_stream)
                index_stream = self.index_stream
                return index_stream

            log("parse_code", parse_code)

            self.code_stream += str(parse_code)
            log("code_stream", self.code_stream)

            clear_code = self.clear_code
            if parse_code == clear_code:
                self.init_table()
                # self.decompression_lzw(parse_code)
                continue

            self.decompression_lzw(parse_code)
            self.update_nbits()
            self.next_number = len(self.code_table)
            log("next_number", self.next_number)
        pass

'''
我现在的理解是
1：编码的情况是，存储没出现过的 索引搭配； 解码就是根据文档上的“要求”，解码出索引搭配
2：如果以后再次出现同样的搭配就可以直接用
3：用于压缩数据，重复过的 “搭配”可以用存储过的 code 直接表示

In the decoding process, we again would increase our code size when we read the code for #7 and would read the next 4, rather than the next 3 bits 那这句话说代码表中 “构建出” #7 的时候，就增加size
那就是要边解码边构建代码表，但是代码表里面的数据刚好就是按顺序，比如初始化代码表最后是 #5，那代码表下一个数据就要用 #6，7, 8,
我的想法是先不按照 LZW Decompression 把代码表里的数据“解码出来”，比如#6 是 1，1； #7 是1，1，1
就先按照"代码表里的顺序数字:6789"把code stream 都 解码出来 ：#4 #1 #6 #6 #2 #9 #9 #7 #8 #10 #2 #12 #1 #14 #15 #6 #0 #21 #0 #10 #7 #22 #23 #18 #26 #7 #10 #29 #13 #24 #12 #18 #16 #36 #12 #5
然后再根据 LZW Decompression去构建“真的”代码表
那就是顺序到7的时候，应该size + 1
比如先取
先 100 -> 4 初始化      三个三个取 next code是 6，因为是初始化 所以代码表是（012345）
再 011 -> 1 代码表（012345）没有7 继续3个3个取， 代码表加入next code（0123456）， next code 变为 7
再 110 -> 6 代码表  (0123456)  没有7，继续3个三个取，代码表里面加入next code（01234567），next code变为 8
再 110 -> 6 代码表  (01234567) , 有7，变为4个4个取，代码表加入next code（012345678），next code变为9    
'''