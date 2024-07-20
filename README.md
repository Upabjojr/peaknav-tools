# PeakNav tools

Tools for elevation data, originally created for the [PeakNav](https://peaknav.com) app.

Example usage, get the estimated elevation of Mount Mitchell, North Carolina, in meters:
```python
from peaknav_tools import get_elevation_from_coordinates
get_elevation_from_coordinates(35.7649563, -82.2651155)
```
Currently, this returns an elevation of 2024 meters for this coordinate (the actual elevation of Mount Mitchell is 2038 meters).
The elevation error typically ranges between 10-20 meters.

This library uses the dataset [elevation-data-ASTER-compressed-retiled](https://huggingface.co/datasets/Upabjojr/elevation-data-ASTER-compressed-retiled)
hosted on huggingface. This dataset is a retiled and compressed version of [ASTER GDEM](https://asterweb.jpl.nasa.gov/GDEM.asp).

Each elevation query requires the relevant elevation tile from this dataset, which is downloaded and cached.
The dataset can also be downloaded and cached for offline usage using the `huggingface_hub` library.
