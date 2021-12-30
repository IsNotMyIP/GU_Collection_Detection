import pandas as pd
import os

path = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(path + '/ole.csv', delimiter=",", header=0, names=['Nombre Carta', 'Cantidad'], encoding='windows-1252')
print(data)