import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Tile:
    """
    Slippy map tile
    """
    x: int
    y: int
    zoom: int

    def get_north_west_corner_coords(self) -> 'Coordinate':
        """
        Given a slippy map tile, return latitude and longitude of its north-western corner.

        Taken from openstreetmap wiki.
        """
        n = 2.0 ** self.zoom
        lon_deg = self.x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * self.y / n)))
        lat_deg = math.degrees(lat_rad)
        return Coordinate(lat_deg, lon_deg)

    def get_bounding_box(self) -> 'CoordinateRectangle':
        """
        Given a slippy map tile (x, y, zoom level), return the coordinates of its bounding box.

        Returns a CoordinateRectangle object.
        """
        lat_deg_nw, lon_deg_nw = self.get_north_west_corner_coords().get_lat_lon()
        lat_deg_se, lon_deg_se = Tile(self.x + 1, self.y + 1, self.zoom).get_north_west_corner_coords().get_lat_lon()
        return CoordinateRectangle(lat_deg_se, lon_deg_nw, lat_deg_nw, lon_deg_se)


@dataclass
class Coordinate:
    """
    A coordinate point, identified by latitude and longitude.
    """

    lat: float
    lon: float


    def get_containing_tile(self, zoom: int) -> Tile:
        """
        Given coordinates (latitude and longitude), return the slippy map tile for the given zoom level.

        Taken from openstreetmap wiki.
        """
        lat_rad = math.radians(self.lat)
        n = 2.0 ** zoom
        xtile = int((self.lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return Tile(xtile, ytile, zoom)

    def get_lat_lon(self) -> Tuple[float, float]:
        """
        Returns a tuple containing the latitude and longitude values of the coordinates.
        """
        return self.lat, self.lon


@dataclass
class CoordinateRectangle:
    """
    Rectangle of coordinates.
    """

    minlat: float
    minlon: float
    maxlat: float
    maxlon: float
