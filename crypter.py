from os import getcwd
from os.path import join

from PyQt5 import QtWidgets, uic
import rsa

from design import make_design


class Cryptor:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.message = None
        self.private_key_path = None
        self.public_key_path = None
        self.message_path = None
        self.prefix = None

        make_design()

        self.app = QtWidgets.QApplication([])
        self.ui = uic.loadUi('design_v2.ui')

        self.ui.choose_public.clicked.connect(self.get_public_key)
        self.ui.choose_private.clicked.connect(self.get_private_key)
        self.ui.message.clicked.connect(self.get_message)
        self.ui.keygen.clicked.connect(self.keygen)
        self.ui.write.clicked.connect(self.write)
        self.ui.read.clicked.connect(self.read)

    def get_public_key(self):
        public_key_path, ok = QtWidgets.QFileDialog.getOpenFileName()
        if ok:
            self.set_public_key(public_key_path)

    def get_private_key(self):
        private_key_path, ok = QtWidgets.QFileDialog.getOpenFileName()
        if ok:
            self.set_private_key(private_key_path)

    def get_message(self):
        message_path, ok = QtWidgets.QFileDialog.getOpenFileName()
        if ok:
            self.set_message(message_path)

    def keygen(self):
        public_key, private_key = rsa.newkeys(1024)
        public_key_path = join(getcwd(), 'public.key')
        private_key_path = join(getcwd(), 'private.key')

        with open(public_key_path, 'wb') as file:
            file.write(public_key.save_pkcs1())
        with open(private_key_path, 'wb') as file:
            file.write(private_key.save_pkcs1())

        self.set_public_key(public_key_path)
        self.set_private_key(private_key_path)

    def write(self):
        if not self.public_key:
            return
        text: str = self.ui.text.toPlainText()
        crypto = rsa.encrypt(
            text.encode(encoding='utf8'),
            self.public_key
        )
        with open(join(getcwd(), 'message.msg'), 'wb') as file:
            file.write(crypto)

    def read(self):
        if not self.private_key or not self.message:
            return
        text = rsa.decrypt(self.message, self.private_key)
        self.ui.text.setPlainText(text.decode('utf8'))

    def set_public_key(self, public_key_path):
        with open(public_key_path, 'rb') as file:
            key = file.read()
            self.public_key = rsa.PublicKey.load_pkcs1(key)
        self.public_key_path = public_key_path
        self.ui.pub_path.setText(public_key_path)

    def set_private_key(self, private_key_path):
        with open(private_key_path, 'rb') as file:
            key = file.read()
            self.private_key = rsa.PrivateKey.load_pkcs1(key)
        self.private_key_path = private_key_path
        self.ui.priv_path.setText(private_key_path)

    def set_message(self, message_path):
        with open(message_path, 'rb') as file:
            self.message = file.read()
        self.message_path = message_path
        self.ui.message_label.setText(message_path)

    def start(self):
        self.ui.show()
        self.app.exec()


if __name__ == '__main__':
    program = Cryptor()
    program.start()
