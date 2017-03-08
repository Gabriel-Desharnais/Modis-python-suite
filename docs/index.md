# Description
This python module can bulk download Modis satelite images from the NSIDC and USGS servers. It is compatible with both python 2 and python 3.
# How to install
To install you must have installed python (2 or 3), have an **earthdata** acount with the applications **LP DAAC Data Pool** and **NSIDC_DATAPOOL_OPS** approved ([https://urs.earthdata.nasa.gov/](url)) and have pip installed on your computer.

Then you just type `pip install modisSuite` with the administrative right in the console.
# Simple example
This simple example show you how to download data from nasa servers. This code will download every day availlable between 2010-02-20 and 2010-03-12
from the MOD10A.006 product.

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
# Documentation
You can find all documention *here*
# Ohter language
[version française](https://gabriel-desharnais.github.io/Modis-python-suite/fr/accueil)
