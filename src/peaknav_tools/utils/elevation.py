import math
import os
import posixpath
from dataclasses import dataclass, astuple
from functools import reduce
from typing import Dict

from PIL import Image
import numpy as np
import numpy

from peaknav_tools.utils.coordinates import Tile, Coordinate

REPO_ID = "Upabjojr/elevation-data-ASTER-compressed-retiled"


@dataclass
class ElevationTile:
    tile: Tile
    f: int

    def load(self, path=None):
        self_tuple = astuple(self)
        if self_tuple in _elevation_array_instances:
            return _elevation_array_instances[self_tuple]

        subpath = posixpath.join(
            f"elev_tiles/",
            f"x{self.tile.x:05}",
            f"y{self.tile.y:05}",
            f"elev.z{self.tile.zoom:02}.x{self.tile.x:05}.y{self.tile.y:05}.f{self.f:03}",
        )
        subpath_jpg = f"{subpath}.jpg"
        subpath_png = f"{subpath}.png"
        if path is None:
            from huggingface_hub import hf_hub_download
            filepath_jpg = hf_hub_download(
                repo_id=REPO_ID,
                filename=subpath_jpg,
                repo_type="dataset",
            )
            filepath_png = hf_hub_download(
                repo_id=REPO_ID,
                filename=subpath_png,
                repo_type="dataset",
            )
        else:
            filepath_jpg = os.path.join(path, subpath_jpg)
            filepath_png = os.path.join(path, subpath_png)
        array_jpg = numpy.array(Image.open(filepath_jpg))
        array_png = numpy.array(Image.open(filepath_png))
        elevation_tile_loaded = ElevationTileLoaded(self, convert_elevation_2img_to_1img(array_jpg, array_png))
        _elevation_array_instances[self_tuple] = elevation_tile_loaded
        return elevation_tile_loaded


@dataclass
class ElevationTileLoaded:
    elevation_tile: ElevationTile
    elevation_array: numpy.ndarray

    def get_elevation_for_coord(self, lat: float, lon: float) -> int:
        """
        Return elevation in meters for coordinates, if they are contained in the tile.
        """
        tile = self.elevation_tile.tile
        bounding_box = tile.get_bounding_box()
        array_size_len = self.elevation_array.shape[0]

        bb_coord_x_len = bounding_box.maxlon - bounding_box.minlon
        bb_coord_y_len = bounding_box.maxlat - bounding_box.minlat

        x_float = (lon - bounding_box.minlon) / bb_coord_x_len * array_size_len
        y_float = (lat - bounding_box.minlat) / bb_coord_y_len * array_size_len
        x_int = math.floor(x_float)
        y_int = math.floor(y_float)

        def get_tile_matrix_elevation_latits(x, y) -> int:
            return int(self.elevation_array[array_size_len - 1 - y, x])

        array_size_len_m1 = array_size_len - 1

        el1 = get_tile_matrix_elevation_latits(x_int, y_int)
        el2 = get_tile_matrix_elevation_latits(x_int + (1 if x_int < array_size_len_m1 else -1), y_int)
        el3 = get_tile_matrix_elevation_latits(x_int, y_int + (1 if y_int < array_size_len_m1 else -1))
        el4 = get_tile_matrix_elevation_latits(x_int + (1 if x_int < array_size_len_m1 else -1), y_int + (1 if y_int < array_size_len_m1 else -1))

        # TODO: maybe average would be better?
        return reduce(max, (el1, el2, el3, el4))


_elevation_array_instances: Dict[tuple, ElevationTileLoaded] = {}


def convert_elevation_1img_to_2img(img):
    """
    Convert elevation array into pair of arrays for JPG/PNG encoding.
    """
    img_jpeg = (img % 1024 / 4).astype(np.uint8)
    img_png = (128 + np.floor(img / 1024)).astype(np.uint8)
    img2f = img_png % 2
    img2bool = (img2f == 1)
    img_jpeg[img2bool] = 255 - img_jpeg[img2bool]
    return img_jpeg, img_png


def convert_elevation_2img_to_1img(img_jpeg: numpy.ndarray, img_png: numpy.ndarray):
    """
    Convert elevation arrays from JPG and PNG images into a single elevation array.
    """
    img2f = img_png % 2
    img2bool = (img2f == 1)
    img = img_jpeg.astype(np.int16)
    img[img2bool] = 255 - img_jpeg[img2bool]
    img += (img_png.astype(np.int16) - 128) * 256
    img *= 4
    return img


def get_elevation_from_coordinates(latitude: float, longitude: float) -> int:
    """
    Return the elevation in meters of the given coordinate (latitude and longitude).

    This function will download the corresponding elevation tile if it has not already been downloaded.
    """
    from ._elevation_tile_index import _elev_tiles
    coord = Coordinate(latitude, longitude)
    tile = coord.get_containing_tile(8)
    if (tile.x, tile.y) not in _elev_tiles:
        return 0
    elev_tile = ElevationTile(tile, 0)
    elev_tile_loaded = elev_tile.load()
    return elev_tile_loaded.get_elevation_for_coord(latitude, longitude)
