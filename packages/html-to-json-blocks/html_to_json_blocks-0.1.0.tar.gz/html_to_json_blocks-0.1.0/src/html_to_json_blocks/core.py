from .converters.base_converter import BaseConverter
from .transformers.image_transformer import ImageTransformer

class HtmlToJsonConverter:
    def __init__(self, image_transformer: ImageTransformer):
        self.image_transformer = image_transformer
        self.converter = BaseConverter()

    def convert(self, soup, images_info):
        return self.converter.convert_html_to_json_blocks(soup, images_info, self.image_transformer)
