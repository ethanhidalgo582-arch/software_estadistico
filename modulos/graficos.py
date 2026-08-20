import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Graficos:
    def __init__(self, datos):
        self.datos = np.array(datos)
        sns.set_style("whitegrid")
    
    def histograma(self, titulo="Histograma", bins=10, guardar=False):
        plt.figure(figsize=(10, 6))
        plt.hist(self.datos, bins=bins, edgecolor='black', alpha=0.7)
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.title(titulo)
        if guardar:
            plt.savefig('salidas/histograma.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def boxplot(self, titulo="Diagrama de Caja", guardar=False):
        plt.figure(figsize=(8, 6))
        plt.boxplot(self.datos, vert=True, patch_artist=True)
        plt.title(titulo)
        plt.ylabel('Valores')
        if guardar:
            plt.savefig('salidas/boxplot.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_barras(self, titulo="Gráfico de Barras", guardar=False):
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        plt.figure(figsize=(10, 6))
        plt.bar(valores, frecuencias, alpha=0.7)
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.title(titulo)
        if guardar:
            plt.savefig('salidas/barras.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_torta(self, titulo="Gráfico de Torta", guardar=False):
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        plt.figure(figsize=(8, 8))
        plt.pie(frecuencias, labels=valores, autopct='%1.1f%%', startangle=90)
        plt.title(titulo)
        if guardar:
            plt.savefig('salidas/torta.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def densidad(self, titulo="Densidad", guardar=False):
        plt.figure(figsize=(10, 6))
        sns.kdeplot(self.datos, fill=True)
        plt.xlabel('Valores')
        plt.ylabel('Densidad')
        plt.title(titulo)
        if guardar:
            plt.savefig('salidas/densidad.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def todos_graficos(self, guardar=False):
        """Genera todos los gráficos en una sola figura"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Histograma
        axes[0, 0].hist(self.datos, bins=10, edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Histograma')
        
        # Boxplot
        axes[0, 1].boxplot(self.datos)
        axes[0, 1].set_title('Boxplot')
        
        # Barras
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        axes[0, 2].bar(valores, frecuencias, alpha=0.7)
        axes[0, 2].set_title('Barras')
        
        # Torta
        axes[1, 0].pie(frecuencias, labels=valores, autopct='%1.1f%%')
        axes[1, 0].set_title('Torta')
        
        # Densidad
        sns.kdeplot(self.datos, fill=True, ax=axes[1, 1])
        axes[1, 1].set_title('Densidad')
        
        # Q-Q Plot
        from scipy import stats
        stats.probplot(self.datos, dist="norm", plot=axes[1, 2])
        axes[1, 2].set_title('Q-Q Plot')
        
        plt.tight_layout()
        if guardar:
            plt.savefig('salidas/todos_graficos.png', dpi=300, bbox_inches='tight')
        plt.show()