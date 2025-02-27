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


def calcular_margen(base: pd.DataFrame, difeCostoIntermediacion: float, margenFinal: float, extra3hs: float, precio: float):

    costo = sum(
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
