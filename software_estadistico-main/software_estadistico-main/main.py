from modulos.utils import cargar_datos, validar_datos, listar_archivos
from modulos.estadisticos import Estadisticos
from modulos.tablas import TablaFrecuencia
from modulos.graficos import Graficos
import pandas as pd
import numpy as np  # <-- CORREGIDO: Importar numpy
import os
import sys

def generar_reporte_completo(datos, nombre_datos="Datos"):
    """Genera reporte completo con todos los análisis"""
    os.makedirs('salidas', exist_ok=True)
    
    print(f"\n📄 GENERANDO REPORTE COMPLETO - {nombre_datos}")
    print("="*50)
    
    try:
        # Estadísticos
        est = Estadisticos(datos)
        resumen = est.resumen_completo()
        
        # Tablas
        tabla = TablaFrecuencia(datos)
        tab_simple = tabla.tabla_simple()
        tab_agrupada = tabla.tabla_agrupada()
        
        # Exportar a Excel
        with pd.ExcelWriter('salidas/reporte_completo.xlsx') as writer:
            # Hoja de estadísticos
            df_resumen = pd.DataFrame([resumen]).T
            df_resumen.columns = ['Valor']
            df_resumen.to_excel(writer, sheet_name='Estadísticos')
            
            # Hojas de tablas
            tab_simple.to_excel(writer, sheet_name='Tabla Simple', index=False)
            tab_agrupada.to_excel(writer, sheet_name='Tabla Agrupada', index=False)
        
        # Guardar gráficos
        graficos = Graficos(datos)
        graficos.todos_graficos(guardar=True)
        
        print("✅ Reporte generado exitosamente en carpeta 'salidas/'")
        print("   📄 reporte_completo.xlsx")
        print("   📊 todos_graficos.png")
        
    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")

def menu_principal():
    print("\n" + "="*50)
    print("📊 SOFTWARE ESTADÍSTICO v1.0")
    print("="*50)
    print("1. Cargar datos desde archivo")
    print("2. Ingresar datos manualmente")
    print("3. Ver datos cargados")
    print("4. Tablas de frecuencia")
    print("5. Estadísticos descriptivos")
    print("6. Gráficos")
    print("7. Reporte completo")
    print("8. Ver archivos disponibles")
    print("9. Salir")
    print("="*50)

def main():
    datos = None
    nombre_datos = "No cargados"
    
    while True:
        menu_principal()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            # Mostrar archivos disponibles
            archivos = listar_archivos()
            if archivos:
                print("\n📁 Archivos disponibles:")
                for i, archivo in enumerate(archivos, 1):
                    print(f"   {i}. {archivo}")
                print("   0. Ingresar ruta manualmente")
                
                try:
                    seleccion = int(input("\nSeleccione un archivo (0 para manual): "))
                    if seleccion > 0 and seleccion <= len(archivos):
                        archivo = archivos[seleccion - 1]
                    else:
                        archivo = input("Ingrese ruta del archivo: ")
                except:
                    archivo = input("Ingrese ruta del archivo: ")
            else:
                archivo = input("Ingrese ruta del archivo (ej: datos.csv): ")
            
            try:
                # Verificar si el archivo existe
                if not os.path.exists(archivo):
                    print(f"❌ Archivo no encontrado: {archivo}")
                    print("   Asegúrate de que el archivo esté en la carpeta correcta")
                    continue
                
                df = cargar_datos(archivo)
                print(f"\n✅ Archivo cargado: {archivo}")
                print(f"   Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
                print("\n📋 Columnas disponibles:", list(df.columns))
                print("\nPrimeras 5 filas:")
                print(df.head())
                
                columna = input("\nSeleccione columna para analizar: ")
                serie = validar_datos(df, columna)
                datos = serie.values
                nombre_datos = f"{archivo} - {columna}"
                print(f"\n✅ Datos cargados: {len(datos)} registros")
                print(f"   Rango: {min(datos):.2f} - {max(datos):.2f}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                print("   Verifica que el archivo tenga el formato correcto")
        
        elif opcion == "2":
            entrada = input("Ingrese datos separados por coma (ej: 1,2,3,4): ")
            try:
                datos = [float(x.strip()) for x in entrada.split(',') if x.strip()]
                if not datos:
                    print("❌ No se ingresaron datos válidos")
                    continue
                nombre_datos = "Datos manuales"
                print(f"\n✅ Datos ingresados: {len(datos)} registros")
                print(f"   Rango: {min(datos):.2f} - {max(datos):.2f}")
            except ValueError:
                print("❌ Error: Ingrese números válidos separados por coma")
        
        elif opcion == "3":
            if datos is not None:
                print(f"\n📋 DATOS CARGADOS: {nombre_datos}")
                print("-"*40)
                print(f"Cantidad: {len(datos)}")
                print(f"Mínimo: {min(datos):.2f}")
                print(f"Máximo: {max(datos):.2f}")
                print(f"Promedio: {sum(datos)/len(datos):.2f}")
                print(f"Suma: {sum(datos):.2f}")
                print(f"Desviación estándar: {np.std(datos, ddof=1):.2f}")
                print("\n📊 Distribución:")
                print(f"   Primeros 10 valores: {datos[:10]}")
                
                # Mostrar frecuencia de valores únicos si son pocos
                valores_unicos = np.unique(datos)
                if len(valores_unicos) <= 10:
                    print("\n   Valores únicos:")
                    for val in valores_unicos:
                        count = np.sum(datos == val)
                        print(f"      {val}: {count} veces")
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "4":
            if datos is not None:
                tabla = TablaFrecuencia(datos)
                print("\n--- TABLAS DE FRECUENCIA ---")
                print("1. Simple (no agrupada)")
                print("2. Agrupada")
                print("3. Ambas")
                subop = input("Seleccione: ")
                
                if subop in ["1", "3"]:
                    print("\n📊 TABLA DE FRECUENCIA SIMPLE")
                    print("-"*60)
                    print(tabla.tabla_simple().to_string(index=False))
                
                if subop in ["2", "3"]:
                    n_clases = input("\nNúmero de clases (Enter para automático): ")
                    n_clases = int(n_clases) if n_clases else None
                    print("\n📊 TABLA DE FRECUENCIA AGRUPADA")
                    print("-"*60)
                    print(tabla.tabla_agrupada(n_clases=n_clases).to_string(index=False))
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "5":
            if datos is not None:
                est = Estadisticos(datos)
                resumen = est.resumen_completo()
                print(f"\n📊 ESTADÍSTICOS DESCRIPTIVOS - {nombre_datos}")
                print("="*50)
                for key, value in resumen.items():
                    if isinstance(value, float):
                        print(f"{key:25}: {value:>12.4f}")
                    else:
                        print(f"{key:25}: {value:>12}")
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "6":
            if datos is not None:
                graficos = Graficos(datos)
                print("\n📈 GRÁFICOS DISPONIBLES")
                print("1. Histograma")
                print("2. Boxplot")
                print("3. Gráfico de Barras")
                print("4. Gráfico de Torta")
                print("5. Densidad")
                print("6. Todos los gráficos")
                subop = input("Seleccione: ")
                
                guardar = input("¿Guardar imagen? (s/n): ").lower() == 's'
                
                opciones = {
                    "1": graficos.histograma,
                    "2": graficos.boxplot,
                    "3": graficos.grafico_barras,
                    "4": graficos.grafico_torta,
                    "5": graficos.densidad,
                    "6": graficos.todos_graficos
                }
                
                if subop in opciones:
                    # Llamar a la función con el parámetro guardar
                    if subop == "6":
                        opciones[subop](guardar=guardar)
                    else:
                        opciones[subop](guardar=guardar)
                else:
                    print("❌ Opción inválida")
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "7":
            if datos is not None:
                generar_reporte_completo(datos, nombre_datos)
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "8":
            print("\n📁 ARCHIVOS DISPONIBLES")
            archivos = listar_archivos()
            if archivos:
                print("\n".join([f"   - {a}" for a in archivos]))
            else:
                print("   No se encontraron archivos .csv, .xlsx o .xls")
            
        elif opcion == "9":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    print("🚀 Iniciando Software Estadístico...")
    print("💡 Asegúrate de tener los archivos en la carpeta correcta")
    print("   Para ayuda, selecciona opción 8 para ver archivos disponibles")
    main()