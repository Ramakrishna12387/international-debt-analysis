import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Database Connection Settings (ungaloda MySQL credentials mathikonga)
DB_USER = "root"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "international_debt_db"

def run_pipeline():
    print("1. Loading raw dataset...")
    # Dataset column names World Bank format padi:
    # country_name, country_code, indicator_name, indicator_code, debt
    df = pd.read_csv("international_debt.csv")
    print(f"Raw record count: {len(df)}")

    print("2. Cleaning & preprocessing data...")
    # Column names standardize panradhu
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Duplicates handling
    df = df.drop_duplicates()

    # Missing values handling
    df = df.dropna(subset=['debt', 'country_name', 'indicator_code', 'country_code'])

    # Data type conversion
    df['debt'] = pd.to_numeric(df['debt'], errors='coerce')
    df = df.dropna(subset=['debt'])

    # Whitespace cleanup
    df['country_name'] = df['country_name'].astype(str).str.strip()
    df['country_code'] = df['country_code'].astype(str).str.strip()
    df['indicator_name'] = df['indicator_name'].astype(str).str.strip()
    df['indicator_code'] = df['indicator_code'].astype(str).str.strip()

    # Save cleaned CSV
    df.to_csv("cleaned_international_debt.csv", index=False)
    print("Cleaned data saved to 'cleaned_international_debt.csv'")

    print("3. Connecting to MySQL and inserting data...")
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    # Countries Dimension
    countries_df = df[['country_code', 'country_name']].drop_duplicates().dropna()
    countries_df.to_sql('countries', con=engine, if_exists='append', index=False)
    print("Inserted countries successfully.")

    # Indicators Dimension
    indicators_df = df[['indicator_code', 'indicator_name']].drop_duplicates().dropna()
    indicators_df.to_sql('indicators', con=engine, if_exists='append', index=False)
    print("Inserted indicators successfully.")

    # Fact Table (Debt Data)
    debt_df = df[['country_code', 'indicator_code', 'debt']]
    debt_df.to_sql('debt_data', con=engine, if_exists='append', index=False, chunksize=1000)
    print("Inserted debt records successfully.")

    print("Pipeline execution completed!")

if __name__ == "__main__":
    run_pipeline()