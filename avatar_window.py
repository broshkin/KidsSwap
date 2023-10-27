import sys

import sqlite3
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDesktopWidget

SCREEN_SIZE = [1920, 1080]
connection = sqlite3.connect("kidsswap.db")
cur = connection.cursor()


class KidsSwapAvatar(QMainWindow):
    data_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        uic.loadUi('templates/avatar_window.ui', self)
        self.setWindowTitle('Профиль')
        self.data_signal.connect(self.set_data)
        self.windows = []
        self.pixmap = ''

    def set_windows(self, window1, window2, window3, window4):
        self.windows = [window1, window2, window3, window4]

    def set_data(self, data):
        self.name_t.setText(data[0])
        self.age_t.setText(data[1])
        self.region_t.setText(data[2])
        self.pixmap = QPixmap(data[3])
        self.pixmap.setDevicePixelRatio((self.pixmap.height() + self.pixmap.width()) / (self.ava.width() +
                                                                                        self.ava.height()) * 1.5)
        self.ava.setPixmap(self.pixmap)
        self.ava.repaint()


class KidsSwapMain(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/main_window.ui', self)
        self.initUI()
        self.windows = []

    def set_windows(self, window1, window2, window3, window4):
        self.windows = [window1, window2, window3, window4]

    def initUI(self):
        self.setWindowTitle('Первоначальное окно')
        self.reg_b.clicked.connect(self.registration)
        self.login_b.clicked.connect(self.autorization)

    def registration(self):
        self.hide()

        self.windows[2].show()

    def autorization(self):
        self.hide()

        self.windows[3].show()


class KidsSwapRegist(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/regist_window.ui', self)
        self.initUI()
        self.data = []
        self.private_data = []
        self.windows = []
        self.pixmap = ''
        self.fname = ''
        self.sname = ''

    def set_windows(self, window1, window2, window3, window4):
        self.windows = [window1, window2, window3, window4]

    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.avatar_b.clicked.connect(self.avatar)
        self.regist_b.clicked.connect(self.regist)
        self.errorLabel.setText('')

    def avatar(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Выберите аватар', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        im = Image.open(self.fname)
        self.sname = f'avatars/{self.fname.split("/")[-1]}'
        im.save(self.sname)
        self.pixmap = QPixmap(self.fname)
        self.pixmap.setDevicePixelRatio((self.pixmap.height() + self.pixmap.width()) /
                                        (self.ava.width() + self.ava.height()) * 1.5)
        self.ava.setPixmap(self.pixmap)
        self.ava.repaint()

    def regist(self):
        allEmails = list(map(lambda x: x[0], cur.execute('''SELECT email FROM users''').fetchall()))
        if self.nameEdit.text() != '' and self.ageEdit.text() != '' and self.regionEdit.text() != '' \
                and self.emailEdit.text() != '' and self.passwordEdit.text() != '' \
                and self.emailEdit.text() not in allEmails and '@' in self.emailEdit.text() \
                and '.' in self.emailEdit.text():
            if self.pixmap == '':
                self.pixmap = QPixmap('default_avatar/empty_avatar.jpg')
                self.sname = 'default_avatar/empty_avatar.jpg'
                self.pixmap.setDevicePixelRatio((self.pixmap.height() + self.pixmap.width()) /
                                                (self.ava.width() + self.ava.height()) * 1.5)
                self.ava.setPixmap(self.pixmap)
                self.ava.repaint()

            self.data = [self.nameEdit.text(), self.ageEdit.text(), self.regionEdit.text(), self.sname]
            self.private_data = [self.emailEdit.text(), self.passwordEdit.text()]

            cur.execute(f'''INSERT INTO users (name, age, region, email, password, avatar) 
            VALUES("{self.data[0]}", {self.data[1]}, "{self.data[2]}", "{self.private_data[0]}",
             "{self.private_data[1]}", "{self.data[3]}");''')
            connection.commit()

            print(self.data)
            print(self.private_data)
            self.hide()
            self.windows[1].data_signal.emit(self.data)
            self.windows[1].show()
        elif self.nameEdit.text() == '':
            self.errorLabel.setText('Укажите имя пользователя')
        elif self.ageEdit.text() == '':
            self.errorLabel.setText('Укажите возраст')
        elif self.regionEdit.text() == '':
            self.errorLabel.setText('Укажите место для обмена товарами')
        elif self.emailEdit.text() == '' or '@' not in self.emailEdit.text() or '.' not in self.emailEdit.text():
            self.errorLabel.setText('Укажите корректный адрес электронной почты')
        elif self.passwordEdit.text() == '':
            self.errorLabel.setText('Укажите пароль')
        elif self.emailEdit.text() in allEmails:
            self.errorLabel.setText('Данный адрес электронной почты уже зарегистрирован')
        else:
            self.errorLabel.setText('Неизвестная ошибка регистрации, обратитесь в техническую поддержку сервиса')


class KidsSwapAut(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/aut_window.ui', self)
        self.initUI()
        self.data = []
        self.private_data = []
        self.windows = []
        self.pixmap = ''

    def set_windows(self, window1, window2, window3, window4):
        self.windows = [window1, window2, window3, window4]

    def initUI(self):
        self.setWindowTitle('Авторизация')
        self.aut_b.clicked.connect(self.aut)
        self.error_label.setText('')

    def aut(self):
        if self.emailEdit.text() != '' and self.passwordEdit.text() != '':
            allEmails = list(map(lambda x: x[0], cur.execute('''SELECT email FROM users''').fetchall()))
            if self.emailEdit.text() in allEmails:
                curPassword = cur.execute(
                    f'''SELECT password FROM users WHERE email="{self.emailEdit.text()}"''').fetchone()[0]
                if self.passwordEdit.text() == curPassword:
                    data = cur.execute(
                        f'''SELECT name, age, region, avatar FROM users WHERE email="{self.emailEdit.text()}"''').fetchall()
                    data = [data[0][0], str(data[0][1]), data[0][2], data[0][3]]
                    self.hide()
                    self.windows[1].data_signal.emit(data)
                    self.windows[1].show()


class KidsSwapExchange(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/regist_window.ui', self)
        self.initUI()
        self.data = []
        self.private_data = []
        self.windows = []
        self.pixmap = QPixmap()

    def set_windows(self, window1, window2, window3):
        self.windows = [window1, window2, window3]

    def initUI(self):
        self.setWindowTitle('Регистрация')
        self.avatar_b.clicked.connect(self.avatar)
        self.regist_b.clicked.connect(self.regist)
