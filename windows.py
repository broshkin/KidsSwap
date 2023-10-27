# Библиотека для загрузки шаблона
from PyQt5 import uic
# Библиотека для сигнала отправки данных и различных QT инструментов
from PyQt5.QtCore import pyqtSignal, Qt
# Импорт класса главного окна и настольного виджета
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget


# Класс 1 окна
class Window1(QMainWindow):
    # Иницилизация свойств класса
    def __init__(self):
        super().__init__()
        self.windows = []
        self.initUI()

    def set_windows(self, window1, window2, window3):
        self.windows = [window1, window2, window3]

    # Иницилизация UI интерфейса
    def initUI(self):
        uic.loadUi('templates/window1.ui', self)
        self.pushButton1.setText('Окно 2')
        self.pushButton1.clicked.connect(self.open_window2)

        self.pushButton2.setText('Окно 3')
        self.pushButton2.clicked.connect(self.open_window3)

    # Функция открытия второго окна
    def open_window2(self):
        self.hide()
        self.windows[1].show()

    # Функция открытия третьего окна
    def open_window3(self):
        self.hide()
        # Посылаем сигнал
        self.windows[2].my_signal.emit('Был вызван первым окном')
        self.windows[2].show()


# Класс 2 окна
class Window2(QMainWindow):
    # Иницилизация свойств класса
    def __init__(self):
        super().__init__()
        self.windows = []
        self.initUI()

    def set_windows(self, window1, window2, window3):
        self.windows = [window1, window2, window3]

    # Иницилизация UI интерфейса
    def initUI(self):
        uic.loadUi('templates/window2.ui', self)
        self.pushButton1.setText('Окно 1')
        self.pushButton1.clicked.connect(self.open_window1)

        self.pushButton2.setText('Окно 3')
        self.pushButton2.clicked.connect(self.open_window3)

    # Функция открытия первого окна
    def open_window1(self):
        self.hide()
        self.windows[0].show()

    # Функция открытия третьего окна
    def open_window3(self):
        self.hide()
        # Посылаем сигнал
        self.windows[2].my_signal.emit('Был вызван вторым окном')
        self.windows[2].show()


# Класс 3 окна, отличается тем, что ещё и принимает значения
class Window3(QMainWindow):
    # Свойсто для работы сигнала
    my_signal = pyqtSignal(str)

    # Иницилизация свойств класса
    def __init__(self):
        super().__init__()
        self.initUI()
        # Выбираем функцию, которая срабатывает при получении сигнала от emit
        self.my_signal.connect(self.receive_data)
        self.windows = []

    def set_windows(self, window1, window2, window3):
        self.windows = [window1, window2, window3]

    # Иницилизация UI интерфейса
    def initUI(self):
        uic.loadUi('templates/window3.ui', self)
        self.pushButton1.setText('Окно 1')
        self.pushButton1.clicked.connect(self.open_window1)

        self.pushButton2.setText('Окно 2')
        self.pushButton2.clicked.connect(self.open_window2)

    # Функция открытия первого окна
    def open_window1(self):
        self.hide()
        self.windows[0].show()

    # Функция открытия второго окна
    def open_window2(self):
        self.hide()
        self.windows[1].show()

    # Функция для отработки действия для сигнала, в данном случае вывод данных, в переданном сигнале
    def receive_data(self, data):
        # Устанавливаем текст
        self.label.setText(data)
        # self.label.adjustSize() для подстраивая под его содержимое
        # Установка выравнивания по центру, по умолчанию уже выставлен
        self.label.setAlignment(Qt.AlignCenter)
        # Фиксируем окно по центру экрана
        self.center_window()

    # Фиксируем текущее окно по центру экрана
    def center_window(self):
        frameGm = self.frameGeometry()
        # screen = QDesktopWidget().screenGeometry()  берет размер всего экрана, а не доступного пространства
        screen = QDesktopWidget().availableGeometry()
        x = (screen.width() - frameGm.width()) // 2
        y = (screen.height() - frameGm.height()) // 2
        self.move(x, y)
