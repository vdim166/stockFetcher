import json
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

with open("stockData.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["data"])

df["date"] = pd.to_datetime(df["date"])
df["1. open"] = pd.to_numeric(df["1. open"])
df["2. high"] = pd.to_numeric(df["2. high"])
df["3. low"] = pd.to_numeric(df["3. low"])
df["4. close"] = pd.to_numeric(df["4. close"])
df["5. volume"] = pd.to_numeric(df["5. volume"])

supportResistanceLevels = data["supportResistanceLevels"]

plt.figure(figsize=(14, 7))

plt.plot(df["date"], df["4. close"], label="Close Price", color="blue")
plt.plot(df["date"], df["1. open"], label="Open Price", color="orange")
plt.fill(
    list(df["date"]) + list(df["date"][::-1]),
    list(df["3. low"]) + list(df["2. high"][::-1]),
    color="gray",
    alpha=0.3,
    label="High-Low Range",
)

for value in supportResistanceLevels:
    plt.axhline(
        y=value,
        color="green",
        linestyle="--",
        label="supportResistanceLevels",
    )

plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Stock Prices with Support and Resistance Lines")
plt.legend()
plt.grid(True)

plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

plt.xticks(rotation=45)
plt.tight_layout()

# plt.savefig("stock_prices_with_full_lines.png")
plt.show()
