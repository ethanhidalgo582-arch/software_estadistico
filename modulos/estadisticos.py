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
        # Para datos agrupados
        return stats.mode(self.datos)[0][0]
    
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
        return (self.desviacion_estandar() / self.media()) * 100
    
    def asimetria(self):
        return stats.skew(self.datos)
    
    def curtosis(self):
        return stats.kurtosis(self.datos)
    
    def resumen_completo(self):
        """Devuelve diccionario con todos los estadísticos"""
        return {
            'Media': self.media(),
            'Mediana': self.mediana(),
            'Moda': self.moda(),
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