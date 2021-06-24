from sha_1 import *
import hmac


def hmac_sha1(key, message):
    """
    hmac-sha1 实现
    :param key: hmac密钥,str
    :param message: 需要认证的消息, str
    :return: mac值,str
    """
    key_bytes = key.encode()
    key_bytes = key_bytes + b'\x00' * (64 - len(key_bytes))
    mes_bytes = message.encode()
    key_int = int(key_bytes.hex(), 16)
    ipad = int('00110110' * 64, 2)
    opad = int('01011100' * 64, 2)
    key_ipad = ipad ^ key_int
    key_opad = opad ^ key_int
    ikey_hex = '{:0128x}'.format(key_ipad)
    okey_hex = '{:0128x}'.format(key_opad)
    ikey = bytes.fromhex(ikey_hex)
    okey = bytes.fromhex(okey_hex)
    ihash_hex = sha_1(ikey + mes_bytes)
    ihash = bytes.fromhex(ihash_hex)
    ohash = sha_1(okey + ihash)
    return ohash


def main():
    print(hmac_sha1('123', 'aac'))
    message = b'aac'
    key = b'123'
    h = hmac.new(key, message, digestmod='SHA1')
    print(h.hexdigest())


if __name__ == '__main__':
    main()
