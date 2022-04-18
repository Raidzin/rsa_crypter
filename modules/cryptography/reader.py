from os import path

from modules.cryptography.cryptographer import RSACryptographer


def get_hex_file_name(file_path, cryptographer: RSACryptographer):
    return str(
        bytearray(
            cryptographer.encrypt(
                path.basename(file_path).encode('utf-8')
            )
        ).hex()
    ) + '\n'


def count_lines(filename, chunk_size=1 << 13):
    with open(filename) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


def count_bytes(filename, chunk_size=1 << 13):
    with open(filename, 'rb') as file:
        count = 0
        chunk = file.read(chunk_size)
        while chunk:
            count += 1
            chunk = file.read(chunk_size)
        return count


def encode_file(file_path, cryptographer, progressbar):
    buffer_size = cryptographer.key_length // 10
    chunk_number = 1
    file_len = count_bytes(file_path, buffer_size)
    with open(file_path, 'rb') as file:
        part = file.read(buffer_size)
        with open('crypto_file', 'w') as crypto_file:
            crypto_file.write(get_hex_file_name(file_path, cryptographer))
        with open('crypto_file', 'a') as crypto_file:
            while part:
                percent = round(chunk_number / file_len * 100)
                progressbar.setValue(percent)
                chunk_number += 1
                crypto_part = cryptographer.encrypt(part)
                crypto_part = bytearray(crypto_part)
                crypto_file.write(str(crypto_part.hex()) + '\n')
                part = file.read(buffer_size)


def decode_file(file_path, cryptographer, progressbar):
    file_len = count_lines(file_path)
    with open(file_path, 'r') as file:
        crypto = file.readline()
        chunk_number = 1
        filename = cryptographer.decrypt(bytes.fromhex(crypto))
        crypto = file.readline()
        crypto_file = open(filename, 'wb')
        crypto_file.close()
        with open(filename, 'ab') as decrypto_file:
            while crypto:
                percent = round(chunk_number / file_len * 100)
                progressbar.setValue(percent)
                chunk_number += 1
                crypto = bytes.fromhex(crypto)
                data = cryptographer.decrypt(crypto)
                decrypto_file.write(data)
                crypto = file.readline()


if __name__ == '__main__':
    print(count_lines(r'..\crypto_file'))
