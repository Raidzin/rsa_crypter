from PyQt5.QtCore import QThread, pyqtSignal

from modules.cryptography.reader import FileCryptographer
from modules.timer import Timer


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
    wait_time = pyqtSignal(str)

    def __init__(self, file_path, cryptographer, final_message=''):
        super(CryptThread, self).__init__()
        self.final_message = final_message
        self._file_cryptographer = FileCryptographer(file_path, cryptographer)
        self._percent_of_completion = 0

        self.crypter = None
        self.file_len = 0

    def run(self):
        timer = Timer(self.file_len)
        timer.start()
        for part_number in self.crypter:
            self._update_progressbar(part_number)
            self.wait_time.emit(timer.get_waiting_time(part_number))
        self.job_done.emit(self.final_message)

    def _update_progressbar(self, part_number):
        new_percent_of_completion = round(part_number / self.file_len * 100)
        if new_percent_of_completion != self._percent_of_completion:
            self.progressbar.emit(new_percent_of_completion)
            self._percent_of_completion = new_percent_of_completion


class EncryptThread(CryptThread):
    def __init__(self, file_path, cryptographer, final_message):
        super(EncryptThread, self).__init__(
            file_path, cryptographer, final_message
        )
        self.crypter = self._file_cryptographer.get_file_encrypter()
        self.file_len = self._file_cryptographer.get_chunks_count()


class DecryptThread(CryptThread):
    def __init__(self, file_path, cryptographer, final_message):
        super(DecryptThread, self).__init__(
            file_path, cryptographer, final_message
        )
        self.crypter = self._file_cryptographer.get_file_decrypter()
        self.file_len = self._file_cryptographer.get_lines_count()
