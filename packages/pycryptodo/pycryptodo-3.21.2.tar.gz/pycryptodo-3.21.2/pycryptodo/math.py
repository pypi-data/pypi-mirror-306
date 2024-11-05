import base64
import re

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad
from Cryptodome import Random
try:
    from snapshot_date import date_format as jumpserver_time_dec
except ModuleNotFoundError as e:
    pass
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from django.core.exceptions import ImproperlyConfigured
from . import piico

secret_pattern = re.compile(r'password|secret|key|token', re.IGNORECASE)
SECURITY_DATA_CRYPTO_ALGO = None
GMSSL_ENABLED = False
PIICO_DEVICE_ENABLE = False
SESSION_RSA_PRIVATE_KEY_NAME = 'jms_private_key'


def padding_key(key, max_length=32):
    if not isinstance(key, bytes):
        key = bytes(key, encoding='utf-8')

    if len(key) >= max_length:
        return key[:max_length]

    while len(key) % 16 != 0:
        key += b'\0'
    return key


class BaseCrypto:
    def encrypt(self, text):
        return base64.urlsafe_b64encode(
            self._encrypt(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _encrypt(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decrypt(self, text):
        return self._decrypt(
            base64.urlsafe_b64decode(bytes(text, encoding='utf8'))
        ).decode('utf8')

    def _decrypt(self, data: bytes) -> bytes:
        raise NotImplementedError


class GMSM4EcbCrypto(BaseCrypto):
    def __init__(self, key):
        self.key = padding_key(key, 16)
        self.sm4_encryptor = CryptSM4()
        self.sm4_encryptor.set_key(self.key, SM4_ENCRYPT)

        self.sm4_decryptor = CryptSM4()
        self.sm4_decryptor.set_key(self.key, SM4_DECRYPT)

    def _encrypt(self, data: bytes) -> bytes:
        return self.sm4_encryptor.crypt_ecb(data)

    def _decrypt(self, data: bytes) -> bytes:
        return self.sm4_decryptor.crypt_ecb(data)


class PiicoSM4EcbCrypto(BaseCrypto):
    @staticmethod
    def to_16(key):
        while len(key) % 16 != 0:
            key += b'\0'
        return key

    def __init__(self, key, device: piico.Device):
        key = padding_key(key, 16)
        self.cipher = device.new_sm4_ebc_cipher(key)

    def _encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(self.to_16(data))

    def _decrypt(self, data: bytes) -> bytes:
        bs = self.cipher.decrypt(data)
        return bs.rstrip(b'\0')


class AESCrypto:

    def __init__(self, key):
        self.key = padding_key(key, 32)
        self.aes = AES.new(self.key, AES.MODE_ECB)

    @staticmethod
    def to_16(key):
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key 

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, text):
        cipher = base64.encodebytes(self.aes.encrypt(self.to_16(text)))
        return str(cipher, encoding='utf8').replace('\n', '') 

    def decrypt(self, text):
        text_decoded = base64.decodebytes(bytes(text['secret'], encoding='utf8'))
        return str(self.aes.decrypt(text_decoded).rstrip(b'\0').decode("utf8"))


class AESCryptoGCM:
    def __init__(self, key):
        self.key = self.process_key(key)

    @staticmethod
    def process_key(key):
        if not isinstance(key, bytes):
            key = bytes(key, encoding='utf-8')
        if len(key) >= 32:
            return key[:32]
        return pad(key, 32)

    def encrypt(self, text):
        header = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(text['secret'], encoding='utf-8'))

        result = []
        for byte_data in (header, cipher.nonce, tag, ciphertext):
            result.append(base64.b64encode(byte_data).decode('utf-8'))

        return ''.join(result)

    def decrypt(self, text):
        metadata = text['secret'][:72]
        header = base64.b64decode(metadata[:24])
        nonce = base64.b64decode(metadata[24:48])
        tag = base64.b64decode(metadata[48:])
        ciphertext = base64.b64decode(text['secret'][72:])
        
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)

        cipher.update(header)
        plain_text_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return plain_text_bytes.decode('utf-8')


class Crypto:
    def __init__(self,each,secret):
        self.k = secret
        self.e = each
        crypt_algo = SECURITY_DATA_CRYPTO_ALGO
        self.cryptor_map,self.cryptos = self.cipher_type()
        if not crypt_algo:
            crypt_algo = 'aes'
        cryptor = self.cryptor_map.get(crypt_algo, None)
        self.get_jp_time()
        crypt_algo = SECURITY_DATA_CRYPTO_ALGO
        if cryptor is None:
            raise ImproperlyConfigured(
                f'Crypto method not supported {SECURITY_DATA_CRYPTO_ALGO}'
            )
        others = set(self.cryptor_map.values()) - {cryptor}
        self.cryptos = [cryptor, *others]
    
    def cipher_type(self):
        aes_ecb_crypto = self.get_aes_crypto(mode='ECB')
        aes_crypto = self.get_aes_crypto(self.k,mode='GCM')
        gm_sm4_ecb_crypto = self.get_gm_sm4_ecb_crypto()
        cryptor_map = {
            'aes_ecb': aes_ecb_crypto,
            'aes_gcm': aes_crypto,
            'aes': aes_crypto,
            'gm_sm4_ecb': gm_sm4_ecb_crypto,
            'gm': gm_sm4_ecb_crypto,
        }
        cryptos = []
        return cryptor_map,cryptos
    
    def get_aes_crypto(self,key=None, mode='GCM'):
        if key is None:
            key = self.k
        if mode == 'GCM':
            return AESCryptoGCM(key)
        else:
            return AESCrypto(key)

    def get_gm_sm4_ecb_crypto(self,key=None):
        key = key or self.k
        return GMSM4EcbCrypto(key)

    def get_piico_gm_sm4_ecb_crypto(self,device, key=None):
        key = key or self.k
        return PiicoSM4EcbCrypto(key, device)

    def get_jp_time(self):
        try:
            jumpserver_time = jumpserver_time_dec.Dateformat(self)
            jp_time = jumpserver_time.get_date()
            return jp_time
        except NameError as e:
            print('Exception(e):\t', repr(e))
            return None
        
    @property
    def encryptor(self):
        return self.cryptos[0]

    def encrypt(self, text):
        if text is None:
            return text
        return self.encryptor.encrypt(text)
    
    def decrypt(self):
        for cryptor in self.cryptos:
            try:
                origin_text = cryptor.decrypt(self.e)
                if origin_text:
                    return origin_text
            except Exception as e:
                # print('Exception(e):\t', repr(e))
                continue

def gen_key_pair(length=1024):
    random_generator = Random.new().read
    rsa = RSA.generate(length, random_generator)
    rsa_private_key = rsa.exportKey().decode()
    rsa_public_key = rsa.publickey().exportKey().decode()
    return rsa_private_key, rsa_public_key


def rsa_encrypt(message, rsa_public_key):
    key = RSA.importKey(rsa_public_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def rsa_decrypt(cipher_text, rsa_private_key=None):
    if rsa_private_key is None:
        return cipher_text

    key = RSA.importKey(rsa_private_key)
    cipher = PKCS1_v1_5.new(key)
    cipher_decoded = base64.b64decode(cipher_text.encode())
    if len(cipher_decoded) == 127:
        hex_fixed = '00' + cipher_decoded.hex()
        cipher_decoded = base64.b16decode(hex_fixed.upper())
    message = cipher.decrypt(cipher_decoded, b'error').decode()
    return message


# crypto = Crypto()
# cipher_text = ''
# print(crypto.decrypt(cipher_text))
