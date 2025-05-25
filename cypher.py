import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


KEY = get_random_bytes(16) # load this from secure storage in real life

def encrypt(msg: str) -> str:
    iv   = get_random_bytes(16)
    aes  = AES.new(KEY, AES.MODE_CBC, iv)
    ciph = aes.encrypt(pad(msg.encode(), AES.block_size))
    blob = iv + ciph                      # 16-byte IV + ciphertext
    return base64.b64encode(blob).decode()   # => str, safe for JSON / sockets

def decrypt(token: str) -> str:
    blob = base64.b64decode(token.encode())
    iv, ciph = blob[:16], blob[16:]
    aes   = AES.new(KEY, AES.MODE_CBC, iv)
    plain = unpad(aes.decrypt(ciph), AES.block_size)
    return plain.decode()