from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from chroma import Chroma

class ItemButton(QToolButton):
    def __init__(self, chroma_data, parent=None):
        super().__init__(parent)

        self.chroma = Chroma(chroma_data)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setText(self.chroma.chroma_name)
        self.setStyleSheet('QToolButton { font-size: 16px; text-align: bottom; } QToolButton::icon { alignment: center; } QToolButton::text { alignment: bottom; } QToolButton::menu-indicator { image: none; } ')
        self.setFixedSize(QSize(400, 200))

        if self.chroma.image:
            resized_img = self.chroma.image.scaled(int(self.width()*0.95), int(self.height()*0.7), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setIcon(QIcon(resized_img))
            self.setIconSize(self.size())
