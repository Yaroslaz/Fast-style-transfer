import os
import sys
import functools
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from matplotlib import gridspec
import matplotlib.pyplot as plt

print("TF Version: ", tf.__version__)
print("TF Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))

def crop_center(image):
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

@functools.lru_cache(maxsize=None)
def load_image(image_path, image_size=(512, 512), preserve_aspect_ratio=True):
    img = tf.io.decode_image(
        tf.io.read_file(image_path),
        channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

def show_n(images, titles=('',)):
    n = len(images)
    image_sizes = [image.shape[1] for image in images]
    w = (image_sizes[0] * 6) // 320
    plt.figure(figsize=(w * n, w))
    gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
    for i in range(n):
        plt.subplot(gs[i])
        plt.imshow(images[i][0], aspect='equal')
        plt.axis('off')
        plt.title(titles[i] if len(titles) > i else '')
    plt.show()



class StyleTransferWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Логотип
        self.logo_label = QLabel(self)
        self.logo_label.setGeometry(10, 10, 100, 100)
        logo_path = os.path.join(os.path.dirname(sys.argv[0]), 'logo.svg')
        pixmap = QPixmap(logo_path).scaled(self.logo_label.width(), self.logo_label.height())
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)

        # Фон
        self.setStyleSheet("background-color: #282828")


        self.content_label = QLabel(self)
        self.content_label.setGeometry(125, 210, 256, 256) #Расположение выбранного изображения

        self.style_label = QLabel(self)
        self.style_label.setGeometry(472, 210, 256, 256) #Расположение выбранного стиля

        self.stylized_label = QLabel(self)
        self.stylized_label.setGeometry(295, 566, 256, 256) #Расположение стилизованного изображения

        # Название окна
        self.setWindowTitle("Style Transfer")
        self.setGeometry(100, 100, 840, 900)

        # Кнопки
        self.content_button = QPushButton("Выберите изображение", self)
        self.content_button.setStyleSheet("background-color: white")
        self.content_button.move(180, 160) #Расположение кнопки выбора изображения
        self.content_button.setFixedSize(145, 40)
        self.content_button.clicked.connect(self.select_content_image)

        self.style_button = QPushButton("Выберите стиль", self)
        self.style_button.setStyleSheet("background-color: white")
        self.style_button.move(540, 160) #Расположение кнопки выбора стиля
        self.style_button.setFixedSize(120, 40)
        self.style_button.clicked.connect(self.select_style_image)

        self.transfer_button = QPushButton("Стилизовать", self)
        self.transfer_button.setStyleSheet("background-color: white")
        self.transfer_button.move(375, 516) #Расположение кнопки стилизации
        self.transfer_button.setFixedSize(100, 40)
        self.transfer_button.clicked.connect(self.transfer_style)
        self.transfer_button.setEnabled(False)

        # настройка пути для изображения
        self.content_image_path = None
        self.style_image_path = None

        # установка размера изображений
        self.content_img_size = (1024, 1024)
        self.style_img_size = (512,512)

    from PyQt6.QtGui import QPixmap

    def show_image(self, label, image_path):
        pixmap = QPixmap(image_path).scaled(label.width(), label.height())
        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def show_content_image(self):
        if self.content_image_path:
            self.show_image(self.content_label, self.content_image_path)

    def show_style_image(self):
        if self.style_image_path:
            self.show_image(self.style_label, self.style_image_path)

    def show_stylized_image(self, image):
        stylized_image = np.squeeze(image.numpy())
        self.stylized_image_path = "stylized_image.jpg"
        plt.imsave(self.stylized_image_path, stylized_image)
        self.show_image(self.stylized_label, self.stylized_image_path)

    def select_content_image(self):
        self.content_image_path, _ = QFileDialog.getOpenFileName(self, "Select Content Image")
        if self.content_image_path and self.style_image_path:
            self.transfer_button.setEnabled(True)
        self.show_content_image()
        print("Selected content image:", self.content_image_path)

    def select_style_image(self):
        """Выбор стиля"""
        self.style_image_path, _ = QFileDialog.getOpenFileName(self, "Select Style Image")
        if self.content_image_path and self.style_image_path:
            self.transfer_button.setEnabled(True)
        self.show_style_image()
        print("Selected style image:", self.style_image_path)

    def transfer_style(self):
        """Перенос стиля из изображения стиля в изображение содержимого."""

        # загрузка изображения
        content_image = load_image(self.content_image_path, self.content_img_size)
        style_image = load_image(self.style_image_path, self.style_img_size)

        # загрузка модели из хаба
        hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

        # Стилизация изображение содержимого с помощью изображения стиля
        stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]

        # Отображение резульатата
        self.show_stylized_image(stylized_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Создаем окно
    window = StyleTransferWindow()
    window.show()

    # зацикливаем
    sys.exit(app.exec())