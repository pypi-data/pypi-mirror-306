from datetime import datetime
from .image_transformer import ImageTransformer

class DefaultImageTransformer(ImageTransformer):
    def transform_image(self, img_node, images_info):
        """Transforma un nodo de imagen HTML en un bloque JSON de imagen."""
        src = img_node.get('src', '')
        image_info = next((img for img in images_info if img['src'] == src), None)

        if image_info:
            # Si se proporciona información de la imagen, utiliza esa información
            return {
                "type": "image",
                "image": {
                    "ext": image_info.get('ext', ''),
                    "url": image_info.get('url', src),
                    "hash": image_info.get('hash', ''),
                    "mime": image_info.get('mime', ''),
                    "name": image_info.get('name', ''),
                    "size": image_info.get('size', 0),
                    "width": image_info.get('width', 0),
                    "height": image_info.get('height', 0),
                    "caption": img_node.get('alt', ''),
                    "formats": image_info.get('formats', {}),
                    "provider": image_info.get('provider', 'local'),
                    "createdAt": image_info.get('createdAt', datetime.now().isoformat()),
                    "updatedAt": image_info.get('updatedAt', datetime.now().isoformat()),
                    "previewUrl": None,
                    "alternativeText": img_node.get('alt', ''),
                    "provider_metadata": None
                },
                "children": [{"text": "", "type": "text"}]
            }
        else:
            # Fallback si no se encuentra la información de la imagen
            return {
                "type": "image",
                "image": {
                    "ext": src.split('.')[-1] if '.' in src else '',
                    "url": src,
                    "hash": src.split('/')[-1].split('.')[0] if '/' in src else '',
                    "mime": f"image/{src.split('.')[-1]}" if '.' in src else '',
                    "name": src.split('/')[-1] if '/' in src else '',
                    "size": 0,
                    "width": img_node.get('width'),
                    "height": img_node.get('height'),
                    "caption": img_node.get('alt', ''),
                    "formats": {},
                    "provider": "local",
                    "createdAt": datetime.now().isoformat(),
                    "updatedAt": datetime.now().isoformat(),
                    "previewUrl": None,
                    "alternativeText": img_node.get('alt', ''),
                    "provider_metadata": None
                },
                "children": [{"text": "", "type": "text"}]
            }
