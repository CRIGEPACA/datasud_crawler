#!/usr/bin/python
# -*- coding: utf-8 -*-

###### IMPORT DES DIFFERENTS MODULES ######

import sys
import os
import os, os.path as OP
import re
import json
import urllib
import csv
from datetime import datetime
import string

Now = datetime.now()
Now_w = str(Now.date())+"_"+str(Now.hour)+"-"+str(Now.minute)
Now_date = Now.date()

###### DOSSIER D'ENREGISTREMENT ET FICHIERS DE SORTIE #######

# Repertoires a créer si inexistants
dirScript = OP.abspath(OP.split(__file__)[0])
# dirSrc = "/DATA/fileadmin/opendata/_crawler"
# dirResult = dirSrc +"//result_crawler"
dirResult ="/DATA/fileadmin/opendata/_crawler"
if not os.path.exists(dirResult):
    os.makedirs(dirResult)
dirLog = dirScript + "//log"
if not os.path.exists(dirLog):
    os.makedirs(dirLog)
	
# Fichier de log
pathFileLog = dirLog + "//log_%s.txt"%(Now_w)
fileLog = open(pathFileLog, "w")
fileLog.write("Lancement du crawler le %s \n\nEcriture des fichiers csv \n\n" %(Now))

# Fichier de resultat en csv
	# nombre de donnéees par thématique : group.csv
pathFileCsvGroup = dirResult+"//group.csv"
csvGroup = csv.reader(open(pathFileCsvGroup, "rb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )
	# nombre de donnéees par type : type.csv
pathFileCsvType = dirResult+"//type.csv"
csvType = csv.reader(open(pathFileCsvType, "rb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )	


###### FONCTIONS ########

# Fonction de récupération du nombre de dataset, pour une requete
def nbFromRequest (url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    assert data["success"] is True
    nb = data["result"]["count"]
    fileLog.write("	-> %s\n 	-> nombre : %i\n\n" %(url,nb))
    return nb

# Fonction d'ajout des nombres de dataset dans une liste
def Line4Csv(urlFix, lstLine, lstURL):
    for i in range(len(lstURL)):
        url = urlFix+lstURL[i]
    	fileLog.write(lstURL[i]+"\n")
    	nb = nbFromRequest(url)
    	print lstURL[i],nb
    	lstLine.append(nb)

# Ajout d'une nouvelle ligne au contenu précédent d'un csv
def saveCSV(csvIni, line, pathCsv):
    newCSV=[]
    for li in csvIni:
        newCSV.append(li)
    newCSV.append(line)
    csvFin = csv.writer(open(pathCsv, "wb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )
    for li in newCSV:
		csvFin.writerow(li)


###### NOMBRE DE DATASET PAR GROUPE #######

fileLog.write ("\n\n#####	  NOMBRE DE DATASET PAR GROUPE   #####\n\n")
print "\n\n#####	  NOMBRE DE DATASET PAR GROUPE   #####\n\n"

# Récupération de la liste des groupes 
urlAPI_listGroup="https://trouver.datasud.fr/api/3/action/group_list"
fileLog.write("Récupération de la liste des groupes grace à la requete de l'API : \n%s\n\n"%(urlAPI_listGroup))
repAPI_listGroup = urllib.urlopen(urlAPI_listGroup)
dataAPI_listGroup=json.loads(repAPI_listGroup.read())
assert dataAPI_listGroup["success"] is True
API_listGroup = dataAPI_listGroup["result"]

# Fabrication des url, récupération des nombres, inscription dans le csv
urlAPI_group = "https://trouver.datasud.fr/api/3/action/package_search?fq=+groups:"
line = [Now_date]
Line4Csv(urlAPI_group, line, API_listGroup)
saveCSV(csvGroup,line,pathFileCsvGroup)


	
###### NOMBRE DE DATASET PAR TYPE #######

fileLog.write ("\n\n\n#####	  NOMBRE DE DATASET PAR TYPE   #####\n\n")
print "\n\n\n#####	  NOMBRE DE DATASET PAR TYPE   #####\n\n"

# Récupération du nombre total de données
fileLog.write("Nombre de donnees au total :\n\n")
url = "https://trouver.datasud.fr/api/3/action/package_search?"
nb = nbFromRequest(url)
print "Nombre de dataset au total %i"%(nb)

# Fabrication des url, récupération des nombres, inscription dans le csv
API_listType = ['donnees-ouvertes','donnees-geographiques','donnees-intelligentes']
urlAPI_type = "https://trouver.datasud.fr/api/3/action/package_search?fq=+datatype:"
line = [Now_date,nb]
Line4Csv(urlAPI_type, line, API_listType)
saveCSV(csvType,line,pathFileCsvType)



###### ENREGISTREMENT DU FICHIER DE LOG #########
fileLog.close()
