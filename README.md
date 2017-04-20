# Modis-python-suite
This python module can bulk download Modis satelite images from the NSIDC and USGS servers. It is compatible with both python 2 and python 3.

- [X] Works on python 3
- [X] Works on python 2

- [X] Download from NSIDC
- [X] Download from USGS

For more information go to [https://gabriel-desharnais.github.io/Modis-python-suite/](https://gabriel-desharnais.github.io/Modis-python-suite/)

### To install
to install on python2 type `sudo python2 setup.py install` to install on python3 type `sudo python3 setup.py install`. python2 and python3 command may be different on your computer.

You have to create an acount on **earthdata** [https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov/) and approve the applications **LP DAAC Data Pool** and **NSIDC_DATAPOOL_OPS**.
### simple example
this code will download every day availlable between 2010-02-20 and 2010-03-12
```python
import modisSuite
#Create object
prod="myd10a2.006"
username=""
password=""
startdate="2010-02-20"
d=20 #Download 20 days
tiles=['h12v04','h13v04']
folder="test/" #will download all file in the folder test
doo=modisSuite.downloader(prod,username,password,date=startdate,delta=d,tuiles=tiles,output=folder)
# telechargerTout is a constructor each itteration of it will download a day
for day in doo.telechargerTout():
  print([aFile.name for aFile in day.files])
```
### Note
#### python 2
- [ ] tested on windows
- [X] tested on Mint 18.1
- [ ] tested on Mageia 5

#### python 3
- [X] tested on windows
- [X] tested on Mint 18.1
- [X] tested on Mageia 5

## Version Française
Ce module python permet de télécharger en masse des images satelites Modis depuis les serveurs de NSIDC et USGS. Il est compatible avec python 2 et python 3.

- [X] Fonctionne sur python 3
- [X] Fonctionne sur python 2

- [X] Télécharge depuis NSIDC
- [X] Télécharge depuis USGS

Pour plus d'information aller sur [https://gabriel-desharnais.github.io/Modis-python-suite/fr/accueil](https://gabriel-desharnais.github.io/Modis-python-suite/fr/accueil)
### Pour installer
Pour installer sur python2 `sudo python2 setup.py install` pour installer sur python3 `sudo python3 setup.py install`. Les noms de commandes `python2` et `python3`peuvent varier selon la configuration de votre ordinateur.

Vous devez créer un compte sur **earthdata** [https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov/). Il faut aussi approuvrer les applications **LP DAAC Data Pool** et **NSIDC_DATAPOOL_OPS**.
### exemple simple
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
  print([fichier.name for fichier in jour.files])
```

### Note
#### python 2
- [ ] testé sur windows
- [X] testé sur Mint 18.1
- [ ] testé sur Mageia 5

#### python 3
- [X] testé sur windows
- [X] testé sur Mint 18.1
- [X] testé sur Mageia 5
