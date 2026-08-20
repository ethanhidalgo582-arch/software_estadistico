import pandas as pd
import numpy as np

def cargar_datos(archivo):
    """Carga datos desde CSV o Excel"""
    if archivo.endswith('.csv'):
        return pd.read_csv(archivo)
    elif archivo.endswith(('.xlsx', '.xls')):
        return pd.read_excel(archivo)
    else:
        raise ValueError("Formato no soportado")

def validar_datos(datos, columna):
    """Valida que los datos sean numéricos"""
    if columna not in datos.columns:
        raise ValueError(f"Columna {columna} no encontrada")
    
    serie = datos[columna].dropna()
    if not pd.api.types.is_numeric_dtype(serie):
        raise ValueError("Los datos deben ser numéricos")
    return serie