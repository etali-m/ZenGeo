from django.shortcuts import render 
from django.contrib.gis.geoip2 import GeoIP2 #cette bibliothèque permet d'obtenir les coordonnées
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

import requests
import json

import firebase_admin 
from firebase_admin import credentials, firestore


# Initialisation du SDK de firebase pour le projet
cred = credentials.Certificate("/home/etali/Programmation/Web/Django/Geolocation/geolocation/gelocation-88d53-firebase-adminsdk-y7038-88b7d27144.json")
firebase_admin.initialize_app(cred)

def index(request): 
    #On recupère l'adresse ip de l'utilisateur
    ip = requests.get('https://api.ipify.org/?format=json')
    ip_data = json.loads(ip.text)
    #On recupère les informations sur la position à partir de l'adresse IP trouvé
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data = json.loads(res.text) #position actuel du client WEB

    #Récupération du client firebase
    db = firestore.client()

    identifier = request.GET.get('recherche')
    referenced_user = ""
    positions = []

    if identifier:
        print(identifier)
        #Recupérer tout le document d'un utilisateur spécifique
        doc_ref = db.collection("utilisateur_position").document(str(identifier))
        if doc_ref.get().exists:

            positions = doc_ref.get().to_dict()['position_ids']
            for item in positions:
                item['timestamp'] = item['timestamp'].isoformat()

            positions = json.dumps(positions)
            print(positions)

            #on recupère le champ référencé dans un autre document
            referenced_doc = doc_ref.get().to_dict()['user_id'] 

            if referenced_doc is not None:
                #on recupère les informations sur l'utilisateur
                referenced_user = db.collection('utilisateur').document(referenced_doc.id).get().to_dict()
                print(f'Champ reférencé: {referenced_user}') 
            else:
                print("La référence est vide ou ne correspond à aucun document")



    """Ajouter un élément au tableau des position d'un utilisateur"""
    #users_ref.update({'position_ids': firestore.ArrayUnion([nouvel_objet])})

   

    #users = [doc.to_dict() for doc in users_ref.stream()]
    #On envoie les données récuperées dans le context
    context = { 
        'data': location_data,
        'searched_user': referenced_user,
        'positions' : positions,
        'identifier': identifier,
        }

    return render(request, 'location/home.html', context) 
