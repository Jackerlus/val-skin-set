from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtGui import QIcon, QImage, QPixmap
from PIL import Image
import urllib.request

class SkinGrid(QWidget):
    def __init__(self, skin_data, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        self.setLayout(layout)

        for skin in skin_data:
            print(skin)
            img = self.get_image_from_url(skin['image'])
            button = QPushButton(f'{skin['name']}')
            if img:
                button.setIcon(QIcon(img))

    def get_image_from_url(self, url):
        try:
            with urllib.request.urlopen(url) as open_url:
                image = Image.open(open_url)

                # Convert PIL image to QImage
                image = image.convert("RGBA")
                data = image.tobytes("raw", "RGBA")
                qimage = QImage(data, image.width, image.height, QImage.Format_RGBA8888)

                # Convert QImage to QPixmap
                pixmap = QPixmap.fromImage(qimage)
                return pixmap
        except Exception as e:
            print(f"Failed to load image from {url}: {e}")
            return None
