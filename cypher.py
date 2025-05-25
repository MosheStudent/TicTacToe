from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Fixed 256-bit key (32 bytes) for AES encryption
# In a production environment, securely generate and share this key
KEY = b'Sixteen byte key padded to 32!!!'

def encrypt(text):
    # Convert text to bytes
    text_bytes = text.encode('utf-8')
    
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    
    # Pad the text to be a multiple of 16 bytes (AES block size)
    pad_length = 16 - (len(text_bytes) % 16)
    text_bytes += bytes([pad_length] * pad_length)
    
    # Create cipher and encrypt
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text_bytes) + encryptor.finalize()
    
    # Return IV + ciphertext
    return iv + ciphertext

def decrypt(data):
    # Extract IV (first 16 bytes) and ciphertext
    iv = data[:16]
    ciphertext = data[16:]
    
    # Create cipher and decrypt
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    pad_length = padded_text[-1]
    text_bytes = padded_text[:-pad_length]
    
    # Convert back to string
    return text_bytes.decode('utf-8')