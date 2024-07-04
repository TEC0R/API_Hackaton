from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from GET.pinecone_vec import reco_mentor
import json

#Lancer api : 
#uvicorn main:app --reload --host 0.0.0.0 --port 8000

def json_load(file):
    with open(f'./data/{file}.json', 'r') as f:
        # Charger les données JSON
        data = json.load(f)
    return data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou spécifiez les origines spécifiques nécessaires
    allow_credentials=True,
    allow_methods=["*"],   # Ou spécifiez les méthodes HTTP nécessaires (par exemple, ["GET", "POST"])
    allow_headers=["*"],   # Ou spécifiez les en-têtes nécessaires
)


#-----------------------------------------------------------
#       Accueil 
#-----------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Hand to Hand"}

#-----------------------------------------------------------
#       Formation 
#-----------------------------------------------------------

@app.get("/trainings")
def trainings():
    return json_load("trainings")

#-----------------------------------------------------------
#       Mentors 
#-----------------------------------------------------------

@app.get("/mentors")
def mentors():
    return json_load("mentors")

@app.get("/mentors/{index}")
def mentors(index : int):
    json = json_load("mentors")
    return [json[index]]

#-----------------------------------------------------------
#       Clients 
#-----------------------------------------------------------

@app.get("/clients")
def clients():
    return json_load("clients")

@app.get("/clients/{index}")
def clients(index : int):
    json = json_load("clients")
    return [json[index]]

#-----------------------------------------------------------
#       Reco mentor 
#-----------------------------------------------------------

@app.get("/reco_mentor/{texte}")
def reco_mentors(texte):
    texte = texte.replace("%20", " ")
    return reco_mentor(texte)

    


