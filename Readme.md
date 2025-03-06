# README para el Proyecto de Optimización de Precios

## Descripción

Este proyecto tiene como objetivo optimizar los precios de productos para diferentes clientes utilizando datos de una base de datos o archivos CSV. El código está diseñado para calcular márgenes y montos a cargar para un servicio de entrega, específicamente para un cliente de comida.

## Estructura del Código

El archivo principal es `test.ipynb`, que contiene las siguientes secciones clave:

1. **Importación de Módulos**:
   - Se importan funciones necesarias desde otros archivos (`Funciones.py` y `Querys.py`) y se cargan configuraciones desde `config.py`.

2. **Carga de Datos**:
   - Se puede cargar datos desde una base de datos utilizando la función `obtener_datos_base()`, o desde archivos CSV si no se tiene acceso a la base de datos.
   - Se debe descomentar la línea correspondiente al cliente que se desea utilizar.

3. **Definición de Parámetros**:
   - Se definen parámetros necesarios para el cálculo de precios, como diferencias de costo y márgenes.

4. **Optimización de Precios**:
   - Se utiliza la función `optimizar_precio()` para calcular el precio optimizado basado en los datos cargados y los parámetros definidos.

5. **Cálculo de Márgenes**:
   - La función `calcular_margen()` se utiliza para calcular el costo total, ingreso total, margen y montos a cargar para el servicio de entrega.

6. **Exportación de Resultados**:
   - Los montos a cargar se guardan en un archivo Excel en una carpeta llamada `exports`. Si la carpeta no existe, se crea automáticamente.

## Requisitos

- Python 3.x
- Bibliotecas: `pandas`, `Funciones`, `Querys`, `config`

## Uso

1. Asegúrate de tener acceso a la base de datos o de haber generado los archivos CSV necesarios.
2. Descomenta la línea correspondiente al cliente que deseas utilizar.
3. Ejecuta las celdas en `test.ipynb` para cargar los datos, optimizar precios y exportar los resultados.

## Notas

- Asegúrate de manejar adecuadamente las advertencias y errores que puedan surgir, como `SettingWithCopyWarning` o `IndexError`.
- Este proyecto está diseñado para ser flexible y puede adaptarse a diferentes clientes y configuraciones de precios.
