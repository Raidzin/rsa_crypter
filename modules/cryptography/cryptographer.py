import rsa


class RSACryptographer:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.key_length = 2048

    def encrypt(self, data):
        return rsa.encrypt(data, self.public_key)

    def decrypt(self, data):
        return rsa.decrypt(data, self.private_key)

    def keygen(self):
        self.public_key, self.private_key = rsa.newkeys(self.key_length)
        return self.public_key, self.private_key

    def set_public_key(self, public_key_path):
        with open(public_key_path, 'rb') as file:
            self.public_key = rsa.PublicKey.load_pkcs1(file.read())

    def set_private_key(self, private_key_path):
        with open(private_key_path, 'rb') as file:
            self.private_key = rsa.PrivateKey.load_pkcs1(file.read())
