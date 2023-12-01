#!/usr/bin/env python
# coding: utf-8

# # Funciones Útiles

# Este archivo contiene funciones útiles para el proceso de Extracción, Transformación y Carga (ETL).

# ## Importar Librerías

# In[ ]:


import pandas as pd
import numpy as np


# ## Funciones

# In[3]:


def cargar_datos_desde_excel(archivo, hojas, engine='openpyxl'):
    """
    Carga datos desde un archivo Excel y devuelve un diccionario de DataFrames.

    Parameters:
    - archivo (str): Ruta del archivo Excel.
    - hojas (list): Lista de nombres de hojas a cargar.
    - engine (str, optional): Motor de Excel a utilizar. Por defecto, 'openpyxl'.

    Returns:
    dfs: Un diccionario donde las claves son los nombres de las hojas y los valores son DataFrames correspondientes.

    Example:
    >>> datos = cargar_datos_desde_excel('archivo.xlsx', ['Hoja1', 'Hoja2'])
    >>> df_hoja1 = datos['Hoja1']
    >>> df_hoja2 = datos['Hoja2']
    """
    
    xls_file = pd.ExcelFile(archivo, engine=engine)
    dfs = {}

    for hoja in hojas:
        df = pd.read_excel(xls_file, hoja) 
        dfs[hoja] = df

    return dfs


# In[4]:


def analizar_valores_sd(dataframe):
    """
    Analiza la presencia de valores 'SD' en cada columna del DataFrame.

    Parameters:
    dataframe (pd.DataFrame): El DataFrame a analizar.

    Returns:
    pd.DataFrame: Un DataFrame que muestra la cantidad y porcentaje de valores 'SD' en cada columna.
    """
    columnas_con_sd = dataframe.columns
    resultados = []

    for columna in columnas_con_sd:
        cantidad_sd = dataframe[columna].eq('SD').sum()
        porcentaje_sd = (cantidad_sd / len(dataframe)) * 100
        resultados.append({'Columna': columna, 'Cantidad de SD': cantidad_sd, 'Porcentaje de SD': porcentaje_sd})

    resultados_df = pd.DataFrame(resultados)
    resultados_con_sd = resultados_df[resultados_df['Cantidad de SD'] > 0]

    return resultados_con_sd


# In[ ]:


def data_cleaning(df, drop_duplicates=False, drop_na=False, fill_na=None, convert_to_datetime=None, uppercase_columns=None,
                  lowercase_columns=None, titlecase_columns=None, strip_spaces=True, rename_columns=None, drop_columns=None,
                  categorize_columns=None, replace_values=None, new_columns=None, convert_date_columns=None):
    """
    Realiza el proceso de limpieza de datos en un DataFrame.

    Parámetros:
    - df (pd.DataFrame): El DataFrame que se va a limpiar.
    - drop_duplicates (bool): Elimina duplicados si es True.
    - drop_na (bool): Elimina filas con valores nulos si es True.
    - fill_na (dict): Un diccionario donde las claves son los nombres de columnas y los valores son valores para rellenar los nulos.
    - convert_to_datetime (list): Lista de columnas para convertir a tipo de dato datetime.
    - uppercase_columns (list): Lista de columnas para convertir a mayúsculas.
    - lowercase_columns (list): Lista de columnas para convertir a minúsculas.
    - titlecase_columns (list): Lista de columnas para convertir a formato de título (primera letra en mayúscula, resto en minúscula).
    - strip_spaces (bool): Elimina espacios en blanco alrededor de los valores de las celdas si es True.
    - rename_columns (dict): Un diccionario donde las claves son los nombres de las columnas actuales y los valores son los nuevos nombres.
    - drop_columns (list): Lista de columnas para eliminar.
    - categorize_columns (list): Lista de columnas para convertir a tipo de dato categoría.
    - replace_values (dict): Un diccionario donde las claves son los nombres de las columnas y los valores son diccionarios de reemplazo.
    - new_columns (dict): Un diccionario donde las claves son los nombres de las nuevas columnas y los valores son valores para esas columnas.
    - convert_date_columns (list): Lista de columnas para convertir a tipo de dato fecha.


    Retorna:
    pd.DataFrame: El DataFrame limpio.
    """
    cleaned_df = df.copy()

    # Eliminar duplicados
    if drop_duplicates:
        cleaned_df.drop_duplicates(inplace=True)

    # Eliminar filas con valores nulos
    if drop_na:
        cleaned_df.dropna(inplace=True)

    # Rellenar valores nulos
    if fill_na:
        cleaned_df.fillna(fill_na, inplace=True)

    # Convertir columnas a tipo datetime
    if convert_to_datetime:
        for column in convert_to_datetime:
            cleaned_df[column] = pd.to_datetime(cleaned_df[column], errors='coerce')

    # Convertir columnas a mayúsculas
    if uppercase_columns:
        for column in uppercase_columns:
            cleaned_df[column] = cleaned_df[column].str.upper()

    # Convertir columnas a minúsculas
    if lowercase_columns:
        for column in lowercase_columns:
            cleaned_df[column] = cleaned_df[column].str.lower()

    # Convertir columnas a formato de título
    if titlecase_columns:
        for column in titlecase_columns:
            cleaned_df[column] = cleaned_df[column].str.title()
            
    # Tratar columnas con espacios
    if strip_spaces:
        cleaned_df = cleaned_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Renombrar columnas
    if rename_columns:
        cleaned_df.rename(columns=rename_columns, inplace=True)
    
    # Eliminar columnas
    if drop_columns:
        cleaned_df.drop(columns=drop_columns, inplace=True)
        
    # Categorizar columnas
    if categorize_columns:
        for column in categorize_columns:
            if column in cleaned_df.columns:
                cleaned_df[column] = cleaned_df[column].astype('category')
            else:
                print(f"La columna '{column}' no existe en el DataFrame.")

    # Reemplazar valores en columnas
    if replace_values:
        for column, replacements in replace_values.items():
            cleaned_df[column].replace(replacements, inplace=True)

    # Agregar nuevas columnas
    if new_columns:
        for column, value in new_columns.items():
            cleaned_df[column] = value
    
    # Convertir columnas de fecha con formato específico
    if convert_date_columns:
        for column, date_format in convert_date_columns.items():
            cleaned_df[column] = pd.to_datetime(cleaned_df[column], format=date_format, errors='coerce')
    #convert_date_columns = {'fecha': '%Y-%m-%d', 'otra_fecha': '%Y-%m-%d %H:%M:%S'}

    return cleaned_df

#mi_dataframe_limpiado = data_cleaning(mi_dataframe, drop_duplicates=True, drop_na=True, fill_na={'columna1': 0, 'columna2': 'valor'}, convert_to_datetime=['fecha'], uppercase_columns=['nombre'])

