import pandas as pd
import numpy as np

class TablaFrecuencia:
    def __init__(self, datos):
        self.datos = np.array(datos)
        
    def tabla_simple(self):
        """Tabla de frecuencia para datos no agrupados"""
        valores = np.unique(self.datos)
        frecuencias = [np.sum(self.datos == v) for v in valores]
        frec_rel = [f/len(self.datos) for f in frecuencias]
        frec_acum = np.cumsum(frecuencias)
        frec_rel_acum = np.cumsum(frec_rel)
        
        return pd.DataFrame({
            'Valor': valores,
            'f': frecuencias,
            'fr': frec_rel,
            'F': frec_acum,
            'Fr': frec_rel_acum
        })
    
    def tabla_agrupada(self, n_clases=None, amplitud=None):
        """Tabla de frecuencia para datos agrupados"""
        datos = self.datos
        n = len(datos)
        
        # Regla de Sturges para número de clases
        if n_clases is None:
            n_clases = int(1 + 3.322 * np.log10(n))
        
        # Calcular amplitud
        if amplitud is None:
            rango = np.max(datos) - np.min(datos)
            amplitud = rango / n_clases
        
        # Crear intervalos
        min_val = np.min(datos)
        limites = [min_val + i * amplitud for i in range(n_clases + 1)]
        
        # Calcular frecuencias
        frecuencias = []
        marcas_clase = []
        
        for i in range(n_clases):
            li = limites[i]
            ls = limites[i + 1]
            marca = (li + ls) / 2
            marcas_clase.append(marca)
            
            if i == n_clases - 1:
                # Último intervalo incluye el límite superior
                freq = np.sum((datos >= li) & (datos <= ls))
            else:
                freq = np.sum((datos >= li) & (datos < ls))
            frecuencias.append(freq)
        
        # Construir DataFrame
        intervalos = [f"[{limites[i]:.2f} - {limites[i+1]:.2f})" 
                      for i in range(n_clases)]
        
        frec_rel = [f/n for f in frecuencias]
        frec_acum = np.cumsum(frecuencias)
        frec_rel_acum = np.cumsum(frec_rel)
        
        return pd.DataFrame({
            'Intervalo': intervalos,
            'Marca': marcas_clase,
            'f': frecuencias,
            'fr': frec_rel,
            'F': frec_acum,
            'Fr': frec_rel_acum
        })