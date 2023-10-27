# Системная библиотека для ошибок
import sys
# Импорт компонета-приложения
from PyQt5.QtWidgets import QApplication
# Импортируем классы окон из другого файл
from avatar_window import KidsSwapAvatar, KidsSwapMain, KidsSwapRegist, KidsSwapAut


# Функция для вывода ошибок, в местах где не выводится
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# Старт программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Создаем ссылки на все окна
    window1 = KidsSwapMain()
    window2 = KidsSwapAvatar()
    window3 = KidsSwapRegist()
    window4 = KidsSwapAut()
    window1.set_windows(window1, window2, window3, window4)
    window2.set_windows(window1, window2, window3, window4)
    window3.set_windows(window1, window2, window3, window4)
    window4.set_windows(window1, window2, window3, window4)
    # Открываем первое окно
    window1.show()
    # Прописываем, что нужно выводить ошибку в местах, где не выводится
    sys.excepthook = except_hook
    # Закрытие приложения
    sys.exit(app.exec_())
