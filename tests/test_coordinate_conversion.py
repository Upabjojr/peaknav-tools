from peaknav_tools.utils.coordinates import Coordinate, Tile, CoordinateRectangle


def test_coordinate_conv():
    coord = Coordinate(0.0, 0.0)
    tile = Tile(512, 512, 10)
    assert coord.get_containing_tile(10) == tile
    assert tile.get_north_west_corner_coords() == coord
    val = 0.3515602939922723
    # assert tile.get_bounding_box() == CoordinateRectangle(-val, 0.0, 0.0, val)
