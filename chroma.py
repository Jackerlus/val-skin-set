import os.path
from pathlib import Path
import urllib.request
from PIL import Image
import pillow_avif
from PySide6.QtGui import QPixmap

class Chroma:
    def __init__(self, chroma_data):
        self.skin_name = chroma_data['skin-name']
        self.chroma_name = chroma_data['chroma-name']
        self.sanitised_skin_name = self.skin_name.replace('/', '_').replace('Ø', 'O')
        self.sanitised_chroma_name = self.chroma_name.replace('/', '_').replace('\r', '').replace('\n', ' ').replace('Ø', 'O')
        self.skin_uuid = chroma_data['skin-uuid']
        self.chroma_uuid = chroma_data['chroma-uuid']
        self.image_url = chroma_data['image-url']
        self.type = chroma_data['type']

        self.load_image()

    def load_image(self):
        self.image = None
        dir = f'skins/{self.type}/{self.sanitised_skin_name}'
        Path(dir).mkdir(parents=True, exist_ok=True)
        file = f'{self.sanitised_chroma_name}.avif'
        path = os.path.join(dir, file)
        if os.path.isfile(path):
            self.image = QPixmap(path)
        else:
            # Local image copy probably doesn't exist, get from URL
            print(f'Failed to load {self.sanitised_chroma_name}.png from directory {dir}')
            print(f'Downloading from {self.image_url}...')
            self.download_image_from_url(dir, self.sanitised_chroma_name)
            # Attempt image load with newly downloaded image
            self.image = QPixmap(path)

    def download_image_from_url(self, dir, name):
        png_path = os.path.join(dir, name + '.png')
        avif_path = os.path.join(dir, name + '.avif')
        try:
            with urllib.request.urlopen(self.image_url) as open_url:
                img_data = open_url.read()
                # Download original .png file
                with open(png_path, 'wb') as handler:
                    handler.write(img_data)
                # Convert .png file to .jpg
                print(f'Converting {name} image to .avif...')
                original_img = Image.open(png_path)
                original_img.save(avif_path, 'AVIF')
                print(f'Deleting original .png...')
                print('-'*40)
                os.remove(png_path)

        except Exception as e:
            print(f"Failed to load image from {self.image_url}: {e}")
            return None
