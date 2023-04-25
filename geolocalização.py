import pandas as pd
import folium
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="matheus-bn") # Defina seu nome de usuário aqui

# Ler o arquivo Excel com o nome da cidade e o estado
cidades = r'cidades.xlsx'
df = pd.read_excel(cidades)

# Criar as colunas para armazenar as coordenadas
df["latitude"] = ""
df["longitude"] = ""

# Iterar sobre as linhas e obter as coordenadas de cada cidade
for index, row in df.iterrows():
    city = row["city"]
    state = row["state"]
    location = geolocator.geocode(f"{city}, {state}")
    if location:
        df.at[index, "latitude"] = location.latitude
        df.at[index, "longitude"] = location.longitude
    else:
        print(f"Coordenadas não encontradas para {city}, {state}")

# Salvar as coordenadas no arquivo Excel
with pd.ExcelWriter(cidades) as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

# Ler o arquivo Excel com as coordenadas
df = pd.read_excel(cidades)

# Verificar se as coordenadas foram adicionadas corretamente
#print(df.head())

# Criar um objeto Mapa
mapa = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=5)

# Adicionar marcadores para cada uma das coordenadas
for index, row in df.iterrows():
    city = row["city"]
    state = row["state"]
    latitude = row["latitude"]
    longitude = row["longitude"]
    popup_text = f"{city}, {state}"
    folium.Marker(location=[latitude, longitude], popup=popup_text).add_to(mapa)

# Exibir o mapa
mapa