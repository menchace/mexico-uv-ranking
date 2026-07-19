"""
Analysis functions for the Mexico UV Atlas.
"""

import numpy as np
import pandas as pd


def analyze_city(dataset, city):
    series = dataset["uvi_clear"].sel(
        latitude=city["lat"],
        longitude=city["lon"],
        method="nearest",
    )

    values = np.asarray(series.values, dtype=float)
    values = values[~np.isnan(values)]

    if len(values) == 0:
        raise ValueError(
            f"No hay datos UV válidos para {city['ciudad']}"
        )

    return {
        "ciudad": city["ciudad"],
        "estado": city["estado"],
        "poblacion": int(city["poblacion"]),
        "elevacion_m": float(city["elevacion_m"]),
        "lat": float(city["lat"]),
        "lon": float(city["lon"]),
        "lat_pixel": float(series.latitude.values),
        "lon_pixel": float(series.longitude.values),
        "dias_uvi_3": int(np.sum(values >= 3)),
        "dias_uvi_6": int(np.sum(values >= 6)),
        "dias_uvi_8": int(np.sum(values >= 8)),
        "dias_uvi_11": int(np.sum(values >= 11)),
        "uvi_promedio": round(float(np.mean(values)), 3),
        "uvi_maximo": round(float(np.max(values)), 3),
        "dias_con_datos": int(len(values)),
    }


def analyze_year(dataset, cities, year):
    results = []

    for _, city in cities.iterrows():
        row = analyze_city(dataset, city)
        row["anio"] = int(year)
        results.append(row)

    columns = [
        "anio",
        "ciudad",
        "estado",
        "poblacion",
        "elevacion_m",
        "lat",
        "lon",
        "lat_pixel",
        "lon_pixel",
        "dias_uvi_3",
        "dias_uvi_6",
        "dias_uvi_8",
        "dias_uvi_11",
        "uvi_promedio",
        "uvi_maximo",
        "dias_con_datos",
    ]

    return pd.DataFrame(results)[columns]