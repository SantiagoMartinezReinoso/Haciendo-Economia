"""
# TALLER 5: Climate Change
# Integrantes: Santiago Gómez, Santiago Martinez, Sara Rodriguez, Emily Rodriguez 
# Parte 1.1.2 y 1.1.3
"""
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar los datos

#skiprows ignora la primera fila donde aparece el titulo de la base
# na_values='***', tenemos en cuenta que la NASA usa "***" para marcar datos faltantes
ruta_datos = r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Raw data\Air&WaterTempAnom.csv"
temp = pd.read_csv(ruta_datos, skiprows=1, na_values="***")

# revisamos que Year sea numerico y que el rango de años sea el esperado.
assert temp["Year"].is_monotonic_increasing, "Los años no estan ordenados"
print("Rango de años en los datos:", temp["Year"].min(), "-", temp["Year"].max())

# El ultimo año puede estar incompleto (por ejemplo 2026)
# Lo dejamos en el dato mensual y estacional (donde si hay
# informacion), pero lo excluimos del grafico anual (J-D) si esa
# columna quedo vacia, para no dibujar un "cero".
temp_anual = temp.dropna(subset=["J-D"]).copy()


# 2. Grafico 1: un mes elegido a lo largo del tiempo (enero)

mes_elegido = "Jan" 

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(temp["Year"], temp[mes_elegido], color="#9f1717", linewidth=1.3)

# Linea de referencia en cero, con su etiqueta
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.text(temp["Year"].min(), 0.05, "promedio de 1951 a 1980", fontsize=9,
        va="bottom", ha="left")

ax.set_title("Anomalía de temperatura en enero - Hemisferio Norte (1880-"
             f"{int(temp['Year'].max())})")
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C, respecto a 1951-1980)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Figures\fig1_anomalia_mensual_enero.png", dpi=600)
plt.close(fig)

promedio_enero = temp[mes_elegido].mean()
print(f"Promedio de la anomalía en {mes_elegido} (1880-{int(temp['Year'].max())}): {promedio_enero:.3f} °C")


# 3. Grafico 2: promedio por estacion (DJF, MAM, JJA, SON)

estaciones = {
    "DJF": "Invierno (dic-ene-feb)",
    "MAM": "Primavera (mar-abr-may)",
    "JJA": "Verano (jun-jul-ago)",
    "SON": "Otoño (sep-oct-nov)",
}

fig, ax = plt.subplots(figsize=(9, 5))
colores = ["#1414d7", "#1f611f", "#ee1010", "#ff7f0e"]
for color, (col, etiqueta) in zip(colores, estaciones.items()):
    ax.plot(temp["Year"], temp[col], label=etiqueta, linewidth=1.1, color=color)

ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.text(temp["Year"].min(), 0.05, "promedio de 1951 a 1980", fontsize=9,
        va="bottom", ha="left")

ax.set_title("Anomalía de temperatura por estación - Hemisferio Norte "
             f"(1880-{int(temp['Year'].max())})")
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C, respecto a 1951-1980)")
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Figures\fig2_anomalia_estacional.png", dpi=600)
plt.close(fig)


# 4. Grafico 3: promedio anual (columna J-D = enero a diciembre)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(temp_anual["Year"], temp_anual["J-D"], color="#111ac7", linewidth=1.4)

ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.text(temp_anual["Year"].min(), 0.05, "promedio de 1951 a 1980", fontsize=9,
        va="bottom", ha="left")

ax.set_title("Anomalía de temperatura anual - Hemisferio Norte (1880-"
             f"{int(temp_anual['Year'].max())})")
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C, respecto a 1951-1980)")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Figures\fig3_anomalia_anual.png", dpi=600)
plt.close(fig)
