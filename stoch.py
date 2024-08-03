import numpy as np
import ta
import json
import pandas as pd
import ta.momentum
import ta.trend

import yfinance as yf

import matplotlib.pyplot as plt

# with open("stockData.json") as f:
#     data = json.load(f)

# df = pd.DataFrame(data["data"])

# df["date"] = pd.to_datetime(df["date"])
# df["1. open"] = pd.to_numeric(df["1. open"])
# df["2. high"] = pd.to_numeric(df["2. high"])
# df["3. low"] = pd.to_numeric(df["3. low"])
# df["4. close"] = pd.to_numeric(df["4. close"])
# df["5. volume"] = pd.to_numeric(df["5. volume"])


# df["%K"] = ta.momentum.stoch(
#     df["2. high"], df["3. low"], df["4. close"], window=14, smooth_window=3
# )


interval = "1h"
# interval = "30m"


df = yf.download("BTC-USD", start="2022-09-01", interval=interval)

close_key = "Close"

df["%K"] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)

df["%D"] = df["%K"].rolling(3).mean()

df["rsi"] = ta.momentum.rsi(df.Close, window=14)


df["macd"] = ta.trend.macd_diff(df.Close)

df.dropna(inplace=True)


def get_triggers(df, lags, buy=True):
    dfx = pd.DataFrame()

    for i in range(1, lags + 1):
        if buy:
            mask = (df["%K"].shift(i) < 20) & (df["%D"].shift(i) < 20)
        else:
            mask = (df["%K"].shift(i) > 80) & (df["%D"].shift(i) > 80)
        # dfx = dfx._append(mask, ignore_index=True)  # type: ignore
        # dfx = pd.concat([dfx, mask], ignore_index=True)
        dfxn = pd.DataFrame([mask])

        dfx = pd.concat([dfx, dfxn])

    return dfx.sum(axis=0)


# 4 can be 6
df["Buytrigger"] = np.where(get_triggers(df, 4), 1, 0)

df["Selltrigger"] = np.where(get_triggers(df, 4, False), 1, 0)

df["Buy"] = np.where(
    (df.Buytrigger)
    & (df["%K"].between(20, 80))
    & (df["%D"].between(20, 80))
    & (df.rsi > 50)
    & (df.macd > 0),
    1,
    0,
)


df["Sell"] = np.where(
    (df.Selltrigger)
    & (df["%K"].between(20, 80))
    & (df["%D"].between(20, 80))
    & (df.rsi < 50)
    & (df.macd < 0),
    1,
    0,
)


Buying_dates, Selling_dates = [], []

for i in range(len(df) - 1):
    if df.Buy.iloc[i]:
        Buying_dates.append(df.iloc[i + 1].name)

        for num, j in enumerate(df.Sell[i:]):
            if j:
                Selling_dates.append(df.iloc[i + num + 1].name)
                break


cutit = len(Buying_dates) - len(Selling_dates)


if cutit:
    Buying_dates = Buying_dates[:-cutit]

frame = pd.DataFrame({"Buying_dates": Buying_dates, "Selling_dates": Selling_dates})


actuals = frame[frame.Buying_dates > frame.Selling_dates.shift(1)]


def profitcalc():
    Buyprices = df.loc[actuals.Buying_dates].Open
    Sellprices = df.loc[actuals.Selling_dates].Open

    return (Sellprices.values - Buyprices.values) / Buyprices.values


profits = profitcalc()

print(profits.mean())
print((profits + 1).prod())

plt.figure(figsize=(20, 10))
plt.plot(df.Close, color="k", alpha=0.7)
plt.scatter(actuals.Buying_dates, df.Open[actuals.Buying_dates], color="g", s=500)
plt.scatter(
    actuals.Selling_dates,
    df.Open[actuals.Selling_dates],
    color="r",
    s=500,
)

plt.show()
