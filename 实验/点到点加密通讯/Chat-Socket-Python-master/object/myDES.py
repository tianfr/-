import Crypto.Random as Random
from Cryptodome.Cipher import DES
import binascii

def generate_DES_key(key_len=8):
    return Random.get_random_bytes(key_len)

def encrypt_with_des(plain_text, key):
    des = DES.new(key, DES.MODE_ECB)
    plain_text = plain_text + (8 - (len(plain_text) % 8)) * '='
    encrypto_text = des.encrypt(plain_text.encode())
    encrypto_text = binascii.b2a_hex(encrypto_text)
    return encrypto_text

def decrypt_with_des(secret_byte_obj, key):
    des = DES.new(key, DES.MODE_ECB)
    decrypto_text = binascii.a2b_hex(secret_byte_obj)
    decrypto_text = des.decrypt(decrypto_text)

    return decrypto_text


if __name__ == "__main__":
    # 这是密钥
    des_key = Random.get_random_bytes(8)
    key = b'abcdefgh'   # key需为8字节长度.
    # 需要去生成一个DES对象
    des = DES.new(key, DES.MODE_ECB)
    # 需要加密的数据
    text = 'python spider!'*10000    # 被加密的数据需要为8字节的倍数.
    text = text + (8 - (len(text) % 8)) * '='
    print(text)
    # 加密的过程
    encrypto_text = des.encrypt(text.encode())
    encrypto_text = binascii.b2a_hex(encrypto_text)
    # print(encrypto_text)

    decrypto_text = binascii.a2b_hex(encrypto_text)
    # print(decrypto_text)
    decrypto_text = des.decrypt(decrypto_text)

    print(decrypto_text)