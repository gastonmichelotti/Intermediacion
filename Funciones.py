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


def calcular_margen(base: pd.DataFrame, difeCostoIntermediacion: float, extra3hs: float, extraGBA: float, precio: float):

    costoTotal = sum(
        base['PrecioMotoboyHoraSemanaDiaZona'] * (1 + difeCostoIntermediacion) * base['QHora3SemanaDia'] * (1 + extra3hs) +
        base['PrecioMotoboyHoraSemanaDiaZona'] * (1 + difeCostoIntermediacion) * base['QHora4SemanaDia'] +
        base['PrecioMotoboyHoraFindeDiaZona'] * (1 + difeCostoIntermediacion) * base['QHora3FindeDia'] * (1 + extra3hs) +
        base['PrecioMotoboyHoraFindeDiaZona'] * (1 + difeCostoIntermediacion) * base['QHora4FindeDia'] +
        base['PrecioMotoboyHora3SemanaNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora3SemanaNoche'] +
        base['PrecioMotoboyHora4SemanaNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora4SemanaNoche'] +
        base['PrecioMotoboyHora5SemanaNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora5SemanaNoche'] +
        base['PrecioMotoboyHora6SemanaNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora6SemanaNoche'] +
        base['PrecioMotoboyHora3FindeNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora3FindeNoche'] +
        base['PrecioMotoboyHora4FindeNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora4FindeNoche'] +
        base['PrecioMotoboyHora5FindeNocheZona'] * (1 + difeCostoIntermediacion) * base['QHora5FindeNoche'] +
        base['PrecioMotoboyHora6FindeNocheZona'] *
        (1 + difeCostoIntermediacion) * base['QHora6FindeNoche']
    )

    IngresoTotal = sum((precio * (1 + extraGBA) if gba else precio) * (hs3sd + hs4sd + hs3fd + hs4fd + hs3sn + hs4sn + hs5sn + hs6sn + hs3fn + hs4fn + hs5fn + hs6fn)
                       for gba, hs3sd, hs4sd, hs3fd, hs4fd, hs3sn, hs4sn, hs5sn, hs6sn, hs3fn, hs4fn, hs5fn, hs6fn
                       in zip(base['EsGBA'], base['QHora3SemanaDia'], base['QHora4SemanaDia'], base['QHora3FindeDia'], base['QHora4FindeDia'],
                              base['QHora3SemanaNoche'], base['QHora4SemanaNoche'], base['QHora5SemanaNoche'], base['QHora6SemanaNoche'],
                              base['QHora3FindeNoche'], base['QHora4FindeNoche'], base['QHora5FindeNoche'], base['QHora6FindeNoche']))

    margen = (IngresoTotal - costoTotal) / IngresoTotal

    return costoTotal, IngresoTotal, margen


def optimizar_precio(base: pd.DataFrame, difeCostoIntermediacion: float, extra3hs: float, extraGBA: float, margenFinal: float):
    """
    Optimiza el valor de precio para obtener un margen final específico.

    Args:
        base: DataFrame con los datos base
        difeCostoIntermediacion: Diferencial de costo de intermediación
        extraGBA: Porcentaje extra para GBA
        extra3hs: Porcentaje extra para 3 horas
        margenFinal: Margen final deseado

    Returns:
        float: Precio óptimo para alcanzar el margen deseado
    """

    def objetivo(precio):
        _, _, margen = calcular_margen(
            base, difeCostoIntermediacion, extra3hs, extraGBA, precio[0])
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
        _, _, margen_obtenido = calcular_margen(
            base, difeCostoIntermediacion, extra3hs, extraGBA, precio_optimo)
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
