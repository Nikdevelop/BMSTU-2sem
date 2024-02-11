from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6 import uic
import sys
import utils

cur_10_to_9 = True
PREC = 10
ALLOWED_SYMBOLS = ".0123456789"


def change_mode(window):
    global cur_10_to_9
    cur_10_to_9 = not cur_10_to_9
    window.pushButton9.setEnabled(cur_10_to_9)
    if cur_10_to_9:
        window.pushButton_change_mode.setText("10 -> 9")
    else:
        window.pushButton_change_mode.setText("9 -> 10")


def append_to_textbox(textbox, num):
    textbox.insert(str(num))


def convert(textbox, main_widget):
    global cur_10_to_9
    number = textbox.text()
    if cur_10_to_9:
        if "." in number:
            converted = utils.convert_float(number, 10, 9, PREC)
        else:
            converted = utils.convert_int(number, 10, 9)
    else:
        if "9" in number:
            QMessageBox.critical(main_widget, "Error", "Incorrect number!")
            textbox.clear()
            return
        if "." in number:
            converted = utils.convert_float(number, 9, 10, PREC)
        else:
            converted = utils.convert_int(number, 9, 10)

    textbox.clear()
    textbox.insert(converted)


def clear_textbox(textbox):
    textbox.clear()


def show_info(window):
    QMessageBox.about(
        window, "Информация об авторе", "Выполнил Жижин Никита.\nГруппа: ИУ7-21Б"
    )


def check_input(textbox):
    global cur_10_to_9
    cur_allowed = ALLOWED_SYMBOLS
    if not cur_10_to_9:
        cur_allowed = cur_allowed[:-1]

    if (
        any(s not in cur_allowed for s in textbox.text())
        or textbox.text().count(".") > 1
    ):
        textbox.setText(textbox.text()[:-1])


def main():
    app = QApplication(sys.argv)
    window = uic.loadUi("MainWindow.ui")
    window.setFixedSize(467, 396)
    textbox = window.lineEdit
    textbox.textChanged.connect(lambda: check_input(textbox))
    window.pushButton0.clicked.connect(lambda: append_to_textbox(textbox, 0))
    window.pushButton1.clicked.connect(lambda: append_to_textbox(textbox, 1))
    window.pushButton2.clicked.connect(lambda: append_to_textbox(textbox, 2))
    window.pushButton3.clicked.connect(lambda: append_to_textbox(textbox, 3))
    window.pushButton4.clicked.connect(lambda: append_to_textbox(textbox, 4))
    window.pushButton5.clicked.connect(lambda: append_to_textbox(textbox, 5))
    window.pushButton6.clicked.connect(lambda: append_to_textbox(textbox, 6))
    window.pushButton7.clicked.connect(lambda: append_to_textbox(textbox, 7))
    window.pushButton8.clicked.connect(lambda: append_to_textbox(textbox, 8))
    window.pushButton9.clicked.connect(lambda: append_to_textbox(textbox, 9))
    window.pushButtonDot.clicked.connect(lambda: append_to_textbox(textbox, "."))
    window.pushButton_change_mode.clicked.connect(lambda: change_mode(window))
    window.pushButton_convert.clicked.connect(lambda: convert(textbox, window))
    window.menu.addAction("Clear text", lambda: clear_textbox(textbox))
    window.menu.addAction("About", lambda: show_info(window))

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
