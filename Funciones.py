import pandas as pd
import requests
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import math
import json
import pyodbc
from datetime import datetime
from config import engine
from Querys import QueryBase


def obtener_datos_base(users: list[int]):

    query = QueryBase(users)

    result = pd.read_sql(query, engine)

    return result

def calcular_margen(base: pd.DataFrame, difeCostoInter: dict, extra3hs: float, extraGBA: float, precio: float):

    MontosMotoboyNuevos = base[['idUsuario', 'alias', 'idzona', 'EsGBA', 'nombre']].copy()
    
    MontosMotoboyNuevos['PrecioMotoboyHoraSemanaDia'] = base['PrecioMotoboyHoraSemanaDiaZona'] * (1 + difeCostoInter.get('mediodia', 0))
    MontosMotoboyNuevos['PrecioMotoboyHoraFindeDia'] = base['PrecioMotoboyHoraFindeDiaZona'] * (1 + difeCostoInter.get('mediodia', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora3SemanaNoche'] = base['PrecioMotoboyHora3SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora4SemanaNoche'] = base['PrecioMotoboyHora4SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora5SemanaNoche'] = base['PrecioMotoboyHora5SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora6SemanaNoche'] = base['PrecioMotoboyHora6SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora3FindeNoche'] = base['PrecioMotoboyHora3FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora4FindeNoche'] = base['PrecioMotoboyHora4FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora5FindeNoche'] = base['PrecioMotoboyHora5FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0))
    MontosMotoboyNuevos['PrecioMotoboyHora6FindeNoche'] = base['PrecioMotoboyHora6FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0))

    costoTotal = sum(
        base['PrecioMotoboyHoraSemanaDiaZona'] * (1 + difeCostoInter.get('mediodia', 0)) * base['QHora3SemanaDia'] * (1 + extra3hs) +
        base['PrecioMotoboyHoraSemanaDiaZona'] * (1 + difeCostoInter.get('mediodia', 0)) * base['QHora4SemanaDia'] +
        base['PrecioMotoboyHoraFindeDiaZona'] * (1 + difeCostoInter.get('mediodia', 0)) * base['QHora3FindeDia'] * (1 + extra3hs) +
        base['PrecioMotoboyHoraFindeDiaZona'] * (1 + difeCostoInter.get('mediodia', 0)) * base['QHora4FindeDia'] +
        base['PrecioMotoboyHora3SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0)) * base['QHora3SemanaNoche'] +
        base['PrecioMotoboyHora4SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0)) * base['QHora4SemanaNoche'] +
        base['PrecioMotoboyHora5SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0)) * base['QHora5SemanaNoche'] +
        base['PrecioMotoboyHora6SemanaNocheZona'] * (1 + difeCostoInter.get('semana_noche', 0)) * base['QHora6SemanaNoche'] +
        base['PrecioMotoboyHora3FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0)) * base['QHora3FindeNoche'] +
        base['PrecioMotoboyHora4FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0)) * base['QHora4FindeNoche'] +
        base['PrecioMotoboyHora5FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0)) * base['QHora5FindeNoche'] +
        base['PrecioMotoboyHora6FindeNocheZona'] * (1 + difeCostoInter.get('finde_noche', 0)) * base['QHora6FindeNoche']
    )

    IngresoTotal = sum((precio * (1 + extraGBA) if gba else precio) * (hs3sd + hs4sd + hs3fd + hs4fd + hs3sn + hs4sn + hs5sn + hs6sn + hs3fn + hs4fn + hs5fn + hs6fn)
                       for gba, hs3sd, hs4sd, hs3fd, hs4fd, hs3sn, hs4sn, hs5sn, hs6sn, hs3fn, hs4fn, hs5fn, hs6fn
                       in zip(base['EsGBA'], base['QHora3SemanaDia'], base['QHora4SemanaDia'], base['QHora3FindeDia'], base['QHora4FindeDia'],
                              base['QHora3SemanaNoche'], base['QHora4SemanaNoche'], base['QHora5SemanaNoche'], base['QHora6SemanaNoche'],
                              base['QHora3FindeNoche'], base['QHora4FindeNoche'], base['QHora5FindeNoche'], base['QHora6FindeNoche']))

    margen = (IngresoTotal - costoTotal) / IngresoTotal

    return costoTotal, IngresoTotal, margen, MontosMotoboyNuevos

def optimizar_precio(base: pd.DataFrame, difeCostoInter: dict, extra3hs: float, extraGBA: float, margenFinal: float):
    """
    Optimiza el valor de precio para obtener un margen final específico.

    Args:
        base: DataFrame con los datos base
        difeCostoInter: Diccionario con los diferenciales de costo por intermediación
        extraGBA: Porcentaje extra para GBA
        extra3hs: Porcentaje extra para 3 horas
        margenFinal: Margen final deseado

    Returns:
        float: Precio óptimo para alcanzar el margen deseado
    """

    def objetivo(precio):
        _, _, margen, _ = calcular_margen(
            base, difeCostoInter, extra3hs, extraGBA, precio[0])
        return abs(margen - margenFinal)

    # Valor inicial para la optimización
    precio_inicial = [5000]  # Valor inicial más bajo

    # Restricción: precio debe ser positivo
    restricciones = [{'type': 'ineq', 'fun': lambda x: x[0]}]

    # Optimización con límites y más iteraciones
    resultado = minimize(objetivo, precio_inicial,
                         method='SLSQP',
                         constraints=restricciones,
                         # Límites razonables para el precio
                         bounds=[(100, 50000)],
                         options={'maxiter': 1000, 'ftol': 1e-8})

    if resultado.success:
        precio_optimo = resultado.x[0]
        # Verificar que realmente se optimizó
        _, _, margen_obtenido, _ = calcular_margen(
            base, difeCostoInter, extra3hs, extraGBA, precio_optimo)
        print(
            f"Margen objetivo: {margenFinal}, Margen obtenido: {margen_obtenido}, Precio: {precio_optimo}")
        return precio_optimo
    else:
        # Intentar con otro método de optimización
        resultado_alt = minimize(objetivo, precio_inicial,
                                 method='Nelder-Mead',
                                 options={'maxiter': 2000})
        if resultado_alt.success:
            return resultado_alt.x[0]
        else:
            raise ValueError(
                "La optimización no convergió. Intente con otros parámetros iniciales.")

def obtener_montos_motoboy(base: pd.DataFrame, extra3hs: float, transpose: bool = True):

    # Calcular precios para 3 horas
    base["PrecioMotoboyHora3SemanaDia"] = base["PrecioMotoboyHoraSemanaDia"] * (1 + extra3hs)
    base["PrecioMotoboyHora3FindeDia"] = base["PrecioMotoboyHoraFindeDia"] * (1 + extra3hs)
    
    # Reordenar las columnas según el orden especificado
    base = base[['idUsuario', 'alias', 
                 'PrecioMotoboyHora3SemanaDia', 'PrecioMotoboyHoraSemanaDia',
                 'PrecioMotoboyHora3FindeDia', 'PrecioMotoboyHoraFindeDia', 
                 'PrecioMotoboyHora3SemanaNoche', 'PrecioMotoboyHora4SemanaNoche',
                 'PrecioMotoboyHora5SemanaNoche', 'PrecioMotoboyHora6SemanaNoche',
                 'PrecioMotoboyHora3FindeNoche', 'PrecioMotoboyHora4FindeNoche',
                 'PrecioMotoboyHora5FindeNoche', 'PrecioMotoboyHora6FindeNoche']]
                 
    # Redondear todas las columnas que comienzan con "Precio" al número entero más cercano
    columnas_precio = [col for col in base.columns if col.startswith('Precio')]
    base.loc[:, columnas_precio] = base.loc[:, columnas_precio].round(0)

    if transpose:
        # Crear identificador combinado de usuario-alias
        base['id_alias'] = base['idUsuario'].astype(str) + '-' + base['alias']
        
        # Seleccionar solo las columnas de precio
        df_precios = base[columnas_precio]
        
        # Transponer el dataframe
        df_transpuesto = df_precios.transpose()
        
        # Renombrar las columnas usando id_alias
        df_transpuesto.columns = base['id_alias']
        
        # Resetear el índice y renombrar la columna de índice
        df_transpuesto = df_transpuesto.reset_index()
        df_transpuesto = df_transpuesto.rename(columns={'index': 'TipoPrecio'})
        
        # Reemplazar el dataframe original
        base = df_transpuesto

    # Obtener el nombre del DataFrame original
    nombre_df = [var_name for var_name, var_val in globals().items() if isinstance(var_val, pd.DataFrame) and var_val is base][0]
    
    # Crear el directorio exports si no existe
    if not os.path.exists('exports'):
        os.makedirs('exports')
        
    # Exportar a Excel
    base.to_excel(f'exports/MontosMotoboy_{nombre_df}.xlsx', index=False)
    return base
