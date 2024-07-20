import pytest

from peaknav_tools.utils.elevation import get_elevation_from_coordinates


@pytest.mark.parametrize(
    ["lat", "lon", "expected", "real", "name"],
    [
        (37.74600,-119.53278, 2612, 2694, "Half Dome, Yosemite"),
        (37.7481814, -119.5868869, 1228, 1218, "Yosemite Village"),
        (36.6065528, -117.1468690, 0, 3, "Stovepipe Wells, Death Valley"),
        (36.23025, -116.76747, -80, -85, "Badwater Basin, Death Valley"),
        (46.8521484, -121.7576820, 4336, 4392, "Mount Rainier"),
        (63.0691150, -151.0062390, 6172, 6190, "Mount Denali"),
        (31.5841, 35.4858, -428, -427, "Dead Sea"),
    ]
)
def test_load_elevation(lat, lon, expected, real, name):
    assert get_elevation_from_coordinates(lat, lon) == expected, f"Wrong expected elevation for {name}"
