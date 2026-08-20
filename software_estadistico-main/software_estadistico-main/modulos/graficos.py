import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

class Graficos:
    def __init__(self, datos):
        self.datos = np.array(datos)
        # Configuración de estilo mejorada
        sns.set_style("whitegrid")
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.dpi'] = 100
        # Crear carpeta salidas si no existe
        os.makedirs('salidas', exist_ok=True)
    
    def histograma(self, titulo="Histograma", bins=10, guardar=False):
        plt.figure(figsize=(10, 6))
        plt.hist(self.datos, bins=bins, edgecolor='black', alpha=0.7, color='skyblue')
        plt.xlabel('Valores', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        if guardar:
            plt.savefig('salidas/histograma.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def boxplot(self, titulo="Diagrama de Caja", guardar=False):
        plt.figure(figsize=(8, 6))
        box = plt.boxplot(self.datos, vert=True, patch_artist=True)
        # Colorear el boxplot
        for patch in box['boxes']:
            patch.set_facecolor('lightblue')
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.ylabel('Valores', fontsize=12)
        plt.grid(True, alpha=0.3)
        if guardar:
            plt.savefig('salidas/boxplot.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_barras(self, titulo="Gráfico de Barras", guardar=False):
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        plt.figure(figsize=(10, 6))
        plt.bar(valores, frecuencias, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.xlabel('Valores', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        # Agregar etiquetas de frecuencia en las barras
        for i, v in enumerate(frecuencias):
            plt.text(valores[i], v + 0.1, str(v), ha='center', va='bottom')
        if guardar:
            plt.savefig('salidas/barras.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_torta(self, titulo="Gráfico de Torta", guardar=False):
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        plt.figure(figsize=(8, 8))
        # Colores automáticos
        colors = plt.cm.Set3(np.linspace(0, 1, len(valores)))
        wedges, texts, autotexts = plt.pie(
            frecuencias, 
            labels=valores, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 11}
        )
        plt.title(titulo, fontsize=14, fontweight='bold')
        if guardar:
            plt.savefig('salidas/torta.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def densidad(self, titulo="Gráfico de Densidad", guardar=False):
        plt.figure(figsize=(10, 6))
        sns.kdeplot(self.datos, fill=True, color='coral', alpha=0.5)
        # Agregar histograma transparente
        plt.hist(self.datos, bins=20, alpha=0.2, color='gray', density=True)
        plt.xlabel('Valores', fontsize=12)
        plt.ylabel('Densidad', fontsize=12)
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        if guardar:
            plt.savefig('salidas/densidad.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def todos_graficos(self, guardar=False):
        """Genera todos los gráficos en una sola figura"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Análisis Estadístico Completo', fontsize=16, fontweight='bold')
        
        # Histograma
        axes[0, 0].hist(self.datos, bins=10, edgecolor='black', alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Histograma')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Boxplot
        axes[0, 1].boxplot(self.datos, patch_artist=True)
        axes[0, 1].set_title('Boxplot')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Barras
        valores, frecuencias = np.unique(self.datos, return_counts=True)
        axes[0, 2].bar(valores, frecuencias, alpha=0.7, color='lightgreen')
        axes[0, 2].set_title('Barras')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Torta
        axes[1, 0].pie(frecuencias, labels=valores, autopct='%1.1f%%', startangle=90)
        axes[1, 0].set_title('Torta')
        
        # Densidad
        sns.kdeplot(self.datos, fill=True, color='coral', alpha=0.5, ax=axes[1, 1])
        axes[1, 1].set_title('Densidad')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Q-Q Plot
        from scipy import stats
        stats.probplot(self.datos, dist="norm", plot=axes[1, 2])
        axes[1, 2].set_title('Q-Q Plot')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if guardar:
            plt.savefig('salidas/todos_graficos.png', dpi=300, bbox_inches='tight')
        plt.show()