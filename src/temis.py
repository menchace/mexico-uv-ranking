"""
Utilities for downloading and opening TEMIS datasets.
"""

from pathlib import Path
import requests
import xarray as xr

BASE_URL = (
    "https://d1qb6yzwaaq4he.cloudfront.net/"
    "uvradiation/v2.0/msr2/nc"
)


def download_year(year: int, folder: str = "data/raw") -> Path:
    """
    Download one TEMIS yearly file if it does not exist.
    """

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"uvief{year}_msr_world.nc"
    output = folder / filename

    if output.exists():
        return output

    url = f"{BASE_URL}/{year}/{filename}"

    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()

        with open(output, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output


def open_dataset(year: int, folder: str = "data/raw"):
    """
    Open TEMIS PRODUCT group.
    """

    path = download_year(year, folder)

    return xr.open_dataset(
        path,
        group="PRODUCT",
        engine="h5netcdf"
    )