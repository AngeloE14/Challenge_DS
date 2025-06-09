import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde URLs de GitHub
urls = [
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_1%20.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_2.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_3.csv",
    "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_4.csv"
]

# Leer cada tienda
tiendas = [pd.read_csv(url) for url in urls]

# Función para extraer métricas

def extraer_metricas(df):
    # Normalizar nombres de columnas para evitar errores por mayúsculas/minúsculas o espacios
    df = df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'))
    ingresos = df["precio"].sum() if "precio" in df.columns else None
    categoria_mas_vendida = df["categoría_del_producto"].mode()[0] if "categoría_del_producto" in df.columns and not df["categoría_del_producto"].empty else None
    producto_mas_vendido = df["producto"].mode()[0] if "producto" in df.columns and not df["producto"].empty else None
    promedio_resenas = df["calificación"].mean() if "calificación" in df.columns and not df["calificación"].empty else None
    return {
        "Ingresos totales": ingresos,
        "Categoría más vendida": categoria_mas_vendida,
        "Producto más vendido": producto_mas_vendido,
        "Promedio reseñas": round(promedio_resenas, 2) if promedio_resenas is not None else None
    }

# Extraer métricas para cada tienda
resultados = {f"Tienda {i}": extraer_metricas(tienda) for i, tienda in enumerate(tiendas, start=1)}

df_resultados = pd.DataFrame(resultados).T

# --- Visualizaciones ---

# 1. Ingresos por tienda
plt.figure(figsize=(8, 5))
ax1 = df_resultados["Ingresos totales"].astype(float).plot(kind="bar", color="mediumseagreen")
plt.title("Ingresos por tienda")
plt.ylabel("Ingresos (USD)")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
for i, v in enumerate(df_resultados["Ingresos totales"].astype(float)):
    ax1.text(i, v + max(df_resultados["Ingresos totales"].astype(float)) * 0.01, f"${v:,.0f}", ha='center', va='bottom', fontsize=9)
plt.savefig("ingresos_por_tienda.png")
plt.close()

# 2. Categoría más vendida por tienda (gráfico circular)
categorias = df_resultados["Categoría más vendida"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(categorias, labels=categorias.index, autopct=lambda p: f'{p:.1f}%\n({int(p*sum(categorias)/100)})', startangle=140, colors=plt.cm.Set3.colors)
plt.title("Categoría más vendida (por tienda)")
plt.tight_layout()
plt.savefig("categoria_mas_vendida.png")
plt.close()

# 3. Dispersión: Reseñas (no hay envío)
plt.figure(figsize=(8, 5))
for tienda, fila in df_resultados.iterrows():
    plt.scatter(float(fila["Promedio reseñas"]), 1, label=tienda, s=120, edgecolor='k')
plt.xlabel("Promedio de reseñas")
plt.yticks([])
plt.title("Promedio de reseñas por tienda")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig("promedio_resenas.png")
plt.close()

# Mostrar métricas de forma más legible
print("\nResumen de métricas por tienda:\n")
print(df_resultados.to_string())
print("\nLas gráficas han sido guardadas como archivos PNG en el directorio actual.")
