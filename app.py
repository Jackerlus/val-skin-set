import sys
import requests
import json
from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import (QApplication, QGridLayout, QSplitter, QWidget, QLabel,
                                QVBoxLayout, QHBoxLayout, QTextEdit, QListView,
                                QGridLayout)
from SkinGrid import SkinGrid

class SkinSetter(QWidget):
    def __init__(self, screen_size, width, height):
        super().__init__()

        self.app_width = width
        self.app_height = height

        # Get all skin data
        self.all_skins = self.get_all_skins()
        print(json.dumps(self.all_skins, indent=4))

        # Create parent window layout
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.setWindowTitle('Skin Setter')

        # Create category list menu widget
        categories_list = QListView()
        list_items = ["Vandal", "Phantom", "Guardian"]
        model = QStringListModel()
        model.setStringList(list_items)
        categories_list.setModel(model)

        # Create left menu layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(categories_list)

        # Create categories menu
        left_categories_menu = QWidget()
        left_categories_menu.setLayout(left_layout)
        left_categories_menu.setMaximumWidth(int(screen_size.width() * 0.25))

        # Create skin grid view widget
        skin_grid = SkinGrid(self.all_skins['HMG'])

        # Create right main view layout
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(skin_grid)

        # Create equippable select main view
        right_main_view = QWidget()
        right_main_view.setLayout(right_layout)
        right_main_view.setMaximumWidth(int(screen_size.width() * 0.75))

        # Create the main widget area with QSplitter
        main_area = QSplitter(orientation=Qt.Horizontal)
        layout.addWidget(main_area)
        main_area.addWidget(left_categories_menu)
        main_area.addWidget(right_main_view)
        main_area.setStretchFactor(0, 1)  # Set the stretch factor for left side
        main_area.setStretchFactor(1, 3)  # Set the stretch factor for right side

    def get_current_loadout(self):
        return

    def get_all_skins(self):
        # Request VALORANT weapon skins from API
        response = requests.get("https://valorant-api.com/v1/weapons/skins")
        output = response.content
        data = json.loads(output)['data']

        # Reorganise data to cut out unnecessary attributes
        skins = {}
        for item in data:
            asset_path = item['assetPath'].split('/')
            if asset_path[3] == 'Guns':
                type = asset_path[5] # Gun type name, e.g. Ares
            else:
                type = 'Melee'
            formattedItem = {}
            formattedItem['name'] = item['displayName']
            formattedItem['uuid'] = item['uuid']
            formattedItem['image'] = item['displayIcon']

            if type not in skins:
                skins[type] = []

            # Add skin to new reformatted weapon skins object
            skins[type].append(formattedItem)

        return skins

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    screen_size = screen.size()

    width = 1200
    height = 800

    widget = SkinSetter(screen_size, width, height)
    widget.resize(width, height)
    widget.show()

    sys.exit(app.exec())
