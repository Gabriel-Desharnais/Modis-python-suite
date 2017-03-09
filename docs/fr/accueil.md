# Description
Ce module python permet de télécharger en masse des images satelites Modis depuis les serveurs de NSIDC et USGS. Il est compatible avec python 2 et python 3.

# Comment installer
Au préalable, vous devez installer *python* (2 ou 3), installer *pip* et approuvrer les applications **LP DAAC Data Pool** et **NSIDC_DATAPOOL_OPS** sur votre compte **earthdata** ([https://urs.earthdata.nasa.gov/]) .

Pour installer, entrer `pip install modisSuite` dans une console en tant qu'administrateur. 

# exemple simple
Ce petit exemple montre comment télécharger des images depuis les serveurs de la NASA. Ce scipt télécharge tous les fichiers entre le 20-02-2010 et le 12-03-2010 du produit MYD10A2.006.

```python
import modisSuite
#Create object
prod="myd10a2.006"
utilisateur=""
motdepasse=""
datedebut="2010-02-20"
nombJour=20 #téléchargement de 20 jours
tuiles=['h12v04','h13v04']
sortie="test/" #Tous les fichiers téléchargés seront enregistrés dans le dosier «test»
doo=modisSuite.downloader(prod,utilisateur,motdepasse,date=datedebut,delta=nombJour,tuiles=tuiles,output=sortie)
# telechargerTout is a constructor each itteration of it will download a day
for jour in doo.telechargerTout():
  print([fichier.name for fichier in jour])
```
# Documentation
Toute la documentation peut être trouvée *ici*.
# Autre langue
[English version](https://gabriel-desharnais.github.io/Modis-python-suite/)
