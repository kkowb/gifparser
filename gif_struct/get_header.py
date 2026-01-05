def get_signature(hex_str):
    signature = hex_str[0:6]
    return signature
    pass


def get_version(hex_str):
    version = hex_str[6:12]
    return version
    pass


def get_header(hex_str):
    signature = get_signature(hex_str)
    version = get_version(hex_str)
    return signature, version
