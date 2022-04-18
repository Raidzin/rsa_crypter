from PyQt5.QtCore import QThread, pyqtSignal


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

    def __init__(self, name, function, file_path, cryptographer, progressbar, label):
        super(CryptThread, self).__init__()
        self.name = name
        self.function = function
        self.file_path = file_path
        self.cryptographer = cryptographer
        self.progressbar = progressbar
        self.label = label

    def run(self):
        self.function(self.file_path, self.cryptographer, self.progressbar, self.label)
        self.job_done.emit(self.name)
