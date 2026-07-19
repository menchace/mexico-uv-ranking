from src.cities import load_cities
from src.temis import open_dataset
from src.analysis import analyze_year

CITIES_PATH = "processed/base_maestra_ciudades_uv_mexico.csv"

cities = load_cities(CITIES_PATH)

print(f"Ciudades cargadas: {len(cities)}")
print(cities.head())