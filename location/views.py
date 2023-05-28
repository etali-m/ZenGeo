from django.shortcuts import render 
from django.contrib.gis.geoip2 import GeoIP2 #cette bibliothèque permet d'obtenir les coordonnées
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.contrib import messages

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
    search_date = request.GET.get('date')
    heure_debut =  request.GET.get('hdebut')
    heure_fin = request.GET.get('hfin')
    referenced_user = ""
    positions = []

    if identifier:
        print(identifier)
        #Recupérer tout le document d'un utilisateur spécifique
        doc_ref = db.collection("utilisateur_position").document(str(identifier))
        if doc_ref.get().exists:

            positions = doc_ref.get().to_dict()['position_ids']
            #on convertit toutes les dates au format iso
            for item in positions:
                item['timestamp'] = item['timestamp'].isoformat()

            #on selectionne les positions qui correspondent à la date entrée.
            
            if search_date:
                filtered_positions = []
                for item in positions:
                    date_iso = datetime.fromisoformat(item['timestamp']) 
                    date_formatted_datetime = datetime.strptime(search_date, "%Y-%m-%d")  #on format la date entrée par l'utilisateur
                    if date_iso.date() == date_formatted_datetime.date():
                        if (heure_debut):
                            heure_d = int(heure_debut) - 1 
                            if(date_iso.hour >= heure_d):
                                if (heure_fin):
                                    heure_f = int(heure_fin) - 1
                                    if(date_iso.hour <= heure_f):
                                        filtered_positions.append(item)  
                                else:
                                    filtered_positions.append(item)
                        else:
                            filtered_positions.append(item)

                print(filtered_positions)
                positions = filtered_positions

            if positions != []:
                message = str(len(positions)) + " lieu(x) trouvé !"
                messages.success(request, message)
            else:
                message = "Aucun Lieu trouvée !"
                messages.warning(request, message)

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

        else:
            messages.error(request, "L'identifiant entré ne correspond à aucun utilisateur !")


    """Ajouter un élément au tableau des position d'un utilisateur"""
    #users_ref.update({'position_ids': firestore.ArrayUnion([nouvel_objet])})

   

    #users = [doc.to_dict() for doc in users_ref.stream()]
    #On envoie les données récuperées dans le context
    context = { 
        'data': location_data,
        'searched_user': referenced_user,
        'positions' : positions,
        'identifier': identifier,
        'search_date': search_date,
        'heure_debut': heure_debut,
        'heure_fin' : heure_fin,
        }

    return render(request, 'location/home.html', context) 
