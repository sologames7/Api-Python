from flask import Flask, request
from dataclasses import field
import json
import pandas as pd
import matplotlib.pyplot as plt
from operator import itemgetter
import plotly.express as px


# début calcul tableau d'objets contenant la donnée calculé
f = open('population-francaise-communes-2014.json')
data = json.load(f)
df = pd.read_json('population-francaise-communes-2014.json')
data = []

for x in df[0:360]['fields']:
    data.append({'aPart':x["population_comptee_a_part"],'popTotale': x["population_totale"],'longitude': x["coordonnees"][1],'latitude': x["coordonnees"][0],'nomComune' : x['nom_de_la_commune'] , 'tauxDisolement' : round((x['population_comptee_a_part']/x['population_totale'])*100, 2)})

dataSorted = sorted(data, key=itemgetter('tauxDisolement')) 
# fin calcul tableau d'objets contenant la donnée calculé



app = Flask(__name__)

@app.route('/status', methods=['GET'])
def a_live():
    return "<h1>Server Alive</h1>"

@app.route('/home', methods=['GET'])
def home():
    

    fig = px.density_mapbox(dataSorted, lat='latitude', lon='longitude', z='tauxDisolement', radius=20, hover_name="nomComune",
                        center=dict(lat=42.0396, lon=9.0129), zoom=7,range_color=(0, 7),
                        color_continuous_scale="YlOrRd",
                        mapbox_style="stamen-terrain")
    fig.show()

    return "<h2>La carte des chaleur avec le taux d'isolement de la population de 0 à 7%</h2> <br> le taux monte jusqu'a 14% mais pour un résultat interressant j'ai décidé de ne monter qu'à 7% la masse étant concentré autour des 3%... "


@app.route('/coord/<lLat>/<lLong>/<hLat>/<hLong>', methods=['GET'])
def perso( lLat= None, lLong = None, hLat = None, hLong = None):
    lLat, lLong, hLat, hLong = float(lLat), float(lLong), float(hLat), float(hLong) # passage de string à entier pour les coordonnées (sLat = "low latitude") pour la latitude du premier point
    if lLat>hLat or lLong>hLong:
        return "<h1>PARAMETRE DE COORDONEES INVALIDES</h1><br><h2>Se référer au README.txt</h2>"
        
    persData = []
    for comune in dataSorted:
        if ( lLat <= comune['latitude'] <= hLat) and  ( lLong <= comune['longitude'] <= hLong):
            persData.append(comune)

    popTot = 0
    popIso = 0
    
    for comune in persData:
        popTot += comune["popTotale"]
        popIso += comune["aPart"]
    
    tauxIso = round((popIso/popTot)*100, 2)


    fig = px.density_mapbox(persData, lat='latitude', lon='longitude', z='tauxDisolement', radius=20, hover_name="nomComune",
                            center=dict(lat=42.0396, lon=9.0129), zoom=7,
                            color_continuous_scale="YlOrRd",
                            mapbox_style="stamen-terrain")
    fig.show()
    
    return "<h1>premier point [latitude: "+str(lLat)+", longitude: "+str(lLong)+"] <br> second point [latitude: "+str(hLat)+", longitude: "+str(hLong)+"]</h1> <br> <h2>Information sur la zone séléctionné:</h2> <br>population totale: "+str(popTot)+"<br>population isolé: "+str(popIso)+"<br>taux d'isolement: "+str(tauxIso)+"%"

app.run(port=4000)