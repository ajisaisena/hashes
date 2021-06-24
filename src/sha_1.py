from hash_lib import padding, rot_left


def mes_schedule(mes):
    """
    消息扩展
    :param mes:填充后64字节消息，bytes
    :return: w[int]
    """
    w = []
    for i in range(16):
        w.append(int(mes[4 * i:4 * (i + 1)].hex(), 16))
    for i in range(16, 80):
        w.append(rot_left(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))
    return w


def sha_1(mes):
    """
    sha-1 实现函数
    :param mes: 需要hash的消息，bytes or str
    :return: sha-1 16进制值,str
    """
    paded = padding(mes)
    result = ''
    block_num = len(paded) // 64
    h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    for i in range(block_num):

        w = mes_schedule(paded[64 * i:64 * (i + 1)])
        a, b, c, d, e = h
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) ^ (~b & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8f1bbcdc
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            a, b, c, d, e = ((rot_left(a, 5) + f + e + k + w[j]) & 0xffffffff,
                             a, rot_left(b, 30), c, d)
        h[0], h[1], h[2], h[3], h[4] = (h[0] + a) & 0xffffffff, (h[1] + b) & 0xffffffff, (h[2] + c) & 0xffffffff, (
            h[3] + d) & 0xffffffff, (h[4] + e) & 0xffffffff
    for i in range(5):
        result += '{:08X}'.format(h[i])
    return result


def main():
    print(sha_1(b''))


if __name__ == '__main__':
    main()
