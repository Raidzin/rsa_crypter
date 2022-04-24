from os import path

from modules.cryptography.cryptographer import RSACryptographer


class FileCryptographer:
    def __init__(self, file_path, cryptographer: RSACryptographer):
        self.file_path = file_path
        self.cryptographer = cryptographer
        self.chunk_length = self.get_chuck_length()
        self.crypto_filename = 'crypto_file'
        self.encoding = 'utf-8'

    def get_file_encrypter(self):
        self.write_crypto_file_name()
        file_reader = self.get_file_reader()
        with open(self.crypto_filename, 'a') as crypto_file:
            for iteration, part in enumerate(file_reader):
                crypto_part = bytearray(self.cryptographer.encrypt(part)).hex()
                crypto_file.write(str(crypto_part) + '\n')
                yield iteration + 1

    def get_file_decrypter(self):
        crypto_file_reader = self.get_crypto_file_reader()
        crypto_name = next(crypto_file_reader)
        crypto = bytes.fromhex(crypto_name)
        filename = self.cryptographer.decrypt(crypto)
        with open(filename, 'ab') as decrypto_file:
            for iteration, crypto_line in enumerate(crypto_file_reader):
                crypto = bytes.fromhex(crypto_line)
                data = self.cryptographer.decrypt(crypto)
                decrypto_file.write(data)
                yield iteration + 1

    def get_crypto_file_reader(self):
        with open(self.file_path, 'r') as crypto_file:
            line = crypto_file.readline()
            while line:
                yield line
                line = crypto_file.readline()

    def get_file_reader(self):
        with open(self.file_path, 'rb') as file_to_encrypt:
            line = file_to_encrypt.read(self.chunk_length)
            while line:
                yield line
                line = file_to_encrypt.read(self.chunk_length)

    def write_crypto_file_name(self):
        with open(self.crypto_filename, 'w') as crypto_file:
            crypto_file.write(self.get_hex_filename())

    def get_hex_filename(self):
        return str(
            bytearray(
                self.cryptographer.encrypt(
                    path.basename(self.file_path).encode(self.encoding)
                )
            ).hex()
        ) + '\n'

    def get_lines_count(self):
        with open(self.file_path) as file:
            return sum(
                chunk.count('\n') for chunk in iter(
                    lambda: file.read(64), ''
                )
            )

    def get_chunks_count(self):
        with open(self.file_path, 'rb') as file:
            count = 0
            chunk_length = self.get_chuck_length()
            chunk = file.read(chunk_length)
            while chunk:
                count += 1
                chunk = file.read(chunk_length)
            return count

    def get_chuck_length(self):
        return self.cryptographer.key_length // 10


# if __name__ == '__main__':
#     crypter = RSACryptographer()
#     crypter.keygen()
#     print('ключи готовы')
#     file_crypter = FileCryptographer(r'D:\Users\Alexey\Pictures\гг.PNG',
#                                      crypter)
#     file_encrypter = file_crypter.get_file_encrypter()
#     file_len = file_crypter.get_chunks_count()
#     for i in file_encrypter:
#         print(i / file_len * 100)
#     file_decrypter = file_crypter.get_file_decrypter()
#     print('зашифровал')
#     file_crypter.file_path = 'crypto_file'
#     file_len = file_crypter.get_lines_count()
#     for i in file_decrypter:
#         print(i / file_len * 100)
#     print('расшифровал')
# Переделать это в тесты!
