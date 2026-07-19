"""
Analysis functions for the Mexico UV Atlas.
"""

import numpy as np
import pandas as pd


def analyze_city(dataset, city):
    """
    Analyze one city for one year.
    """

    serie = dataset["uvi_clear"].sel(
        latitude=city["lat"],
        longitude=city["lon"],
        method="nearest"
    )

    values = np.asarray(serie.values, dtype=float)
    values = values[~np.isnan(values)]

    return {
        "ciudad": city["ciudad"],
        "estado": city["estado"],
        "poblacion": city["poblacion"],
        "elevacion_m": city["elevacion_m"],
        "lat": city["lat"],
        "lon": city["lon"],
        "lat_pixel": float(serie.latitude.values),
        "lon_pixel": float(serie.longitude.values),
        "dias_uvi_3": int(np.sum(values >= 3)),
        "dias_uvi_6": int(np.sum(values >= 6)),
        "dias_uvi_8": int(np.sum(values >= 8)),
        "dias_uvi_11": int(np.sum(values >= 11)),
        "uvi_promedio": float(np.mean(values)),
        "uvi_maximo": float(np.max(values)),
        "dias_con_datos": len(values),
    }


def analyze_year(dataset, cities, year):
    """
    Analyze all cities for one year.
    """

    results = []

    for _, city in cities.iterrows():

        row = analyze_city(dataset, city)

        row["anio"] = year

        results.append(row)

    return pd.DataFrame(results)