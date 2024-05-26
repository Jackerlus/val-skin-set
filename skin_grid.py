from PySide6.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QPushButton, QToolButton
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtCore import Qt
from PIL import Image
import urllib.request
from io import BytesIO

class SkinGrid(QWidget):
    def __init__(self, skin_data, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        self.setLayout(layout)

        for index, skin in enumerate(skin_data):
            img = None
            try:
                img = QPixmap(f'skins/{skin['type']}/{skin['name'].replace('/', ':')}.png')
            except Exception as e:
                print(f'Failed to load {skin['name']}.png from path skins/{skin['type']}')

            button = QToolButton()
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setText(skin['name'])

            if img:
                button.setLayout(QVBoxLayout())
                button.setIcon(QIcon(img))
                button.setIconSize(img.size())
                button.setMinimumWidth(int(self.width()*0.5))

            # Calculate the row and column position
            row = index // 2  # Adjust the number of columns as needed
            col = index % 2
            layout.addWidget(button, row, col)

    def download_image_from_url(self, url, name, type):
        try:
            with urllib.request.urlopen(url) as open_url:
                img_data = open_url.read()
                with open(f'skins/{type}/{name}.png', 'wb') as handler:
                        handler.write(img_data)
        except Exception as e:
            print(f"Failed to load image from {url}: {e}")
            return None
