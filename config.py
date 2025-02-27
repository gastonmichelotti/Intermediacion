# Configuracion de variables

# Conexion a la base de datos
from sqlalchemy import create_engine

server = '26.150.228.219'
database = 'rapiboyv7'
username = 'gastonMichelotti'
password = 'e4c9b81800490aab2c7ece08018853f23ac75e08ecb7725a6d6cb496539b3fe1'
driver = 'ODBC Driver 18 for SQL Server'
port = '1433'
conn = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}&TrustServerCertificate=yes"

engine = create_engine(conn)

# Mapeo Deals Con usuarios
DEALS = {'sushi_club': [31425, 5660, 7731, 5312, 7900, 32920, 7819, 7786],
         'fabric': [20307, 30984, 21626, 26274, 14264, 28888],
         'fabric_guido': [55260, 55262, 55263, 55367, 55368]}
