from os import getcwd
from os.path import join

from PyQt5 import QtWidgets

import modules.messages as messages
from modules.cryptography.cryptographer import RSACryptographer
from modules.threads import KeygenThread, EncryptThread, DecryptThread
from ui_designs.py_designs.design_v2 import Ui_MainWindow


class Crypter(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cryptographer = RSACryptographer()

        self.file_path = None

        self.open_file_btn.clicked.connect(self.open_file)
        self.open_public_key_btn.clicked.connect(self.open_public_key)
        self.open_private_key_btn.clicked.connect(self.open_private_key)

        self.keygen_btn.clicked.connect(self.keygen)
        self.encrypt_btn.clicked.connect(self.encrypt)
        self.decrypt_btn.clicked.connect(self.decrypt)

        self.key_length_dial.valueChanged.connect(self.update_lcd)

    def open_public_key(self):
        public_key_path, ok = QtWidgets.QFileDialog.getOpenFileName(
            filter="*.key")
        if ok:
            self.set_public_key(public_key_path)

    def open_private_key(self):
        private_key_path, ok = QtWidgets.QFileDialog.getOpenFileName(
            filter="*.key")
        if ok:
            self.set_private_key(private_key_path)

    def open_file(self):
        message_path, ok = QtWidgets.QFileDialog.getOpenFileName()
        if ok:
            self.set_file(message_path)

    def keygen(self):
        self.switch_buttons()
        self.progressBar.setRange(0, 0)
        self.keygen_thread = KeygenThread(
            self.cryptographer,
            2 ** self.key_length_dial.value()
        )
        self.keygen_thread.finished.connect(self.keygen_thread.deleteLater)
        self.keygen_thread.write_keys.connect(self.write_keys)
        self.keygen_thread.start()

    def write_keys(self, keys):
        public_key, private_key = keys
        public_key_path = join(getcwd(), 'public.key')
        private_key_path = join(getcwd(), 'private.key')

        with open(public_key_path, 'wb') as file:
            file.write(public_key.save_pkcs1())
        with open(private_key_path, 'wb') as file:
            file.write(private_key.save_pkcs1())

        self.public_key_browse.setText(public_key_path)
        self.private_key_browse.setText(private_key_path)

        self.progressBar.setRange(0, 100)
        self.switch_buttons()
        self.errors_lbl.setText(messages.KEY_GENERATED)

    def update_lcd(self):
        value = self.key_length_dial.value()
        if value == 12:
            self.errors_lbl.setText(messages.OVERLOAD)
        else:
            self.errors_lbl.setText('')
        self.key_length_lcd.display(2 ** value)

    def encrypt(self):
        if not self.file_path:
            self.errors_lbl.setText(messages.FILE_NOT_CHOSEN)
            return
        if not self.cryptographer.public_key:
            self.errors_lbl.setText(messages.PUBLIC_KEY_NOT_CHOSEN)
            return

        self.switch_buttons()
        self.encrypt_thread = EncryptThread(
            file_path=self.file_path,
            cryptographer=self.cryptographer,
            final_message=messages.ENCRYPT_FINISHED,
        )
        self.encrypt_thread.progressbar.connect(self.progressBar.setValue)
        self.encrypt_thread.wait_time.connect(self.errors_lbl.setText)
        self.encrypt_thread.job_done.connect(self.set_message)
        self.encrypt_thread.finished.connect(self.encrypt_thread.deleteLater)
        self.encrypt_thread.start()

    def decrypt(self):
        if not self.file_path:
            self.errors_lbl.setText(messages.FILE_NOT_CHOSEN)
            return
        if not self.cryptographer.private_key:
            self.errors_lbl.setText(messages.PRIVATE_KEY_NOT_CHOSEN)
            return

        self.switch_buttons()
        self.decrypt_thread = DecryptThread(
            file_path=self.file_path,
            cryptographer=self.cryptographer,
            final_message=messages.DECRYPT_FINISHED,
        )
        self.decrypt_thread.progressbar.connect(self.progressBar.setValue)
        self.decrypt_thread.wait_time.connect(self.errors_lbl.setText)
        self.decrypt_thread.job_done.connect(self.set_message)
        self.decrypt_thread.finished.connect(self.decrypt_thread.deleteLater)
        self.decrypt_thread.start()

    def set_message(self, text):
        self.switch_buttons()
        self.errors_lbl.setText(text)

    def switch_buttons(self):
        self.progressBar.setValue(0)
        self.key_length_dial.setEnabled(not self.key_length_dial.isEnabled())
        self.keygen_btn.setEnabled(not self.keygen_btn.isEnabled())
        self.encrypt_btn.setEnabled(not self.encrypt_btn.isEnabled())
        self.decrypt_btn.setEnabled(not self.decrypt_btn.isEnabled())

    def set_public_key(self, public_key_path):
        self.cryptographer.set_public_key(public_key_path)
        self.public_key_browse.setText(public_key_path)

    def set_private_key(self, private_key_path):
        self.cryptographer.set_private_key(private_key_path)
        self.private_key_browse.setText(private_key_path)

    def set_file(self, file_path):
        self.file_path = file_path
        self.file_browse.setText(file_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Crypter()
    window.show()
    app.exec()
