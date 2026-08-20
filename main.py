from modulos.utils import cargar_datos, validar_datos
from modulos.estadisticos import Estadisticos
from modulos.tablas import TablaFrecuencia
from modulos.graficos import Graficos
import pandas as pd
import os

def menu_principal():
    print("\n" + "="*50)
    print("📊 SOFTWARE ESTADÍSTICO")
    print("="*50)
    print("1. Cargar datos desde archivo")
    print("2. Ingresar datos manualmente")
    print("3. Ver datos cargados")
    print("4. Tablas de frecuencia")
    print("5. Estadísticos descriptivos")
    print("6. Gráficos")
    print("7. Reporte completo")
    print("8. Salir")
    print("="*50)

def main():
    datos = None
    columna = None
    
    while True:
        menu_principal()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            archivo = input("Ingrese ruta del archivo (csv/excel): ")
            try:
                df = cargar_datos(archivo)
                print("\nColumnas disponibles:", list(df.columns))
                columna = input("Seleccione columna para analizar: ")
                serie = validar_datos(df, columna)
                datos = serie.values
                print(f"\n✅ Datos cargados: {len(datos)} registros")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif opcion == "2":
            entrada = input("Ingrese datos separados por coma (ej: 1,2,3,4): ")
            try:
                datos = [float(x.strip()) for x in entrada.split(',')]
                print(f"\n✅ Datos ingresados: {len(datos)} registros")
            except:
                print("❌ Error: Ingrese números válidos")
        
        elif opcion == "3":
            if datos is not None:
                print("\n📋 Datos cargados:")
                print(f"Cantidad: {len(datos)}")
                print(f"Mínimo: {min(datos):.2f}")
                print(f"Máximo: {max(datos):.2f}")
                print(f"Suma: {sum(datos):.2f}")
                print("\nPrimeros 10 valores:", datos[:10])
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "4":
            if datos is not None:
                tabla = TablaFrecuencia(datos)
                print("\n--- TABLA DE FRECUENCIA ---")
                print("1. Simple (no agrupada)")
                print("2. Agrupada")
                subop = input("Seleccione: ")
                
                if subop == "1":
                    print("\n", tabla.tabla_simple())
                elif subop == "2":
                    n_clases = input("Número de clases (Enter para automático): ")
                    n_clases = int(n_clases) if n_clases else None
                    print("\n", tabla.tabla_agrupada(n_clases=n_clases))
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "5":
            if datos is not None:
                est = Estadisticos(datos)
                resumen = est.resumen_completo()
                print("\n📊 ESTADÍSTICOS DESCRIPTIVOS")
                print("-"*40)
                for key, value in resumen.items():
                    print(f"{key:25}: {value:.4f}")
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "6":
            if datos is not None:
                graficos = Graficos(datos)
                print("\n📈 GRÁFICOS")
                print("1. Histograma")
                print("2. Boxplot")
                print("3. Gráfico de Barras")
                print("4. Gráfico de Torta")
                print("5. Densidad")
                print("6. Todos los gráficos")
                subop = input("Seleccione: ")
                
                guardar = input("¿Guardar imagen? (s/n): ").lower() == 's'
                
                if subop == "1":
                    graficos.histograma(guardar=guardar)
                elif subop == "2":
                    graficos.boxplot(guardar=guardar)
                elif subop == "3":
                    graficos.grafico_barras(guardar=guardar)
                elif subop == "4":
                    graficos.grafico_torta(guardar=guardar)
                elif subop == "5":
                    graficos.densidad(guardar=guardar)
                elif subop == "6":
                    graficos.todos_graficos(guardar=guardar)
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "7":
            if datos is not None:
                generar_reporte_completo(datos)
            else:
                print("❌ No hay datos cargados")
        
        elif opcion == "8":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")

def generar_reporte_completo(datos):
    """Genera reporte completo con todos los análisis"""
    os.makedirs('salidas', exist_ok=True)
    
    print("\n📄 GENERANDO REPORTE COMPLETO...")
    
    # Estadísticos
    est = Estadisticos(datos)
    resumen = est.resumen_completo()
    
    # Tablas
    tabla = TablaFrecuencia(datos)
    tab_simple = tabla.tabla_simple()
    tab_agrupada = tabla.tabla_agrupada()
    
    # Gráficos
    graficos = Graficos(datos)
    
    # Exportar a Excel
    with pd.ExcelWriter('salidas/reporte_completo.xlsx') as writer:
        # Hoja de estadísticos
        pd.DataFrame([resumen]).T.to_excel(writer, sheet_name='Estadísticos')
        
        # Hojas de tablas
        tab_simple.to_excel(writer, sheet_name='Tabla Simple', index=False)
        tab_agrupada.to_excel(writer, sheet_name='Tabla Agrupada', index=False)
    
    # Guardar gráficos
    graficos.todos_graficos(guardar=True)
    
    print("✅ Reporte generado en carpeta 'salidas/'")
    print("   - reporte_completo.xlsx")
    print("   - todos_graficos.png")

if __name__ == "__main__":
    main()