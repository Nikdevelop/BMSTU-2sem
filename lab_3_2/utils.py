import numpy as np
import io
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QBuffer
import PIL.Image as Image
from ctypes import c_uint8

def transform_to_array(pixmap: QPixmap) -> np.ndarray:
    buffer = QBuffer()
    buffer.open(QBuffer.OpenModeFlag.ReadWrite)
    pixmap.save(buffer, "PNG")
    img = Image.open(io.BytesIO(buffer.data()))

    return np.array(img)


def transform_to_qimg(arr: np.ndarray) -> QImage:
    height, width, subpixSize = arr.shape
    bytesPerLine = subpixSize * width

    return QImage(arr.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)


def encode_data(data: bytes, pixmap: QPixmap) -> QImage:
    data += b"\x00"
    data_size = len(data)

    arr = transform_to_array(pixmap)
    ySize, xSize, subpixSize = arr.shape
    cur_bit = 7
    cur_byte = 0
    done = False

    for y_pos in range(ySize):
        for x_pos in range(xSize):
            for subpix_pos in range(subpixSize):
                if cur_bit < 0:
                    if cur_byte == data_size - 1:
                        done = True
                        break
                    cur_byte += 1
                    cur_bit = 7

                bit = 1 if (data[cur_byte] & (2**cur_bit)) else 0
                if bit:
                    arr[y_pos, x_pos, subpix_pos] |= 1
                else:
                    arr[y_pos, x_pos, subpix_pos] &= 0xfe

                cur_bit -= 1
                
            if done:
                break
        if done:
            break

    return transform_to_qimg(arr)


def decode_data(pixmap: QPixmap) -> str:
    arr = transform_to_array(pixmap)
    ySize, xSize, subpixSize = arr.shape
    result = bytes()
    buffer = 0
    cur_bit = 0
    null_byte = False

    for y_pos in range(ySize):
        if null_byte:
            break
        for x_pos in range(xSize):
            if null_byte:
                break
            for subpix_pos in range(subpixSize):
                if cur_bit > 7:
                    if buffer == 0:
                        null_byte = True
                        break

                    result += int(buffer).to_bytes(1, "little")
                    buffer = 0
                    cur_bit = 0

                buffer <<= 1
                buffer += arr[y_pos, x_pos, subpix_pos] & 1
                cur_bit += 1
    try:
        return result.decode()
    except:
        return "Unable to decode this text"
