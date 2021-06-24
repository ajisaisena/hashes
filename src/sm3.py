from hash_lib import *

iv = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
      0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]


def t(j):
    """
    sm3 t变量选取函数
    :param j: 轮数j, int
    :return: 指定的t值，int
    """
    return 0x79cc4519 if 0 <= j <= 15 else 0x7a879d8a


def ff(x, y, z, j):
    """
    sm3 ff 函数
    :param x: 第一个参数，int
    :param y: 第二个参数, int
    :param z: 第三个参数, int
    :param j: 轮数，int
    :return: ff函数结果
    """
    if 0 <= j <= 15:
        return x ^ y ^ z
    elif 16 <= j <= 63:
        return (x & y) | (x & z) | (y & z)


def gg(x, y, z, j):
    """
    sm3 gg函数
    :param x: 第一个参数, int
    :param y: 第二个参数, int
    :param z: 第三个参数, int
    :param j: 轮数, int
    :return: gg 计算结果，int
    """
    if 0 <= j <= 15:
        return x ^ y ^ z
    elif 16 <= j <= 63:
        return (x & y) | ((~x) & z)


def p(x, mode):
    """
    p_0和p_1函数集合
    :param x: 写入的字节,int
    :param mode: 选用的模式,0 or 1
    :return: p函数计算结果, int
    """
    if mode == 0:
        return x ^ rot_left(x, 9) ^ rot_left(x, 17)
    elif mode == 1:
        return x ^ rot_left(x, 15) ^ rot_left(x, 23)


def mes_expand(mes):
    """
    sm3 消息扩展
    :param mes:需要扩展的消息,bytes
    :return: 扩展后的消息,list[int]
    """
    w = []
    w_q = []
    for i in range(16):
        w.append(int(mes[4 * i:4 * (i + 1)].hex(), 16))
    for i in range(16, 68):
        w.append(p(w[i - 16] ^ w[i - 9] ^ rot_left(w[i - 3], 15), 1)
                 ^ rot_left(w[i - 13], 7) ^ w[i - 6])
    for i in range(64):
        w_q.append(w[i] ^ w[i + 4])
    return w, w_q


def cf(v, mes):
    """
    cf压缩函数
    :param v: 变量v,list[int] 
    :param mes: 扩展前填充后消息mes, bytes
    :return: 新一轮v函数, list[int]
    """
    a, b, c, d, e, f, g, h = v
    w, w_q = mes_expand(mes)
    for i in range(64):
        ss1 = rot_left(
            (rot_left(a, 12) + e + rot_left(t(i), i % 32)) & 0xffffffff, 7)
        ss2 = ss1 ^ rot_left(a, 12)
        tt1 = (ff(a, b, c, i) + d + ss2 + w_q[i]) & 0xffffffff
        tt2 = (gg(e, f, g, i) + h + ss1 + w[i]) & 0xffffffff
        a, b, c, d, e, f, g, h = tt1, a, rot_left(
            b, 9), c, p(tt2, 0), e, rot_left(f, 19), g
    v_plus = [a ^ v[0], b ^ v[1], c ^ v[2], d ^
              v[3], e ^ v[4], f ^ v[5], g ^ v[6], h ^ v[7]]
    return v_plus


def sm3(mes):
    """
    sm3实现函数
    :param mes: 需要进行哈希的消息，str or bytes
    :return: 16进制哈希值，str
    """
    mes_pad = padding(mes)
    rounds = len(mes_pad) // 64
    v = iv
    for i in range(rounds):
        v = cf(v, mes_pad[64 * i:64 * (i + 1)])
    result = ''
    for num in v:
        result += '{:08x}'.format(num)
    return result


def main():
    print(sm3('abc'))


if __name__ == '__main__':
    main()
