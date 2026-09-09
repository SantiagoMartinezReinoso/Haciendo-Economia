"""
# TALLER 5: Climate Change
# Integrantes: Santiago Gómez, Santiago Martinez, Sara Rodriguez, Emily Rodriguez
Preguntas 1.3.3 y 1.3.4 
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# 0. Carpeta de salida (se crea automaticamente si no existe)

carpeta_figuras = r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Figures"
os.makedirs(carpeta_figuras, exist_ok=True)


# 1. Cargar y limpiar los datos de CO2

co2 = pd.read_excel(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Raw data\CO2.xlsx")
co2 = co2.rename(columns={"Monthly average": "average"})

# -99.99 es el codigo de dato faltante que usa NOAA para "average";
# lo convertimos a NaN para no confundirlo con una medicion real.
co2["average"] = co2["average"].replace(-99.99, np.nan)

# Control de calidad basico (Bjarkefur et al.): revisar rango y huecos
co2_ordenado_temporal = co2.sort_values(["Year", "Month"])
primera_fila, ultima_fila = co2_ordenado_temporal.iloc[0], co2_ordenado_temporal.iloc[-1]
print(f"Rango de datos de CO2: {int(primera_fila['Year'])}-{int(primera_fila['Month']):02d} "
      f"a {int(ultima_fila['Year'])}-{int(ultima_fila['Month']):02d}")
print("Meses con 'average' faltante (rellenados via 'Interpolated'):",
      co2["average"].isna().sum())

co2["fecha"] = pd.to_datetime(dict(year=co2["Year"], month=co2["Month"], day=1))
co2 = co2.sort_values("fecha").reset_index(drop=True)

# Nos quedamos desde enero de 1960, como pide el taller
co2_1960 = co2[co2["fecha"] >= "1960-01-01"].copy()

# 2. Pregunta 1.3.3: grafico de linea de CO2 en el tiempo

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(co2_1960["fecha"], co2_1960["Interpolated"], label="Interpolado",
        color="#1f77b4", linewidth=1.1)
ax.plot(co2_1960["fecha"], co2_1960["Trend"], label="Tendencia (sin ciclo estacional)",
        color="#d62728", linewidth=1.6)
ax.set_title("Concentración de CO2 en la atmósfera - Observatorio de Mauna Loa\n"
             f"(enero 1960 - {co2_1960['fecha'].max().strftime('%m/%Y')})")
ax.set_xlabel("Año")
ax.set_ylabel("Concentración de CO2 (ppm, partes por millón)")
ax.legend(loc="upper left", frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(carpeta_figuras, "fig5_co2_tiempo.png"), dpi=200)
plt.close(fig)
print(f"Guardado: {os.path.join(carpeta_figuras, 'fig5_co2_tiempo.png')}")

print(f"\nCO2 (interpolado) en enero de 1960: "
      f"{co2_1960[co2_1960['fecha']=='1960-01-01']['Interpolated'].values}")
ultimo = co2_1960.iloc[-1]
print(f"CO2 (interpolado) en el ultimo mes disponible ({ultimo['fecha'].strftime('%Y-%m')}): "
      f"{ultimo['Interpolated']:.2f} ppm")
print(f"Aumento total interpolado entre 1960 y el final del archivo: "
      f"{ultimo['Interpolated'] - co2_1960.iloc[0]['Interpolated']:.2f} ppm")


# 3. Pregunta 1.3.4: dispersión CO2 vs. anomalía de temperatura

mes_elegido = "Jan"  # debe coincidir con el mes usado en la Parte 1.1
temp = pd.read_csv(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Raw data\Air&WaterTempAnom.csv", skiprows=1, na_values="***")
temp_mes = temp[["Year", mes_elegido]].rename(columns={mes_elegido: "anomalia_temp"})

co2_mes = co2[co2["fecha"].dt.month == 1].copy()  # enero, para que coincida con mes_elegido
co2_mes["Year"] = co2_mes["fecha"].dt.year

datos = pd.merge(temp_mes, co2_mes[["Year", "Trend"]], on="Year", how="inner").dropna()
print(f"\nAños disponibles para el cruce CO2-temperatura (enero): "
      f"{datos['Year'].min()}-{datos['Year'].max()} (n={len(datos)})")

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(datos["anomalia_temp"], datos["Trend"], color="#1f77b4", alpha=0.75,
           edgecolor="white", s=50)
ax.set_title(f"CO2 vs. anomalía de temperatura en enero ({datos['Year'].min()}-{datos['Year'].max()})\n"
             "cada punto representa un año")
ax.set_xlabel("Anomalía de temperatura (°C, respecto a 1951-1980)")
ax.set_ylabel("Concentración de CO2 - tendencia (ppm)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(carpeta_figuras, "fig6_dispersion_co2_temp.png"), dpi=200)
plt.close(fig)
print(f"Guardado: {os.path.join(carpeta_figuras, 'fig6_dispersion_co2_temp.png')}")

# Coeficiente de correlacion de Pearson (con su valor p, para reportar
# tambien la significancia estadistica)
r, valor_p = stats.pearsonr(datos["anomalia_temp"], datos["Trend"])
print(f"\nCorrelación de Pearson entre CO2 (tendencia) y anomalía de temperatura "
      f"en enero: r = {r:.3f}  (valor p = {valor_p:.2e}, n = {len(datos)} años)")
print(f"r² (proporción de la varianza compartida): {r**2:.3f}")