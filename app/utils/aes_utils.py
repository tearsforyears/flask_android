# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 16
PADDING = '\0'
pad_it = lambda s: s + (16 - len(s) % 16) * PADDING
key = b''
iv = b''


# 使用aes算法，进行加密解密操作
# 为跟java实现同样的编码，注意PADDING符号自定义
def encrypt_aes(sourceStr):
    # 注意这里 segment_size=128
    generator = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    # 注意这里先将明文通过 utf-8 转码成为字节串再调用 padding 算法
    padded = pad_byte(sourceStr.encode('utf-8'))
    crypt = generator.encrypt(padded)
    cryptedStr = base64.b64encode(crypt)
    return cryptedStr


def pad_byte(b):
    bytes_num_to_pad = BLOCK_SIZE - (len(b) % BLOCK_SIZE)
    byte_to_pad = bytes([bytes_num_to_pad])
    padding = byte_to_pad * bytes_num_to_pad
    padded = b + padding
    return padded


def decrypt_aes(cryptedStr):
    # 注意这里 segment_size=128
    generator = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    cryptedStr = base64.b64decode(cryptedStr)
    recovery = generator.decrypt(cryptedStr)
    decryptedStr = recovery.rstrip(PADDING.encode('utf-8'))
    return decryptedStr


if __name__ == '__main__':
    print(str(encrypt_aes("root"),encoding='utf-8'))