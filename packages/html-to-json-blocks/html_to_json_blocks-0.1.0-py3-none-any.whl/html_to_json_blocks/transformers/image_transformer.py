from abc import ABC, abstractmethod

class ImageTransformer(ABC):
    @abstractmethod
    def transform_image(self, img_node, images_info):
        pass
