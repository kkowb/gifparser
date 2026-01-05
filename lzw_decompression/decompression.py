from .decoder import DecoderBytes

def get_all_data(str):
    print("image data", str)
    min_code_size = int(str[0:2], 16)
    data = str[2:]
    all_data = ''
    while True:
        num_of_bytes = int(data[0:2], 16)
        if num_of_bytes == 0:
            break
        all_data += data[2: 2 + num_of_bytes * 2]
        data = data[2 + num_of_bytes * 2 :]
    return all_data, min_code_size


def hex_to_binary(hex_str):
    hex_str_length = len(hex_str)
    byte_hex_list = [hex_str[i:i+2] for i in range(0, hex_str_length, 2)]
    bit_chunks = []
    for hex_byte in byte_hex_list:
        decimal_val = int(hex_byte, 16)
        normal_bits = format(decimal_val, '08b')
        lsb_first_bits = normal_bits[::-1]
        bit_chunks.append(lsb_first_bits)
    full_bits = ''.join(bit_chunks)
    return full_bits


def get_code(binary, min_code_size):
    decoder = DecoderBytes(binary, min_code_size)
    decoder.start()


def decoding_bytes(str):
    all_data, min_code_size = get_all_data(str)
    print("all_data", all_data)
    binary = hex_to_binary(all_data)
    code = get_code(binary, min_code_size)