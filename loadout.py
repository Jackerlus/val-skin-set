import json
class Loadout:
    def __init__(self, load='default'):
        with open(f'loadouts/{load}.json') as loadout_file:
            data = json.load(loadout_file)
        self.name = data['loadout-name']
        self.skins = data['skins']
