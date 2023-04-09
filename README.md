# Fast-style-transfer
This code contains the implementation of a window application for styling images.
The window contains buttons for selecting an image and a style, as well as a button for starting the styling process.

The code also defines functions for loading, processing and displaying images, as well as for styling.

The necessary modules are imported, including the TensorFlow library and its TensorFlow Hub extension, libraries for working with images and the PyQt graphical interface.

It then defines a crop_center function to crop the center of the image, a load_image function to load and process an image, and a show_n function to display multiple images together.

Next, the StyleTransferWindow class is defined to create a window and its elements and functions to process them. Within the class, functions are defined to display the selected image and style, as well as a function to display the stylized image.

The buttons are processed by the select_content_image, select_style_image, and transfer_style functions, which call up the appropriate file selection dialogs and run the corresponding functions.

Basically, this code implements a GUI to perform image styling operation using TensorFlow and TensorFlow Hub.
