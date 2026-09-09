# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:46:50 2026

@author: sarag
"""

import pandas as pd
import numpy as np
from scipy import stats


RUTA_TEMPERATURA = "C:/Users/sarag/OneDrive/Desktop/Taller5/RawData/temperatura_anomalias.csv"
RUTA_CO2 = "C:/Users/sarag/OneDrive/Desktop/Taller5/RawData/CO2.xlsx"

# 1. limpieza de datos de temperatura:

temp = pd.read_csv(RUTA_TEMPERATURA, skiprows=1)

cols_numericas = [c for c in temp.columns if c != "Year"]
for c in cols_numericas:
    temp[c] = pd.to_numeric(temp[c], errors="coerce")

temp["Year"] = pd.to_numeric(temp["Year"], errors="coerce")
temp = temp.dropna(subset=["Year"])
temp["Year"] = temp["Year"].astype(int)

print("Columnas disponibles en temperatura:", list(temp.columns))
print(temp.head())

# 2. tablas de frecuencia:

periodo_1 = temp[(temp["Year"] >= 1951) & (temp["Year"] <= 1980)]["J-D"].dropna()
periodo_2 = temp[(temp["Year"] >= 1981) & (temp["Year"] <= 2010)]["J-D"].dropna()

def tabla_frecuencias(serie, n_bins=8, nombre=""):
    tabla = pd.cut(serie, bins=n_bins)
    frec = tabla.value_counts().sort_index()
    frec_rel = (frec / frec.sum() * 100).round(1)
    resultado = pd.DataFrame({"frecuencia": frec, "frecuencia_%": frec_rel})
    print(f"\n--- Tabla de frecuencias: {nombre} ---")
    print(resultado)
    return resultado

tabla_1951_1980 = tabla_frecuencias(periodo_1, nombre="1951-1980")
tabla_1981_2010 = tabla_frecuencias(periodo_2, nombre="1981-2010")

# 3. deciles 3 y 7 en 1951-1980;

decil_3 = np.quantile(periodo_1, 0.3)
decil_7 = np.quantile(periodo_1, 0.7)

print(f"\nDecil 3 (umbral 'frío') 1951-1980: {decil_3:.3f}")
print(f"Decil 7 (umbral 'caliente') 1951-1980: {decil_7:.3f}")


# 4. anomalías calientes en 1981-2010:

n_calientes = (periodo_2 > decil_7).sum()
pct_calientes = n_calientes / len(periodo_2) * 100

print(f"\n% de años 'calientes' en 1981-2010 (usando umbral de 1951-1980): "
      f"{pct_calientes:.1f}%")

# 5. Media y varianza por estación en 3 periodos:

estaciones = ["DJF", "MAM", "JJA", "SON"]
periodos = {
    "1921-1950": (1921, 1950),
    "1951-1980": (1951, 1980),
    "1981-2010": (1981, 2010),
}

resultados = []
for nombre_periodo, (y1, y2) in periodos.items():
    sub = temp[(temp["Year"] >= y1) & (temp["Year"] <= y2)]
    for est in estaciones:
        media = sub[est].mean()
        varianza = sub[est].var()
        resultados.append({
            "periodo": nombre_periodo,
            "estacion": est,
            "media": round(media, 4),
            "varianza": round(varianza, 4),
        })

tabla_estaciones = pd.DataFrame(resultados)
tabla_pivot_varianza = tabla_estaciones.pivot(index="estacion", columns="periodo", values="varianza")

print("\n-Media y varianza por estación y periodo-")
print(tabla_estaciones)
print("\n-Varianzas (para comparar si aumentan con el tiempo)-")
print(tabla_pivot_varianza)


# 6carga de datos CO2:

co2 = pd.read_excel(RUTA_CO2)
print("\nColumnas disponibles en CO2:", list(co2.columns))

# El valor -99,99 es el código de "dato faltante" de Mauna Loa.
# Lo convertimos a NaN (vacío) para que no dañe los cálculos.
for col in ["Monthly average", "Interpolated", "Trend"]:
    if col in co2.columns:
        co2[col] = co2[col].replace(-99.99, np.nan)

# 7. correlacion de pearson (CO2 vs temperatura):

MES_ELEGIDO = 3  # marzo -- es el primer mes con datos completos en este archivo

co2_mes = co2[co2["Month"] == MES_ELEGIDO][["Year", "Trend"]].rename(
    columns={"Year": "Year", "Trend": "CO2_trend"}
)

temp_anual = temp[["Year", "J-D"]].rename(columns={"J-D": "anomalia"})

datos_combinados = pd.merge(co2_mes, temp_anual, on="Year", how="inner").dropna()

r, p_valor = stats.pearsonr(datos_combinados["CO2_trend"], datos_combinados["anomalia"])

print(f"\nCorrelación de Pearson (CO2 vs anomalía de temperatura): r = {r:.3f}")
print(f"p-valor: {p_valor:.4f}")
print("Interpretación: r cercano a 1 indica una relación lineal positiva fuerte.")
print("Recuerda (1.3.6): correlación fuerte NO implica causalidad.")


# Resumen:

print("\n" + "=" * 60)
print("RESUMEN DE CIFRAS CLAVE PARA EL BRIEFING")
print("=" * 60)
print(f"Decil 3 / Decil 7 (1951-1980): {decil_3:.2f} / {decil_7:.2f}")
print(f"% años calientes en 1981-2010: {pct_calientes:.1f}%")
print(f"Correlación CO2-temperatura: r = {r:.3f} (p = {p_valor:.4f})")
print("Varianzas por estación: ver tabla_pivot_varianza arriba")

