import pandas as pd

data = pd.read_csv("data.csv", delimiter=";", na_values=["", " "], dtype={"Hora (UTC)": str})


numerical_columns = [
    "Temp. Ins. (C)", "Temp. Max. (C)", "Temp. Min. (C)",
    "Umi. Ins. (%)", "Umi. Max. (%)", "Umi. Min. (%)",
    "Pto Orvalho Ins. (C)", "Pto Orvalho Max. (C)", "Pto Orvalho Min. (C)",
    "Pressao Ins. (hPa)", "Pressao Max. (hPa)", "Pressao Min. (hPa)",
    "Vel. Vento (m/s)", "Dir. Vento (m/s)", "Raj. Vento (m/s)", "Radiacao (KJ/m²)", "Chuva (mm)"
]

data["Hora (UTC)"] = data["Hora (UTC)"].apply(lambda x: f"{x[:2]}:{x[2:]}")


# Convert columns to numeric, setting errors='coerce' to handle invalid values
for col in numerical_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")

    if data[col].empty:
        data[col] = None

print(data.head())


""" data["datetime"] = pd.to_datetime(data["Data"] + " " + data["Hora (UTC)"], format="%d/%m/%Y %H%M")

data.drop(columns=["Data", "Hora (UTC)"], inplace=True)

data.fillna(method="ffill", inplace=True)

data.set_index("datetime", inplace=True)

relevant_data = data[["Temp. Ins. (C)", "Chuva (mm)"]] """