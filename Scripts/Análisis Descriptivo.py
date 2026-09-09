"""
# TALLER 5: Climate Change
# Integrantes: Santiago Gómez, Santiago Martinez, Sara Rodriguez, Emily Rodriguez 
# Parte 1.2.1 a 1.2.5, y 1.3.4

Usamos los 12 valores mensuales de cada año,
"apilados" en una sola columna, porque con solo 30 promedios
anuales por periodo los deciles pedidos en la pregunta serian 
muy poco confiables (cada decil dependeria de un solo dato). 
Con 12 meses x 30 años = 360 observaciones por periodo, 
el calculo es mucho mas estable.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

usar_mensual = True

# ------------------------------------------------------------------
# 0. Carpeta de salida (se crea automaticamente si no existe)
# ------------------------------------------------------------------
carpeta_figuras = r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Figures"
os.makedirs(carpeta_figuras, exist_ok=True)


def guardar_tabla_como_imagen(df, nombre_archivo, titulo=None, carpeta=carpeta_figuras):
    """Convierte un DataFrame en una imagen PNG con formato de tabla
    y la guarda en la carpeta indicada."""
    fig, ax = plt.subplots(figsize=(0.9 * len(df.columns) + 2, 0.4 * len(df) + 1.2))
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, fontsize=11, pad=12)

    tabla = ax.table(
        cellText=df.round(3).astype(str).values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.4)

    # Encabezado con color
    for j in range(len(df.columns)):
        tabla[0, j].set_facecolor("#dfe7f5")
        tabla[0, j].set_text_props(weight="bold")

    fig.tight_layout()
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    fig.savefig(ruta_completa, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Guardado: {ruta_completa}")


# ------------------------------------------------------------------
# 1. Cargar datos y construir las series por periodo
# ------------------------------------------------------------------
temp = pd.read_csv(r"C:\Users\Emily\OneDrive\Documentos\Haciendo Economía\Taller 5\Raw data\Air&WaterTempAnom.csv", skiprows=1, na_values="***")
meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def serie_del_periodo(temp, año_ini, año_fin):
    """Devuelve un arreglo 1D con las anomalias mensuales (apiladas)
    de un periodo [año_ini, año_fin], sin valores faltantes."""
    sub = temp[(temp["Year"] >= año_ini) & (temp["Year"] <= año_fin)]
    if usar_mensual:
        valores = sub[meses].values.flatten()
    else:
        valores = sub["J-D"].values
    return valores[~np.isnan(valores)]


periodo_1 = serie_del_periodo(temp, 1951, 1980)  # periodo de referencia
periodo_2 = serie_del_periodo(temp, 1981, 2010)  # periodo reciente

print(f"Observaciones 1951-1980: {len(periodo_1)}")
print(f"Observaciones 1981-2010: {len(periodo_2)}")

# ------------------------------------------------------------------
# 2. Pregunta 1.2.1: tablas de frecuencias
# ------------------------------------------------------------------
# Usamos los MISMOS bordes de intervalo (bins) para ambos periodos,
# de modo que las dos tablas/histogramas sean directamente comparables.
bin_min = np.floor(min(periodo_1.min(), periodo_2.min()) * 5) / 5
bin_max = np.ceil(max(periodo_1.max(), periodo_2.max()) * 5) / 5
bordes = np.arange(bin_min, bin_max + 0.2, 0.2).round(2)


def tabla_frecuencias(valores, bordes):
    cortes = pd.cut(valores, bins=bordes, right=False)
    tabla = cortes.value_counts().sort_index().reset_index()
    tabla.columns = ["Intervalo (°C)", "Frecuencia"]
    tabla["Porcentaje"] = (tabla["Frecuencia"] / tabla["Frecuencia"].sum() * 100).round(1)
    return tabla


tabla_1951_1980 = tabla_frecuencias(periodo_1, bordes)
tabla_1981_2010 = tabla_frecuencias(periodo_2, bordes)

print("\nTabla de frecuencias 1951-1980:")
print(tabla_1951_1980.to_string(index=False))
print("\nTabla de frecuencias 1981-2010:")
print(tabla_1981_2010.to_string(index=False))

# Convertimos el intervalo (Interval) a texto para que se vea bien en la imagen
tabla_1951_1980_img = tabla_1951_1980.copy()
tabla_1951_1980_img["Intervalo (°C)"] = tabla_1951_1980_img["Intervalo (°C)"].astype(str)
tabla_1981_2010_img = tabla_1981_2010.copy()
tabla_1981_2010_img["Intervalo (°C)"] = tabla_1981_2010_img["Intervalo (°C)"].astype(str)

guardar_tabla_como_imagen(tabla_1951_1980_img, "tabla_frecuencias_1951_1980.png",
                           titulo="Frecuencias de anomalías mensuales (1951-1980)")
guardar_tabla_como_imagen(tabla_1981_2010_img, "tabla_frecuencias_1981_2010.png",
                           titulo="Frecuencias de anomalías mensuales (1981-2010)")

# ------------------------------------------------------------------
# 3. Pregunta 1.2.2: histogramas
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True, sharex=True)

axes[0].hist(periodo_1, bins=bordes, color="#64a2ce", edgecolor="white")
axes[0].set_title("1951-1980")
axes[0].set_xlabel("Anomalía de temperatura mensual (°C)")
axes[0].set_ylabel("Número de meses")

axes[1].hist(periodo_2, bins=bordes, color="#d88f8f", edgecolor="white")
axes[1].set_title("1981-2010")
axes[1].set_xlabel("Anomalía de temperatura mensual (°C)")

for ax in axes:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")

fig.suptitle("Distribución de anomalías mensuales de temperatura - "
             "Hemisferio Norte", y=1.03)
fig.tight_layout()
fig.savefig(os.path.join(carpeta_figuras, "fig4_histogramas_periodos.png"),
            dpi=200, bbox_inches="tight")
plt.close(fig)
print(f"Guardado: {os.path.join(carpeta_figuras, 'fig4_histogramas_periodos.png')}")

# ------------------------------------------------------------------
# 4. Pregunta 1.2.3: deciles 3 y 7 de 1951-1980
# ------------------------------------------------------------------
decil_3 = np.quantile(periodo_1, 0.3)
decil_7 = np.quantile(periodo_1, 0.7)
print(f"\nDecil 3 (umbral 'frio') 1951-1980: {decil_3:.3f} °C")
print(f"Decil 7 (umbral 'caliente') 1951-1980: {decil_7:.3f} °C")

# ------------------------------------------------------------------
# 5. Pregunta 1.2.4: % de meses "calientes" en 1981-2010
# ------------------------------------------------------------------
pct_caliente_1981_2010 = (periodo_2 > decil_7).mean() * 100
pct_frio_1981_2010 = (periodo_2 < decil_3).mean() * 100
print(f"\n% de meses 'calientes' (> decil 7 de 1951-1980) en 1981-2010: "
      f"{pct_caliente_1981_2010:.1f}%")
print(f"% de meses 'frios' (< decil 3 de 1951-1980) en 1981-2010: "
      f"{pct_frio_1981_2010:.1f}%")
# Como referencia: en el propio periodo 1951-1980, por construccion,
# el 30% de los meses es "caliente" y el 30% es "frio".
print("(Referencia: por construccion, en 1951-1980 el 30.0% es 'caliente' "
      "y el 30.0% es 'frio')")

# ------------------------------------------------------------------
# 6. Pregunta 1.2.5: media y varianza estacional en tres periodos
# ------------------------------------------------------------------
estaciones = ["DJF", "MAM", "JJA", "SON"]
periodos = {"1921-1950": (1921, 1950), "1951-1980": (1951, 1980),
            "1981-2010": (1981, 2010)}

filas = []
for nombre_periodo, (ini, fin) in periodos.items():
    sub = temp[(temp["Year"] >= ini) & (temp["Year"] <= fin)]
    for est in estaciones:
        valores = sub[est].dropna()
        filas.append({
            "Periodo": nombre_periodo,
            "Estacion": est,
            "Media": round(valores.mean(), 3),
            "Varianza": round(valores.var(ddof=1), 4),
            "N": valores.shape[0],
        })

tabla_estaciones = pd.DataFrame(filas)
tabla_pivot_var = tabla_estaciones.pivot(index="Estacion", columns="Periodo", values="Varianza")
tabla_pivot_var = tabla_pivot_var[["1921-1950", "1951-1980", "1981-2010"]]
tabla_pivot_media = tabla_estaciones.pivot(index="Estacion", columns="Periodo", values="Media")
tabla_pivot_media = tabla_pivot_media[["1921-1950", "1951-1980", "1981-2010"]]

print("\nMedia de la anomalia por estacion y periodo:")
print(tabla_pivot_media)
print("\nVarianza de la anomalia por estacion y periodo:")
print(tabla_pivot_var)

guardar_tabla_como_imagen(tabla_pivot_media.reset_index(), "tabla_media_estacional.png",
                           titulo="Media de la anomalía por estación y periodo")
guardar_tabla_como_imagen(tabla_pivot_var.reset_index(), "tabla_varianza_estacional.png",
                           titulo="Varianza de la anomalía por estación y periodo")