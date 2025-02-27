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
