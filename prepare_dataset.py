
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "COUNTRIES.xlsx" / "ALL COUNTRIES.xlsx"
OUTPUT_FILE = BASE_DIR / "international_debt.csv"

print("1. Reading Excel dataset...")

df = pd.read_excel(EXCEL_FILE, sheet_name="Data")

print("Original rows:", len(df))

# Keep country and indicator details
id_columns = [
    "Country Name",
    "Country Code",
    "Series Name",
    "Series Code",
]

# Identify year columns
year_columns = [
    col for col in df.columns
    if str(col).isdigit()
]

print("Year columns found:", len(year_columns))

# Convert wide format into long format
long_df = df.melt(
    id_vars=id_columns,
    value_vars=year_columns,
    var_name="year",
    value_name="debt",
)

# Rename columns to match the project pipeline
long_df = long_df.rename(columns={
    "Country Name": "country_name",
    "Country Code": "country_code",
    "Series Name": "indicator_name",
    "Series Code": "indicator_code",
})

# Clean text columns
for col in [
    "country_name",
    "country_code",
    "indicator_name",
    "indicator_code",
]:
    long_df[col] = long_df[col].astype("string").str.strip()

# Convert values to numbers and remove missing values
long_df["debt"] = pd.to_numeric(
    long_df["debt"], errors="coerce"
)

long_df = long_df.dropna(
    subset=[
        "country_name",
        "country_code",
        "indicator_name",
        "indicator_code",
        "debt",
    ]
)

long_df = long_df.drop_duplicates()

# Save the converted data
long_df.to_csv(OUTPUT_FILE, index=False)

print("2. Dataset converted successfully.")
print("Output file:", OUTPUT_FILE.name)
print("Records saved:", len(long_df))
print(long_df.head())
