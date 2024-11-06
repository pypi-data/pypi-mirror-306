from .base_converter import BaseConverter
from ..transformers.default_image_transformer import DefaultImageTransformer

class DefaultConverter(BaseConverter):
    def __init__(self):
        super().__init__()

    def convert_html_to_json_blocks(self, soup, images_info):
        """Convierte el HTML a bloques JSON utilizando el transformador de imágenes predeterminado."""
        default_image_transformer = DefaultImageTransformer()
        return super().convert_html_to_json_blocks(soup, images_info, default_image_transformer)
