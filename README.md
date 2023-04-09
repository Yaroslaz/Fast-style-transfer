# Fast-style-transfer
This code contains the implementation of a window application for styling images.
The window contains buttons for selecting an image and a style, as well as a button for starting the styling process.

The code also defines functions for loading, processing and displaying images, as well as for styling.

The necessary modules are imported, including the TensorFlow library and its TensorFlow Hub extension, libraries for working with images and the PyQt graphical interface.

It then defines a crop_center function to crop the center of the image, a load_image function to load and process an image, and a show_n function to display multiple images together.

Next, the StyleTransferWindow class is defined to create a window and its elements and functions to process them. Within the class, functions are defined to display the selected image and style, as well as a function to display the stylized image.

The buttons are processed by the select_content_image, select_style_image, and transfer_style functions, which call up the appropriate file selection dialogs and run the corresponding functions.

Basically, this code implements a GUI to perform image styling operation using TensorFlow and TensorFlow Hub.
---------------------------------------------------------------------------------------------------------------------
Данный код содержит реализацию оконного приложения для стилизации изображений.
Окно содержит кнопки для выбора изображения и стиля, а также кнопку для запуска процесса стилизации.

Также в коде определены функции для загрузки, обработки и отображения изображений, а также для стилизации.

Импортируются необходимые модули, включая библиотеку TensorFlow и ее расширение TensorFlow Hub, библиотеки для работы с изображениями и графическим интерфейсом PyQt.

Затем определяется функция crop_center для обрезания центральной части изображения, функция load_image для загрузки и обработки изображения и функция show_n для отображения нескольких изображений вместе.

Далее определяется класс StyleTransferWindow для создания окна и его элементов и функций для их обработки. Внутри класса определены функции для отображения выбранного изображения и стиля, а также функция для отображения стилизованного изображения.

Кнопки обрабатываются функциями select_content_image, select_style_image и transfer_style, которые вызывают соответствующие диалоговые окна для выбора файлов и запускают соответствующие функции.

В целом, данный код реализует графический интерфейс для выполнения операции стилизации изображений с помощью TensorFlow и TensorFlow Hub.
