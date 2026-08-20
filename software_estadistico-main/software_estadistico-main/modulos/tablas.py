import pandas as pd
import numpy as np

class TablaFrecuencia:
    def __init__(self, datos):
        # Asegurar que los datos sean numéricos
        self.datos = np.array(datos, dtype=float)
        
    def tabla_simple(self):
        """
        Tabla de frecuencia para datos no agrupados con:
        - x: valores
        - f: frecuencia absoluta
        - %: porcentaje
        - F ↑: frecuencia absoluta ascendente (acumulada)
        - % ↑: porcentaje acumulado ascendente
        - F ↓: frecuencia absoluta descendente
        - % ↓: porcentaje acumulado descendente
        """
        valores = np.unique(self.datos)
        n = len(self.datos)
        
        # Ordenar valores
        valores = np.sort(valores)
        
        # Calcular frecuencias absolutas
        frecuencias = [np.sum(self.datos == v) for v in valores]
        
        # Porcentajes
        porcentajes = [(f / n) * 100 for f in frecuencias]
        
        # Frecuencias absolutas ascendentes (acumuladas)
        frec_acum_asc = np.cumsum(frecuencias)
        porcentajes_acum_asc = np.cumsum(porcentajes)
        
        # Frecuencias absolutas descendentes
        frec_acum_desc = []
        porcentajes_acum_desc = []
        
        for i in range(len(frecuencias)):
            # Suma desde el final hasta la posición i
            desc = sum(frecuencias[i:])
            frec_acum_desc.append(desc)
            porcentajes_acum_desc.append((desc / n) * 100)
        
        # Crear DataFrame con las columnas solicitadas
        df = pd.DataFrame({
            'x': valores,
            'f': frecuencias,
            '%': [round(x, 2) for x in porcentajes],
            'F ↑': frec_acum_asc,
            '% ↑': [round(x, 2) for x in porcentajes_acum_asc],
            'F ↓': frec_acum_desc,
            '% ↓': [round(x, 2) for x in porcentajes_acum_desc]
        })
        
        # Agregar fila de totales (solo f y %)
        total_row = pd.DataFrame({
            'x': ['TOTAL'],
            'f': [sum(frecuencias)],
            '%': [100.0],
            'F ↑': ['-'],
            '% ↑': ['-'],
            'F ↓': ['-'],
            '% ↓': ['-']
        })
        
        return pd.concat([df, total_row], ignore_index=True)
    
    def tabla_agrupada(self, n_clases=None, amplitud=None):
        """
        Tabla de frecuencia para datos agrupados con:
        - Límite real inferior (LRI)
        - Límite real superior (LRS)
        - Marca de clase (Mc)
        - f: frecuencia absoluta
        - %: porcentaje
        - F ↑: frecuencia absoluta ascendente
        - % ↑: porcentaje acumulado ascendente
        - F ↓: frecuencia absoluta descendente
        - % ↓: porcentaje acumulado descendente
        """
        datos = self.datos
        n = len(datos)
        
        if n == 0:
            return pd.DataFrame()
        
        # Regla de Sturges para número de clases
        if n_clases is None:
            n_clases = max(2, int(1 + 3.322 * np.log10(n)))
            # Limitar número de clases
            n_clases = min(n_clases, 20)
        
        # Calcular amplitud
        rango_datos = np.max(datos) - np.min(datos)
        if rango_datos == 0:
            # Todos los datos son iguales
            n_clases = 1
            amplitud = 1
        else:
            if amplitud is None:
                amplitud = rango_datos / n_clases
                # Redondear a número bonito
                amplitud = self._redondear_amplitud(amplitud)
        
        # Crear intervalos
        min_val = np.min(datos)
        limites = [min_val + i * amplitud for i in range(n_clases + 1)]
        
        # Calcular frecuencias
        frecuencias = []
        limites_reales_inf = []
        limites_reales_sup = []
        marcas_clase = []
        intervalos = []
        
        for i in range(n_clases):
            li = limites[i]
            ls = limites[i + 1]
            
            # Calcular límites reales (restar/sumar 0.5 si son enteros)
            # Si los datos son enteros, usar ±0.5, si no, usar la mitad de la precisión
            if all(x.is_integer() for x in datos):
                lri = li - 0.5
                lrs = ls + 0.5
            else:
                # Para datos decimales, usar la mitad de la diferencia
                precision = 0.005  # Para 2 decimales
                lri = li - precision
                lrs = ls + precision
            
            limites_reales_inf.append(lri)
            limites_reales_sup.append(lrs)
            
            marca = (li + ls) / 2
            marcas_clase.append(marca)
            
            intervalo = f"[{li:.2f} - {ls:.2f}]"
            intervalos.append(intervalo)
            
            if i == n_clases - 1:
                # Último intervalo incluye el límite superior
                freq = np.sum((datos >= li) & (datos <= ls))
            else:
                freq = np.sum((datos >= li) & (datos < ls))
            frecuencias.append(freq)
        
        # Porcentajes
        porcentajes = [(f / n) * 100 for f in frecuencias]
        
        # Frecuencias absolutas ascendentes (acumuladas)
        frec_acum_asc = np.cumsum(frecuencias)
        porcentajes_acum_asc = np.cumsum(porcentajes)
        
        # Frecuencias absolutas descendentes
        frec_acum_desc = []
        porcentajes_acum_desc = []
        
        for i in range(len(frecuencias)):
            desc = sum(frecuencias[i:])
            frec_acum_desc.append(desc)
            porcentajes_acum_desc.append((desc / n) * 100)
        
        # Crear DataFrame con todas las columnas
        df = pd.DataFrame({
            'LRI': [round(x, 2) for x in limites_reales_inf],
            'LRS': [round(x, 2) for x in limites_reales_sup],
            'Mc': [round(x, 2) for x in marcas_clase],
            'f': frecuencias,
            '%': [round(x, 2) for x in porcentajes],
            'F ↑': frec_acum_asc,
            '% ↑': [round(x, 2) for x in porcentajes_acum_asc],
            'F ↓': frec_acum_desc,
            '% ↓': [round(x, 2) for x in porcentajes_acum_desc]
        })
        
        # Agregar fila de totales (solo f y %)
        total_row = pd.DataFrame({
            'LRI': ['-'],
            'LRS': ['-'],
            'Mc': ['-'],
            'f': [sum(frecuencias)],
            '%': [100.0],
            'F ↑': ['-'],
            '% ↑': ['-'],
            'F ↓': ['-'],
            '% ↓': ['-']
        })
        
        return pd.concat([df, total_row], ignore_index=True)
    
    def _redondear_amplitud(self, amplitud):
        """Redondea la amplitud a un número más manejable"""
        if amplitud <= 0:
            return 1
        elif amplitud < 1:
            return round(amplitud, 2)
        elif amplitud < 10:
            return round(amplitud, 1)
        else:
            return round(amplitud)