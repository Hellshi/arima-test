import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima


data = pd.read_csv("data.csv", delimiter=";", na_values=["", " "], dtype={"Hora (UTC)": str})
data["Temp. Ins. (C)"] = data["Temp. Ins. (C)"].astype(str).str.replace(",", ".")
data["Vel. Vento (m/s)"] = data["Vel. Vento (m/s)"].astype(str).str.replace(",", ".")
data["Dir. Vento (m/s)"] = data["Dir. Vento (m/s)"].astype(str).str.replace(",", ".")
data["Raj. Vento (m/s)"] = data["Raj. Vento (m/s)"].astype(str).str.replace(",", ".")
data["Radiacao (KJ/m²)"] = data["Radiacao (KJ/m²)"].astype(str).str.replace(",", ".")


numerical_columns = [
    "Temp. Ins. (C)", "Temp. Max. (C)", "Temp. Min. (C)",
    "Umi. Ins. (%)", "Umi. Max. (%)", "Umi. Min. (%)",
    "Pto Orvalho Ins. (C)", "Pto Orvalho Max. (C)", "Pto Orvalho Min. (C)",
    "Pressao Ins. (hPa)", "Pressao Max. (hPa)", "Pressao Min. (hPa)",
    "Vel. Vento (m/s)", "Dir. Vento (m/s)", "Raj. Vento (m/s)", "Radiacao (KJ/m²)", "Chuva (mm)"
]

print(data.head(50))

data["Hora (UTC)"] = data["Hora (UTC)"].apply(lambda x: f"{x[:2]}:{x[2:]}")


for col in numerical_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")

    if data[col].empty:
        data[col] = None

data["datetime"] = pd.to_datetime(data["Data"] + " " + data["Hora (UTC)"], format="%d/%m/%Y %H:%M")
print(data.head(20))

data.drop(columns=["Data", "Hora (UTC)"], inplace=True)

data.fillna(method="ffill", inplace=True)

data.set_index("datetime", inplace=True)

relevant_data = data[["Temp. Ins. (C)", "Radiacao (KJ/m²)"]]

relevant_data.plot(subplots=True, figsize=(10, 6), title="Weather Data Trends")

#plt.savefig('grafico.png')

temperature = data["Temp. Ins. (C)"]

temperature = temperature.dropna()

model = auto_arima(temperature, seasonal=False, m=24, trace=True, stepwise=True)
model.summary()

forecast = model.predict(n_periods=24)

plt.plot(temperature, label="Historical Data")
plt.plot(pd.date_range(temperature.index[-1], periods=24, freq="H"), forecast, label="Forecast")
plt.legend()
plt.savefig("arima-result.png")

forecast = model.predict(n_periods=1)

print(f"A previsão de temperatura para o dia seguinte é: {forecast[0]:.2f}°C")

