from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "ciudad",
    "estado",
    "poblacion",
    "lat",
    "lon",
    "elevacion_m",
}


def load_cities(path) -> pd.DataFrame:
    """Carga y valida la base maestra de ciudades."""
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de ciudades: {csv_path}"
        )

    cities = pd.read_csv(csv_path)

    missing = REQUIRED_COLUMNS.difference(cities.columns)
    if missing:
        raise ValueError(
            "Faltan columnas obligatorias: "
            + ", ".join(sorted(missing))
        )

    cities = cities.copy()
    cities["poblacion"] = pd.to_numeric(
        cities["poblacion"], errors="raise"
    ).astype(int)

    for column in ["lat", "lon", "elevacion_m"]:
        cities[column] = pd.to_numeric(
            cities[column], errors="raise"
        )

    if cities["ciudad"].duplicated().any():
        duplicates = cities.loc[
            cities["ciudad"].duplicated(), "ciudad"
        ].tolist()
        raise ValueError(
            f"Hay ciudades duplicadas: {duplicates}"
        )

    return cities.sort_values(
        "poblacion", ascending=False
    ).reset_index(drop=True)