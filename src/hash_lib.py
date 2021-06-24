def padding(mes):
    """
    sha-1/sm3 填充函数
    :param mes:需要填充的消息,bytes or str
    :return:填充后消息,bytes
    """
    mes_bytes = mes.encode() if isinstance(mes, str) else mes
    lens = len(mes_bytes)
    mes_hex = mes_bytes.hex()
    mes_bin = '{:0{}b}'.format(
        int(mes_hex, 16), lens * 8) if mes_hex != '' else ''
    k = (447 - lens * 8) % 512
    pad_bin = mes_bin + '1' + '0' * k + '{:064b}'.format(lens * 8)
    len_bin = len(pad_bin)
    pad_hex = '{:0{}X}'.format(int(pad_bin, 2), len_bin // 4)
    paded = bytes.fromhex(pad_hex)
    return paded


def rot_left(num, times):
    """
    循环左移函数
    :param num:需要左移的字节，int
    :param times: 需要左移的次数,int
    :return: 左移后的结果
    """
    return ((num << times) | (num >> (32 - times))) & 0xffffffff
