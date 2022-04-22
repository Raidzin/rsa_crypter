from PyQt5.QtCore import QThread, pyqtSignal

from modules.cryptography.reader import FileCryptographer


class KeygenThread(QThread):
    write_keys = pyqtSignal(object)

    def __init__(self, cryptographer, key_length):
        super(KeygenThread, self).__init__()
        self.cryptographer = cryptographer
        self.cryptographer.key_length = key_length

    def run(self):
        keys = self.cryptographer.keygen()
        self.write_keys.emit(keys)


class CryptThread(QThread):
    job_done = pyqtSignal(object)
    progressbar = pyqtSignal(int)

    def __init__(self, name, encrypt, file_path, cryptographer):
        super(CryptThread, self).__init__()
        self.name = name
        self.encrypt = encrypt
        self.file_cryptographer = FileCryptographer(file_path, cryptographer)

    def run(self):
        if self.encrypt:
            crypter = self.file_cryptographer.get_file_encrypter()
            file_len = self.file_cryptographer.get_chunks_count()
        else:
            crypter = self.file_cryptographer.get_file_decrypter()
            file_len = self.file_cryptographer.get_lines_count()
        percent = 0
        for part_number in crypter:
            new_percent = round(part_number / file_len * 100)
            if new_percent != percent:
                self.progressbar.emit(new_percent)
                percent = new_percent
        self.job_done.emit(self.name)


