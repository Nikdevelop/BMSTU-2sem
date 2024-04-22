import PyQt6.QtCore
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QFileDialog,
    QErrorMessage,
    QLineEdit,
    QLabel,
    QMessageBox,
    QWidget,
    QPlainTextEdit,
)
from PyQt6 import uic
import sys, os
import utils


def get_file_size_formatted(filename: str) -> float:
    size = os.stat(filename).st_size / 2**10
    return f"Size: {size:.2f} kB."


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("mainwindow.ui", self)

        self.imagefile = None
        self.datafile = None
        self.original_pixmap = None
        self.modified_pixmap = None

        self.img_tb: QLineEdit
        self.data_tb: QLineEdit

        self.original_img: QLabel
        self.modified_img: QLabel

        self.imgSize_label: QLabel
        self.dataSize_label: QLabel

        self.openImage_btn: QPushButton
        self.openData_btn: QPushButton

        self.decode_btn: QPushButton
        self.encode_btn: QPushButton

        self.save_img_action: QAction

        self.save_img_action.triggered.connect(self.SaveModifiedImage)

        self.openImage_btn.clicked.connect(self.GetImageFile)
        self.openData_btn.clicked.connect(self.GetDataFile)

        self.decode_btn.clicked.connect(self.DecodeMsg)
        self.encode_btn.clicked.connect(self.EncodeMsg)

    def OpenFileDialog(self, **params):
        filename = QFileDialog.getOpenFileName(self, **params)
        return filename[0] if filename[0] else None

    def GetDataFile(self):
        file = self.OpenFileDialog(caption="Open data file", filter="All Files (*.*)")
        if not file:
            QErrorMessage(self).showMessage("Error while opening file")
            return None

        self.datafile = file

        self.data_tb.clear()
        self.data_tb.insert(file)

        self.dataSize_label.setText(get_file_size_formatted(file))

    def GetImageFile(self):
        file = self.OpenFileDialog(
            caption="Open image file", filter="Image Files (*.png *.jpg *.bmp)"
        )
        if not file:
            QErrorMessage(self).showMessage("Error while opening file")
            return None

        self.imagefile = file
        self.img_tb.clear()
        self.img_tb.insert(file)

        self.imgSize_label.setText(get_file_size_formatted(file))
        self.OpenImageFile()

    def ScalePixmap(self, viewer, pixmap: QPixmap) -> QPixmap:
        height, width = viewer.height(), viewer.width()
        return pixmap.scaled(
            width, height, PyQt6.QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )

    def OpenImageFile(self):
        self.original_pixmap = QPixmap(self.imagefile)
        pixmap = self.ScalePixmap(self.original_img, self.original_pixmap)

        self.SetPixmap(self.original_img, pixmap)

    def SetPixmap(self, viewer, pixmap: QPixmap):
        viewer.setPixmap(pixmap)

    def DecodeMsg(self):
        result = utils.decode_data(self.original_pixmap)
        decoded_window = DecodedMsg(self, result)
        decoded_window.show()

    def SaveModifiedImage(self):
        if not self.modified_pixmap:
            QErrorMessage(self).showMessage("Nothing to save")
            return None

        file = QFileDialog.getSaveFileName(
            self, "Save image", filter="Image Files (*.png)"
        )
        self.modified_pixmap.save(file[0])

    def EncodeMsg(self):
        if not self.imagefile or not self.datafile:
            QErrorMessage(self).showMessage("You did not choose image or data file")
            return None
        data = open(self.datafile, "r").read().encode()

        self.modified_pixmap = utils.encode_data(data, self.original_pixmap)

        self.SetPixmap(
            self.modified_img,
            self.ScalePixmap(
                self.modified_img, QPixmap.fromImage(self.modified_pixmap)
            ),
        )


class DecodedMsg(QWidget):
    def __init__(self, parent, message: str) -> None:
        super(DecodedMsg, self).__init__(parent, PyQt6.QtCore.Qt.WindowType.Window)
        uic.loadUi("decodedtext.ui", self)

        self.text_tb: QPlainTextEdit
        self.text_tb.setPlainText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
