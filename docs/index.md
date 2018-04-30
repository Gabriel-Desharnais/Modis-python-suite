# Description
This python module can bulk download and do basic opperation (clip, mosaic, compress, etc.) on Modis satelite images from the NSIDC and USGS servers. It is compatible with both python 2 and python 3.
# How to install
To install you must have installed python (2 or 3), have an **earthdata** acount with the applications **LP DAAC Data Pool** and **NSIDC_DATAPOOL_OPS** approved ([https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov/)) and have pip installed on your computer.

Then you just type `pip install modisSuite` with the administrative right in the console.
# Simple example
This simple example show you how to download data from NASA servers. This code will download every day availlable between 2010-02-20 and 2010-03-12
from the MYD10A2.006 product and mosaic the tiles together.

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
  day.mosaic()
```
# Documentation
You can find the user manual [here](https://github.com/Gabriel-Desharnais/Modis-python-suite/en/userManual)
You can find the code documention [here](https://gabriel-desharnais.github.io/Modis-python-suite/en/package)
# Support
If you are having any problems, or have any sugesstion for improvement, just post an issue on the github page. I will be more than happy to help you in your project. [issues](https://github.com/Gabriel-Desharnais/Modis-python-suite/issues)
# Contribute
If you want to give a hand you can do any of the following:
- Share the project with your colleague.
- Repport issue/improvement on the github page
- Improve code on your branch on github

# License
This software is using the MIT license
# Ohter language
[version française](https://gabriel-desharnais.github.io/Modis-python-suite/fr/accueil)
