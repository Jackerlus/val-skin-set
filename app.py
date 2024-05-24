import random
import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QSplitter, QWidget, QLabel, QPushButton, QVBoxLayout,
                                QSplitter)

class SkinSetter(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.setWindowTitle('Skin Setter')

        main_window = QSplitter(orientation=Qt.Horizontal)
        layout.addWidget(main_window)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = SkinSetter()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
