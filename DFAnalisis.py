import pandas as pd
# =======================================================
# PASO 1 - LEER DATA SET E IDENTIFICAR COLUMNAS
# ======================================================
#file_id = "1sqrRHPmPPcc28KmkTlJfZZZGBKbEFsgg"

file_id = "1jlo-TjeDEkIeHrbcdSVXO8pqzTTfyE6N"

url = f"https://drive.google.com/uc?export=download&id={file_id}"

df = pd.read_csv(url)

print(df.head())


print("\n" + "="*50 + "\n")
print("LIMPIEZA DE DATOS")
print("\n" + "="*50 + "\n")

print(df)

print("\n")
print("COLUMNAS DEL DATAFRAME")

print("=" * 60)

print(df.columns)

# =======================================================
# PASO 2 - BUSCAR DUPLICADOS
# ======================================================

duplicados = df[
    df.duplicated(
        subset=['id_venta'],
        keep='first'
    )
]

print("\n")
print("FILAS DUPLICADAS")
print("=" * 60)

print(duplicados)


# ============================================================ 
# PASO 3  - ELIMINAR DUPLICADOS 
# ============================================================ 
df_limpio = df.drop_duplicates( subset=['id_venta'], keep='first' ).copy() 
print("\n")
print("DATAFRAME DESPUÉS DE ELIMINAR DUPLICADOS") 
print("=" * 60) 
print(df_limpio) 
print("\nFilas originales:", len(df)) 
print("Filas después de eliminar duplicados:", len(df_limpio))

# ============================================================
# PASO 4 - LIMPIAR NOMBRES DE PRODUCTOS
# ============================================================

print("\nANTES DE LIMPIAR PRODUCTO")
print("=" * 60)

print(df_limpio['producto'])
# Ahora limpiamos los nombres

df_limpio['producto'] = (
    df_limpio['producto']
    .str.strip()
    .str.lower()
)

print("\nDESPUÉS DE LIMPIAR producto")
print("=" * 60)

print(df_limpio['producto'])

# PASO 5 - LIMPIAR CATEGORÍAS
# ============================================================

print("ANTES DE LIMPIAR categoria")
print("=" * 60)

print(df_limpio['categoria'])
# Limpiar categorías

df_limpio['categoria'] = (
    df_limpio['categoria']
    .str.strip()
    .str.lower()
)

print("DESPUÉS DE LIMPIAR categoria")
print("=" * 60)

print(df_limpio['categoria'])


# ============================================================
# PASO 6 - PREPARAR EL PRECIO
# ============================================================

print("\n")
print("PRECIO ORIGINAL")
print("=" * 60)

print(df_limpio['precio'])

# Eliminar el signo $
df_limpio['precio'] = (
    df_limpio['precio']
    .str.replace('$', '', regex=False)
    .str.strip()
)

print("\nPRECIO SIN SIGNO $")
print("=" * 60)

print(df_limpio['precio'])

# Cambiar coma decimal por punto
df_limpio['precio'] = (
    df_limpio['precio']
    .str.replace(',', '.', regex=False)
)

print("\nDESPUÉS DE CAMBIAR COMA POR PUNTO")
print("=" * 60)

print(df_limpio['precio'])

# Convertir el precio a número
df_limpio['precio'] = pd.to_numeric(
    df_limpio['precio'],
    errors='coerce'
)

print("\nPRECIO CONVERTIDO A NÚMERO")
print("=" * 60)

print(df_limpio['precio'])

print("\nTIPO DE DATO")
print("=" * 60)

print(df_limpio['precio'].dtype)

# ============================================================ 
# PASO 7 - BUSCAR VALORES FALTANTES EN EL PRECIO 
# ============================================================ 
print("\n")
print("VALORES FALTANTES EN PRECIO") 
print("=" * 60) 
print(df_limpio['precio'].isna()) 
print( "\ncantidad de precios faltantes:", df_limpio['precio'].isna().sum() )

# ============================================================ 
# PASO 8 - CALCULAR LA MEDIA DEL PRECIO 
# ============================================================ 
media_precio = ( df_limpio['precio'] .mean() ) 
print("\n")
print("MEDIA DEL PRECIO") 
print("=" * 60) 
print(media_precio)

# ============================================================ 
# PASO 9 - REEMPLAZAR VALORES FALTANTES 
# ============================================================ 
df_limpio['precio'] = ( df_limpio['precio'] .fillna(media_precio) ) 
print("\n")
print("PRECIO DESPUÉS DE FILLNA") 
print("=" * 60) 
print(df_limpio['precio']) 
print( "\nPrecios faltantes:", df_limpio['precio'].isna().sum() )



# ============================================================
# PASO 10 - CONVERTIR FECHAS
# ============================================================
print("\n")
print("FECHAS ORIGINALES")
print("=" * 60)

print(df_limpio['fecha_venta'])
# Convertir las fechas a datetime

fecha_transformada = pd.to_datetime(
    df_limpio['fecha_venta'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)
print("\n")
print("FECHAS CONVERTIDAS A DATETIME")
print("=" * 60)

print(fecha_transformada)

print("\nTipo de dato:") 
print(fecha_transformada.dtype)

# PASO 11 - BUSCAR FECHAS INVÁLIDAS
# ============================================================
print("\n")
print("FECHAS INVÁLIDAS")
print("=" * 60)

print(
    fecha_transformada[
        fecha_transformada.isna()
    ]
)
# ============================================================
# PASO 12 - FORMATEAR LAS FECHAS
# ============================================================

df_limpio['fecha_venta'] = (
    fecha_transformada
    .dt.strftime('%d-%m-%Y')
)
print("\n")
print("FECHAS FORMATEADAS")
print("=" * 60)

print(df_limpio['fecha_venta'])
# ============================================================
# PASO 13 - REEMPLAZAR FECHAS FALTANTES
# ============================================================

df_limpio['fecha_venta'] = (
    df_limpio['fecha_venta']
    .fillna('Sin Fecha')
)
print("\n")
print("FECHAS DESPUÉS DE FILLNA")
print("=" * 60)

print(df_limpio['fecha_venta'])

# ============================================================
# PASO 14 - CALCULAR TOTAL_CALCULADO 
# ============================================================ 
df_limpio['Total_Calculado'] = ( df_limpio['cantidad'] * df_limpio['precio'] ) 
print("\n")
print("TOTAL CALCULADO") 
print("=" * 60) 
print( df_limpio[ [ 'cantidad', 'precio', 'Total_Calculado' ] ] )

# ============================================================
# PASO 15 - CREAR DF_TRANSFORMADO
# ============================================================

df_transformado = df_limpio.drop(
    columns=['Estatus_Auditoria'],
    errors='ignore'
)

print("\nDF_TRANSFORMADO")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 16 - ELIMINAR CATEGORÍAS ERRÓNEAS
# ============================================================

df_transformado = df_transformado[
    df_transformado['categoria']
    !=
    'error_cat'
]

print("\nDESPUÉS DE ELIMINAR error_cat")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 17 - REINICIAR LOS ÍNDICES
# ============================================================

df_transformado = (
    df_transformado
    .reset_index(drop=True)
)

print("\nÍNDICES REINICIADOS")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 18 - CREAR DICCIONARIO DE DÍAS
# Se utiliza para traducir los nombres de los días al español.
# ============================================================

dias_es = {

    'Monday': 'Lunes',

    'Tuesday': 'Martes',

    'Wednesday': 'Miércoles',

    'Thursday': 'Jueves',

    'Friday': 'Viernes',

    'Saturday': 'Sábado',

    'Sunday': 'Domingo'
}

print(dias_es)

# ============================================================
# PASO 19 - OBTENER EL DÍA DE LA SEMANA
# ============================================================

dias_ingles = (
    pd.to_datetime(
        df_transformado['fecha_venta'],
        format='%d-%m-%Y',
        errors='coerce'
    )
    .dt.day_name()
)

print("\nDÍAS EN INGLÉS")
print("=" * 60)

print(dias_ingles)
# ============================================================
# PASO 20 - TRADUCIR LOS DÍAS AL ESPAÑOL
# ============================================================

df_transformado['Dia_Venta'] = (
    dias_ingles
    .map(dias_es)
)

print("\nDATAFRAME CON DIA_VENTA")
print("=" * 60)

print(df_transformado)

print("\nVERIFICACIÓN DE FACTURACIÓN")
print("=" * 60)

print(
    df_transformado[
        ['id_venta', 'producto', 'cantidad', 'precio', 'Total_Calculado']
    ].head(20)
)


# ============================================================
# PASO 21 - GROUPBY
# FACTURACIÓN POR PRODUCTO
# ============================================================

productos = (
    df_transformado
    .groupby('producto')
    .agg(
        Facturacion_Total=('Total_Calculado', 'sum'),
        cantidad_compras=('cantidad', 'sum'),
        Transacciones=('id_venta', 'count')
    )
    .sort_values(
        by='Facturacion_Total',
        ascending=False
    )
)

print("\nFACTURACIÓN POR PRODUCTO")
print("=" * 60)

print(productos)


# ============================================================
# PASO 22 - PIVOT TABLE
# ============================================================

tabla_matriz = (
    df_limpio
    .pivot_table(
        index='producto',
        columns='categoria',
        values='Total_Calculado',
        aggfunc='sum',
        fill_value=0
    )
)

print("\nTABLA MATRIZ")
print("=" * 60)

print(tabla_matriz)
# ============================================================
# PASO 23 - VER EL DATAFRAME FINAL
# ============================================================

print("\nDATAFRAME FINAL")
print("=" * 60)

print(df_transformado)
df_transformado.to_excel("datos_ventas.xlsx", index=False)

print("Archivo Excel creado correctamente.")