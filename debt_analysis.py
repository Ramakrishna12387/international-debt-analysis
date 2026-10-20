
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("cleaned_international_debt.csv")

# Average debt per capita by country
avg_debt = (
    df.groupby("country_name")["debt"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# Create bar chart
plt.figure(figsize=(12, 6))
avg_debt.sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Average External Debt Per Capita")
plt.xlabel("Average External Debt Per Capita (US$)")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig("top_10_debt_countries.png", dpi=300)
plt.show()

print("Chart saved as top_10_debt_countries.png")
print(avg_debt.round(2))
