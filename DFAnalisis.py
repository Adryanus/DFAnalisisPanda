import pandas as pd

file_id = "1sqrRHPmPPcc28KmkTlJfZZZGBKbEFsgg"

url = f"https://drive.google.com/uc?export=download&id={file_id}"

df = pd.read_csv(url)

df.head()

print("\n" + "="*50 + "\n")
print("LIMPIEZA DE DATOS")
print("\n" + "="*50 + "\n")

print(df)

print("\n")
print("COLUMNAS DEL DATAFRAME")

print("=" * 60)

print(df.columns)

# =======================================================
# BUSCAR DUPLICADOS
# ======================================================

duplicados = df[
    df.duplicated(
        subset=['ID_Transaccion'],
        keep='first'
    )
]

print("\n")
print("FILAS DUPLICADAS")
print("=" * 60)

print(duplicados)


# ============================================================ 
# ELIMINAR DUPLICADOS 
# ============================================================ 
df_limpio = df.drop_duplicates( subset=['ID_Transaccion'], keep='first' ).copy() 
print("\n")
print("DATAFRAME DESPUÉS DE ELIMINAR DUPLICADOS") 
print("=" * 60) 
print(df_limpio) 
print("\nFilas originales:", len(df)) 
print("Filas después de eliminar duplicados:", len(df_limpio))

# ============================================================
# PASO 4 - LIMPIAR NOMBRES DE CLIENTES
# ============================================================

print("ANTES DE LIMPIAR CLIENTE_NOMBRE")
print("=" * 60)

print(df_limpio['Cliente_Nombre'])
# Ahora limpiamos los nombres

df_limpio['Cliente_Nombre'] = (
    df_limpio['Cliente_Nombre']
    .astype(str)
    .str.strip()
    .str.lower()
)

print("DESPUÉS DE LIMPIAR CLIENTE_NOMBRE")
print("=" * 60)

print(df_limpio['Cliente_Nombre'])

# PASO 5 - LIMPIAR CATEGORÍAS
# ============================================================

print("ANTES DE LIMPIAR CATEGORIA_PRODUCTO")
print("=" * 60)

print(df_limpio['Categoria_Producto'])
# Limpiar categorías

df_limpio['Categoria_Producto'] = (
    df_limpio['Categoria_Producto']
    .astype(str)
    .str.strip()
    .str.lower()
)

print("DESPUÉS DE LIMPIAR CATEGORIA_PRODUCTO")
print("=" * 60)

print(df_limpio['Categoria_Producto'])


# ============================================================
# PASO 6 - PREPARAR EL PRECIO
# ============================================================
print("\n")
print("PRECIO ORIGINAL")
print("=" * 60)

print(df_limpio['Precio_Unitario'])
# Convertimos el precio a texto

df_limpio['Precio_Unitario'] = (
    df_limpio['Precio_Unitario']
    .astype(str)
)
print("\n")
print("PRECIO CONVERTIDO A TEXTO")
print("=" * 60)

print(df_limpio['Precio_Unitario'])
# Cambiar coma decimal por punto

df_limpio['Precio_Unitario'] = (
    df_limpio['Precio_Unitario']
    .str.replace(',', '.')
)
print("\n")
print("DESPUÉS DE CAMBIAR COMA POR PUNTO")
print("=" * 60)

print(df_limpio['Precio_Unitario'])
# Convertir el precio a número

df_limpio['Precio_Unitario'] = pd.to_numeric(
    df_limpio['Precio_Unitario'],
    errors='coerce'
)

print("\n")
print("PRECIO CONVERTIDO A NÚMERO")
print("=" * 60)

print(df_limpio['Precio_Unitario'])

# Convertir el precio a número 
df_limpio['Precio_Unitario'] = pd.to_numeric( df_limpio['Precio_Unitario'], errors='coerce' ) 

print("\n")
print("TIPO DE DATO") 
print("=" * 60) 
print("\nTipo de dato:") 
print(df_limpio['Precio_Unitario'].dtype)

# ============================================================ 
# PASO 7 - BUSCAR VALORES FALTANTES EN EL PRECIO 
# ============================================================ 
print("\n")
print("VALORES FALTANTES EN PRECIO") 
print("=" * 60) 
print(df_limpio['Precio_Unitario'].isna()) 
print( "\nCantidad de precios faltantes:", df_limpio['Precio_Unitario'].isna().sum() )

# ============================================================ 
# PASO 8 - CALCULAR LA MEDIA DEL PRECIO 
# ============================================================ 
media_precio = ( df_limpio['Precio_Unitario'] .mean() ) 
print("\n")
print("MEDIA DEL PRECIO") 
print("=" * 60) 
print(media_precio)

# ============================================================ 
# PASO 9 - REEMPLAZAR VALORES FALTANTES 
# ============================================================ 
df_limpio['Precio_Unitario'] = ( df_limpio['Precio_Unitario'] .fillna(media_precio) ) 
print("\n")
print("PRECIO DESPUÉS DE FILLNA") 
print("=" * 60) 
print(df_limpio['Precio_Unitario']) 
print( "\nPrecios faltantes:", df_limpio['Precio_Unitario'].isna().sum() )

# ============================================================
# PASO 10 - LIMPIAR MÉTODO DE PAGO
# ============================================================

print("\n")
print("MÉTODO DE PAGO ORIGINAL")
print("=" * 60)

print(df_limpio['Metodo_Pago'])
# Limpiar espacios y convertir a minúsculas

df_limpio['Metodo_Pago'] = (
    df_limpio['Metodo_Pago']
    .astype(str)
    .str.strip()
    .str.lower()
)
print("\n")
print("MÉTODO DE PAGO LIMPIO")
print("=" * 60)

print(df_limpio['Metodo_Pago'])

# ============================================================ 
# PASO 11 - REEMPLAZAR BTC_CRYPTO 
# ============================================================ 
df_limpio['Metodo_Pago'] = ( df_limpio['Metodo_Pago'] .replace( 'btc_crypto', 'desconocido' ) ) 
print("\n")
print("MÉTODO DE PAGO DESPUÉS DEL REEMPLAZO") 
print("=" * 60) 
print(df_limpio['Metodo_Pago'])

# ============================================================
# PASO 12 - CONVERTIR FECHAS
# ============================================================
print("\n")
print("FECHAS ORIGINALES")
print("=" * 60)

print(df_limpio['Fecha_Venta'])
# Convertir las fechas a datetime

fecha_transformada = pd.to_datetime(
    df_limpio['Fecha_Venta'],
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

# PASO 13 - BUSCAR FECHAS INVÁLIDAS
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
# PASO 14 - FORMATEAR LAS FECHAS
# ============================================================

df_limpio['Fecha_Venta'] = (
    fecha_transformada
    .dt.strftime('%d-%m-%Y')
)
print("\n")
print("FECHAS FORMATEADAS")
print("=" * 60)

print(df_limpio['Fecha_Venta'])
# ============================================================
# PASO 15 - REEMPLAZAR FECHAS FALTANTES
# ============================================================

df_limpio['Fecha_Venta'] = (
    df_limpio['Fecha_Venta']
    .fillna('Sin Fecha')
)
print("\n")
print("FECHAS DESPUÉS DE FILLNA")
print("=" * 60)

print(df_limpio['Fecha_Venta'])

# ============================================================
# PASO 16 - CALCULAR TOTAL_CALCULADO 
# ============================================================ 
df_limpio['Total_Calculado'] = ( df_limpio['Cantidad'] * df_limpio['Precio_Unitario'] ) 
print("\n")
print("TOTAL CALCULADO") 
print("=" * 60) 
print( df_limpio[ [ 'Cantidad', 'Precio_Unitario', 'Total_Calculado' ] ] )

# ============================================================
# PASO 17 - CREAR DF_TRANSFORMADO
# ============================================================

df_transformado = df_limpio.drop(
    columns=['Estatus_Auditoria']
)

print("\nDF_TRANSFORMADO")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 18 - ELIMINAR CATEGORÍAS ERRÓNEAS
# ============================================================

df_transformado = df_transformado[
    df_transformado['Categoria_Producto']
    !=
    'error_cat'
]

print("\nDESPUÉS DE ELIMINAR error_cat")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 19 - REINICIAR LOS ÍNDICES
# ============================================================

df_transformado = (
    df_transformado
    .reset_index(drop=True)
)

print("\nÍNDICES REINICIADOS")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 20 - CREAR DICCIONARIO DE DÍAS
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
# PASO 21 - OBTENER EL DÍA DE LA SEMANA
# ============================================================

dias_ingles = (
    fecha_transformada
    .dt.day_name()
)

print("\nDÍAS EN INGLÉS")
print("=" * 60)

print(dias_ingles)
# ============================================================
# PASO 22 - TRADUCIR LOS DÍAS AL ESPAÑOL
# ============================================================

df_transformado['Dia_Venta'] = (
    fecha_transformada
    .dt.day_name()
    .map(dias_es)
)

print("\nDATAFRAME CON DIA_VENTA")
print("=" * 60)

print(df_transformado)
# ============================================================
# PASO 23 - GROUPBY
# FACTURACIÓN POR CLIENTE
# ============================================================

clientes = (
    df_limpio
    .groupby('Cliente_Nombre')
    ['Total_Calculado']
    .agg(
        Facturacion_Total='sum',

        Cantidad_compras='count',

        Transacciones='count'
    )
    .sort_values(
        by='Facturacion_Total',
        ascending=False
    )
)

print("\nFACTURACIÓN POR CLIENTE")
print("=" * 60)

print(clientes)
# ============================================================
# PASO 24 - PIVOT TABLE
# ============================================================

tabla_matriz = (
    df_limpio
    .pivot_table(

        index='Cliente_Nombre',

        columns=[
            'Categoria_Producto',
            'Metodo_Pago'
        ],

        values=[
            'Total_Calculado',
            'Cantidad'
        ],

        aggfunc=[
            'sum',
            'max'
        ],

        fill_value=0
    )
)

print("\nTABLA MATRIZ")
print("=" * 60)

print(tabla_matriz)
# ============================================================
# PASO 25 - VER EL DATAFRAME FINAL
# ============================================================

print("\nDATAFRAME FINAL")
print("=" * 60)

print(df_transformado)