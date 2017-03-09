import numpy as np
from PIL import Image
from skimage import color
from skimage.feature import hog

from pelops.features.feature_producer import FeatureProducer


class HOGFeatureProducer(FeatureProducer):

    def __init__(self, chip_producer, image_size=(256,256), cells=(16, 16), orientations=8):
        self.image_size = image_size
        self.cells = cells
        self.orientations = orientations
        super().__init__(chip_producer)

    def produce_features(self, chip):
        """Takes a chip object and returns a feature vector of size
        self.feat_size. """
        img = self.get_image(chip)
        img = img.resize(self.image_size, Image.BICUBIC)
        img_x, img_y = img.size
        img = color.rgb2gray(np.array(img))
        features = hog(
            img,
            orientations=self.orientations,
            pixels_per_cell=(img_x / self.cells[0], img_y / self.cells[1]),
            cells_per_block=self.cells,  # Normalize over the whole image
        )
        return features

    def set_variables(self):
        self.feat_size = self.cells[0] * self.cells[1] * self.orientations