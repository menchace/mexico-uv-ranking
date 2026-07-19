from pathlib import Path

from src.cities import load_cities
from src.temis import open_dataset
from src.analysis import analyze_year

# ----------------------------
# Configuration
# ----------------------------

YEAR = 2024

CITIES = "processed/base_maestra_ciudades_uv_mexico.csv"

OUTPUT = Path("outputs/tables")
OUTPUT.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Load cities
# ----------------------------

cities = load_cities(CITIES)

print(f"{len(cities)} cities loaded")

# ----------------------------
# Open TEMIS
# ----------------------------

ds = open_dataset(YEAR)

print("Dataset opened")

# ----------------------------
# Run analysis
# ----------------------------

results = analyze_year(
    ds,
    cities,
    YEAR
)

results.to_csv(
    OUTPUT / f"uv_{YEAR}.csv",
    index=False
)

print(results.head())

print("\nDone!")