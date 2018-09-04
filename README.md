# datasud_crawler
Crawler for Datasud API CKAN

Ces scripts permettent d'interroger l'API CKAN de Datasud.fr et de réaliser un suivi de la publication de données sur le portail. Le script init_fichier.py initialise les deux fichiers de résultats, le script add_data.py y ajoute chaque jour une nouvelle ligne (grâce à un cron quotidien).

Les deux fichiers de résultats sont aux formats CSV. Ils présentent, pour chaque jour, le nombre de données publiées en distinguant les thématiques pour l'un, et les types de données pour l'autre (géographique, ouvertes, intelligentes).
