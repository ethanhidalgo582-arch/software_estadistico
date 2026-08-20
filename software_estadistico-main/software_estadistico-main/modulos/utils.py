import pandas as pd
import numpy as np
import os
import csv

def detectar_separador(archivo):
    """Detecta automáticamente el separador del archivo CSV"""
    with open(archivo, 'r', encoding='utf-8') as f:
        primera_linea = f.readline()
        
        # Contar ocurrencias de posibles separadores
        separadores = {
            ',': primera_linea.count(','),
            ';': primera_linea.count(';'),
            '\t': primera_linea.count('\t'),
            '|': primera_linea.count('|')
        }
        
        # Seleccionar el separador con más ocurrencias
        separador = max(separadores, key=separadores.get)
        
        # Si no hay separador, usar coma por defecto
        if separadores[separador] == 0:
            separador = ','
        
        return separador

def cargar_datos(archivo):
    """Carga datos desde CSV o Excel con detección automática de separadores"""
    try:
        if archivo.endswith('.csv'):
            # Detectar separador automáticamente
            separador = detectar_separador(archivo)
            
            # Intentar cargar con el separador detectado
            df = pd.read_csv(archivo, sep=separador, encoding='utf-8')
            
            # Si solo tiene una columna y hay más columnas potenciales, intentar con otro separador
            if df.shape[1] == 1:
                # Probar con otros separadores comunes
                for sep in [',', ';', '\t', '|']:
                    if sep != separador:
                        try:
                            df_test = pd.read_csv(archivo, sep=sep, encoding='utf-8')
                            if df_test.shape[1] > 1:
                                df = df_test
                                break
                        except:
                            continue
            
            return df
            
        elif archivo.endswith(('.xlsx', '.xls')):
            return pd.read_excel(archivo)
        else:
            raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")
            
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Archivo no encontrado: {archivo}")
    except Exception as e:
        raise Exception(f"❌ Error al cargar archivo: {e}")

def validar_datos(datos, columna):
    """Valida que los datos sean numéricos"""
    if columna not in datos.columns:
        raise ValueError(f"❌ Columna '{columna}' no encontrada")
    
    # Limpiar datos - convertir a numérico, reemplazar no numéricos con NaN
    serie = pd.to_numeric(datos[columna], errors='coerce')
    serie = serie.dropna()
    
    if len(serie) == 0:
        raise ValueError("❌ No hay datos numéricos válidos en la columna")
    
    return serie

def listar_archivos():
    """Lista archivos disponibles en el directorio actual"""
    archivos = []
    for file in os.listdir('.'):
        if file.endswith(('.csv', '.xlsx', '.xls')):
            archivos.append(file)
    return sorted(archivos)