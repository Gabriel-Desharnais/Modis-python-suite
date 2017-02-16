# Modis-python-suite
This python module can bulk download Modis satelite images from the NSIDC and USGS servers. It is compatible with both python 2 and python 3.

- [X] Works on python 3
- [ ] Works on python 2

- [X] Download from NSIDC
- [ ] Download from USGS

### simple example
this code will download every day availlable between 2010-02-20 and 2010-03-12
```python
import Downloader
#Create object
prod="myd10a2.006"
username=""
password=""
startdate="2010-02-20"
d=20 #Download 20 days
tiles=['h12v04','h13v04']
folder="test/" #will download all file in the folder test
doo=Downloader.telecharger(prod,username,password,date=startdate,delta=d,tuiles=tiles,output=folder)
# telechargerTout is a constructor each itteration of it will download a day
for x,y in doo.telechargerTout():
  print(x,y)
```

## Version Française
Ce module python permet de télécharger en masse des images satelites Modis depuis les serveurs de NSIDC et USGS. Il est compatible avec python 2 et python 3.

- [X] Fonctionne sur python 3
- [ ] Fonctionne sur python 2
- [X] Télécharge depuis NSIDC
- [ ] Télécharge depuis USGS
