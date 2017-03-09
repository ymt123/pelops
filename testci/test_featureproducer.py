import collections
import datetime
import pytest
import numpy as np
from PIL import Image

#from pelops.datasets.chip import ChipDataset, Chip
from pelops.datasets.featuredataset import FeatureDataset
from pelops.features.feature_producer import FeatureProducer


@pytest.fixture
def chip_producer():
    Chip = collections.namedtuple("Chip", ["filepath", "car_id", "cam_id", "time", "img_data", "misc"])
    DATA = [[[  0,   0,   0],
             [255, 255, 255],
             [  0,   0,   0]],
            [[255, 255, 255],
             [  0,   0,   0],
             [255, 255, 255]],
            [[  0,   0,   0],
             [255, 255, 255],
             [  0,   0,   0]]]
    CHIPS = (
        # filepath, car_id, cam_id, time, img_data, misc
        ("car1_cam1.png", 1, 1, datetime.datetime(2016, 10, 1, 0, 1, 2, microsecond=100), np.array(DATA, dtype=np.uint8), {}),
    )

    chip_producer = {"chips": {}}
    for filepath, car_id, cam_id, time, img_data, misc in CHIPS:
        print(img_data.shape)
        chip = Chip(filepath, car_id, cam_id, time, img_data, misc)
        chip_producer["chips"][filepath] = chip

    return chip_producer

@pytest.fixture
def monkey_feature_producer(chip_producer):
    # Monkey patch the __init__() function so that it will succeed
    def new_init(self, chip_producer):
        self.chip_producer = chip_producer

    FeatureProducer.__init__ = new_init

    return (FeatureProducer(chip_producer))


def test_set_variables_raises():
    with pytest.raises(NotImplementedError):
        fp = FeatureProducer(None)


def test_produce_features_raises(monkey_feature_producer):
    with pytest.raises(NotImplementedError):
        monkey_feature_producer.produce_features(None)


def test_get_image_img_data(monkey_feature_producer, chip_producer):
    for key, chip in chip_producer["chips"].items():
        assert monkey_feature_producer.get_image(chip)

