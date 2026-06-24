import zlib
import base64
with open('keys/prod.keys', 'rb') as f:
    data = f.read()
compressed = zlib.compress(data)
encoded = base64.b64encode(compressed).decode('ascii')
with open('keys_data.py', 'w') as f:
    f.write(f'ENCRYPTED_KEYS = "{encoded}"\n')
