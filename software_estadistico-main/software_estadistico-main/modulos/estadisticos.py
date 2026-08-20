import numpy as np
from scipy import stats
import pandas as pd

class Estadisticos:
    def __init__(self, datos):
        self.datos = np.array(datos)
        
    def media(self):
        return np.mean(self.datos)
    
    def mediana(self):
        return np.median(self.datos)
    
    def moda(self):
        """Calcula la moda de los datos"""
        try:
            # Versión moderna de scipy
            moda_resultado = stats.mode(self.datos)
            # Si es un objeto con atributos
            if hasattr(moda_resultado, 'mode'):
                return moda_resultado.mode[0]
            else:
                return moda_resultado[0][0]
        except:
            # Si falla, usar método alternativo
            from collections import Counter
            contador = Counter(self.datos)
            return max(contador.items(), key=lambda x: x[1])[0]
    
    def varianza(self):
        return np.var(self.datos, ddof=1)  # Varianza muestral
    
    def desviacion_estandar(self):
        return np.std(self.datos, ddof=1)
    
    def rango(self):
        return np.max(self.datos) - np.min(self.datos)
    
    def cuartiles(self):
        return np.percentile(self.datos, [25, 50, 75])
    
    def rango_intercuartil(self):
        q1, q3 = self.cuartiles()[0], self.cuartiles()[2]
        return q3 - q1
    
    def coeficiente_variacion(self):
        media_val = self.media()
        if media_val == 0:
            return 0
        return (self.desviacion_estandar() / media_val) * 100
    
    def asimetria(self):
        return stats.skew(self.datos)
    
    def curtosis(self):
        return stats.kurtosis(self.datos)
    
    def resumen_completo(self):
        """Devuelve diccionario con todos los estadísticos"""
        try:
            moda_val = self.moda()
        except:
            moda_val = "No disponible"
            
        return {
            'Media': self.media(),
            'Mediana': self.mediana(),
            'Moda': moda_val,
            'Varianza': self.varianza(),
            'Desviación Estándar': self.desviacion_estandar(),
            'Rango': self.rango(),
            'Q1': self.cuartiles()[0],
            'Q3': self.cuartiles()[2],
            'Rango Intercuartil': self.rango_intercuartil(),
            'Coef. Variación (%)': self.coeficiente_variacion(),
            'Asimetría': self.asimetria(),
            'Curtosis': self.curtosis()
        }