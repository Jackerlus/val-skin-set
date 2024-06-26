import sys
import requests
import json
from PySide6.QtCore import QStringListModel, Qt
from PySide6.QtWidgets import (QApplication, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QListView, QSplitter, QStyledItemDelegate)
from skin_grid import SkinGrid
from loadout import Loadout

class NonEditableStringListModel(QStringListModel):
    def flags(self, index):
        # Set the item flags to make them non-editable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

class SkinSetter(QWidget):
    def __init__(self, screen_size):
        super().__init__()

        # Initialise working loadout
        self.loadout = Loadout()
        print(f'Initialised loadout {self.loadout.name}')

        # Get all skin data
        self.all_skins = self.get_all_skins()

        # Create parent window layout
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.setWindowTitle('SkinSet')

        # Create category list menu widget
        self.categories_list = QListView()
        self.list_items = [
            'Loadout',
            'Classic', 'Shorty', 'Frenzy', 'Ghost', 'Sheriff',
            'Stinger', 'Spectre',
            'Bucky', 'Judge',
            'Bulldog', 'Guardian', 'Phantom', 'Vandal',
            'Marshal', 'Outlaw', 'Operator',
            'Ares', 'Odin',
            'Melee'
        ]
        self.menu_model = NonEditableStringListModel(self.list_items)
        self.categories_list.setItemDelegate(QStyledItemDelegate(None))
        #self.menu_model.setStringList(self.list_items)
        self.categories_list.setModel(self.menu_model)
        self.categories_list.clicked.connect(self.list_item_clicked)

        # Create left menu layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.categories_list)

        # Create categories menu
        left_categories_menu = QWidget()
        left_categories_menu.setLayout(left_layout)

        # Create skin grid view widget
        skin_grid = SkinGrid(self.loadout.skins, loadout=True) # Shows the loadout view by default
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setEnabled(False)
        self.scroll_area.horizontalScrollBar().setHidden(True)
        self.scroll_area.setWidget(skin_grid)

        # Create right main view layout
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.scroll_area)

        # Create equippable select main view
        right_main_view = QWidget()
        right_main_view.setLayout(right_layout)

        # Create the main widget area with QSplitter
        main_area = QSplitter(orientation=Qt.Horizontal)
        layout.addWidget(main_area)
        main_area.addWidget(left_categories_menu)
        main_area.addWidget(right_main_view)
        main_area.setStretchFactor(1, 3) # Set left:right space ratio

    def list_item_clicked(self, index):
        item_text = self.categories_list.model().data(index, Qt.DisplayRole)
        print(f'Selected item: {item_text}')

        # Convert list text to internal weapon code
        type = ''
        match item_text:
            case 'Loadout':
                type = 'Loadout'
            case 'Classic':
                type = 'BasePistol'
            case 'Shorty':
                type = 'Slim'
            case 'Frenzy':
                type = 'AutoPistol'
            case 'Ghost':
                type = 'Luger'
            case 'Sheriff':
                type = 'Revolver'
            case 'Stinger':
                type = 'Vector'
            case 'Spectre':
                type = 'MP5'
            case 'Bucky':
                type = 'PumpShotgun'
            case 'Judge':
                type = 'AutoShotgun'
            case 'Bulldog':
                type = 'Burst'
            case 'Guardian':
                type = 'DMR'
            case 'Phantom':
                type = 'Carbine'
            case 'Vandal':
                type = 'AK'
            case 'Marshal':
                type = 'Leversniper'
            case 'Outlaw':
                type = 'Doublesniper'
            case 'Operator':
                type = 'Boltsniper'
            case 'Ares':
                type = 'LMG'
            case 'Odin':
                type = 'HMG'
            case 'Melee':
                type = 'Melee'

        if type == 'Loadout':
            self.scroll_area.setWidget(SkinGrid(self.loadout.skins, loadout=True))
        else:
            self.scroll_area.setWidget(SkinGrid(self.all_skins[type]))

    def get_all_skins(self):
        # Request VALORANT weapon skins from API
        response = requests.get('https://valorant-api.com/v1/weapons/skins')
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

            for chroma in item['chromas']:
                formatted_chroma = {}

                if item['displayName'][-1] == ' ':
                    formatted_chroma['skin-name'] =  item['displayName'][:-1]
                else:
                    formatted_chroma['skin-name'] =  item['displayName']
                if chroma['displayName'][-1] == ' ':
                    formatted_chroma['chroma-name'] = chroma['displayName'][:-1]
                else:
                    formatted_chroma['chroma-name'] = chroma['displayName']

                formatted_chroma['skin-uuid'] = item['uuid']
                formatted_chroma['chroma-uuid'] = chroma['uuid']
                formatted_chroma['image-url'] = chroma['fullRender']
                formatted_chroma['type'] = type

                if type not in skins:
                    skins[type] = []

                # Add chroma to new reformatted weapon skins object
                skins[type].append(formatted_chroma)

        return skins

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    screen_size = screen.size()

    width = 1200
    height = 800

    widget = SkinSetter(screen_size)
    widget.resize(width, height)
    widget.show()

    sys.exit(app.exec())
