
import pandas as pd
import mysql.connector

# CSV file
df = pd.read_csv("cleaned_international_debt.csv")

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="international_debt_db"
)

cursor = conn.cursor()

try:
    # Insert countries
    countries = df[["country_code", "country_name"]].drop_duplicates()

    cursor.executemany(
        """
        INSERT IGNORE INTO countries (country_code, country_name)
        VALUES (%s, %s)
        """,
        list(countries.itertuples(index=False, name=None))
    )

    # Insert indicators
    indicators = df[["indicator_code", "indicator_name"]].drop_duplicates()

    cursor.executemany(
        """
        INSERT IGNORE INTO indicators (indicator_code, indicator_name)
        VALUES (%s, %s)
        """,
        list(indicators.itertuples(index=False, name=None))
    )

    # Insert debt data
    records = list(
        df[["country_code", "indicator_code", "year", "debt"]]
        .itertuples(index=False, name=None)
    )

    cursor.executemany(
        """
        INSERT IGNORE INTO debt_data
        (country_code, indicator_code, year, debt)
        VALUES (%s, %s, %s, %s)
        """,
        records
    )

    conn.commit()
    print("Data loaded successfully!")
    print("Countries:", len(countries))
    print("Indicators:", len(indicators))
    print("Debt records:", len(records))

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    cursor.close()
    conn.close()
