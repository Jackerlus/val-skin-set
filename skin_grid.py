from PySide6.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QPushButton, QToolButton
from PySide6.QtCore import QSize, Qt
from item_button import ItemButton

class SkinGrid(QWidget):
    def __init__(self, skin_data, loadout=False, parent=None):
        super().__init__(parent)

        self.skin_data = skin_data
        self.loadout = loadout

        layout = QGridLayout()
        self.setLayout(layout)
        self.all_buttons = []

        index = 0
        for chroma in self.skin_data:
            button = None
            if self.loadout is True:
                self.skin_data[chroma]['type'] = chroma
                button = ItemButton(self.skin_data[chroma])
            else:
                button = ItemButton(chroma)
            self.all_buttons.append(button)
            # Calculate the row and column position
            row = index // 2  # Adjust the number of columns as needed
            col = index % 2
            layout.addWidget(button, row, col)
            index += 1
