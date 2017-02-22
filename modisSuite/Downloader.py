#!/usr/bin/python3
# coding: utf8
"""
Auteur: Gabriel Desharnais

Module permetant de télécharger des images depuis les serveurs du NSIDC

Module that download images from NSIDC servers
"""
from . import logMod
import requests
import datetime
import os
import sys  
import re

#URL de base du serveur de données
URL="https://n5eil01u.ecs.nsidc.org"
URL2="https://e4ftl01.cr.usgs.gov"
#Préfixe à l'addresse de téléchargement
PreTel='<A HREF="'
#
Nom="Downloader"
class telecharger:
    def __init__(self,produit,utilisateur,motdepasse,date="",delta=0,tuiles=[],log=logMod.Log("",nolog=True),output=""):
        self.log=log
        self.tempsRestant=0             #Le temps restant à la tâche
        self.debit=0                    #La vitesse de téléchargement
        self.progression=0              #La progression en pourcentage
        self.produit=produit.upper()
        self.utilisateur=utilisateur
        self.motdepasse=motdepasse
        self.date=date
        self.delta=delta+1
        self.tuiles=tuiles
        self.session=requests.session()
        if output[-1]=="\\":
            self.output=output
        else:
            self.output=output+"\\"
        self.authentification(self.session)
        log.log('i',Nom,'Objet telecharger créer')
    def listeSource(self):
        liste={}
        def listeSourceUSGS():
            h='<img src="/icons/folder.gif" alt="[DIR]"> <a href="'
            prog=re.compile('\<img src="/icons/folder\.gif" alt="\[DIR\]"\> \<a href=".{1,}/">')
            m=prog.findall(self.session.get(URL2).text)
            for e in m:
                nom=e[len(h):-3]
                liste[nom]=URL2+"/"+nom
        def listeSourceNSICD():
            
            r=self.session.get(URL)
            rs=r.text
            i=rs.find("NSIDC DATA ARE AVAILABLE VIA HTTPS VIA THE LINKS BELOW.")
            while not rs[i:].find(PreTel)==-1:
                i=rs[i:].find(PreTel)+len(PreTel)+i
                e=rs[i:].find('"')+i
                f=rs[e:].find('/')+e
                g=rs[f:].find(' ')+f
                #raw_input( rs[i:e])
                liste[rs[f+1:g]]=URL+rs[i:e-1]
                i=g
        listeSourceUSGS()
        listeSourceNSICD()
        return liste
    def listeProduit(self):
        ListeSource=self.listeSource()
        ListeProduit={}
        for l in ListeSource:
                try:
                    #get the web page that list all product
                    r=self.session.get(ListeSource[l])
                    rs=r.text
                    #regex that select only product links
                    prog=re.compile('href="[A-Z,a-z,0-9,\.,_]{1,}/"')
                    #find all match of this re
                    m=prog.findall(rs)
                    #Add match to dictionnary
                    for prod in m:
                        ListeProduit[prod[6:-2].upper()]=ListeSource[l]+"/"+prod[6:-2]
                except:
                    pass
        return ListeProduit
    def listeToutesDates(self):
        ListeDates={}
        l=self.listeProduit()
        #Get the date list for the product
        r=self.session.get(l[self.produit])
        rs=r.text
        #regex that select only date of format YYYY.MM.DD
        prog=re.compile('[0-9]{4}\.[0-9]{2}\.[0-9]{2}')
        #find all match of this re
        m=prog.findall(rs)
        #Add match to dictionnary
        for date in m:
            ListeDates[date]=l[self.produit]+"/"+date
        return ListeDates
    def listeDates(self):
        liste={}
        lToutesDates=self.listeToutesDates()
        for date in self.calendrier():
            try:
                liste[date]=lToutesDates[date]
            except KeyError:
                pass                #N'ajoute pas la clée dans le dict retourné
        return liste
    def calendrier(self):
        date=datetime.date(int(self.date[:4]),int(self.date[5:7]),int(self.date[8:10]))
        for i in range(self.delta):
            yield "{:%Y.%m.%d}".format(date+datetime.timedelta(days=i))
    def authentification(self,session):
        #Devrait éventuellement déterminer lorsque l'authentification ne réussi pas
        def authentificationUSGS():
            h=session.get("https://e4ftl01.cr.usgs.gov/MOLT/MOD09A1.005/2000.02.18/MOD09A1.A2000049.h00v08.005.2006268222532.hdf",auth=(self.utilisateur,self.motdepasse),allow_redirects=False)
            h=session.get(h.headers["Location"],auth=(self.utilisateur,self.motdepasse),allow_redirects=False)
        def authentificationNSIDC():
            form={}
            formfield=["utf8","authenticity_token","client_id","redirect_uri","response_type","state","stay_in","commit"]
            r=session.get(URL+"/MOST")
            rs=r.text
            for name in formfield:
                utf8formA=rs.find('name="'+name+'"')
                utf8formA+= rs[utf8formA:].find('value=\"') +len('value=\"')
                utf8formB=utf8formA+rs[utf8formA:].find('\"')

                form[name]=rs[utf8formA:utf8formB]
        
#print form
            form["username"]=self.utilisateur
            form["password"]=self.motdepasse
            h=session.post('https://urs.earthdata.nasa.gov/login',data=form)
            import time
            time.sleep(3)
            a=h.text.find('redirectURL = "')+len('redirectURL = "')
            b=h.text[a:].find('"')+a
            session.get(h.text[a:b])
        authentificationNSIDC()
        authentificationUSGS()
    def listefichiersATelecharger(self,addresseDate):
        listefichiers={}
        typeOfFile=["\.hdf","\.hdf\.xml"]
        #Get list of file for date
        r=self.session.get(addresseDate)
        rs=r.text
        for tuile in self.tuiles:
            for typ in typeOfFile:
                try:
                    #Regex to find the file to download
                    prog=re.compile('href="[A-Z,a-z,0-9,_,\.]{1,}'+tuile+'[A-Z,a-z,0-9,_,\.]{1,}'+typ)
                    #Find first occurence of this re
                    m=prog.search(rs)
                    listefichiers[m.group(0)[6:]]=addresseDate+"/"+m.group(0)[6:]
                except:
                    pass
        return listefichiers
    def telechargerUnfichier(self,addresse,nom):
        #Devrait vérifier l'existance d'un fichier sur le disque avant de le télécharger
        r=self.session.get(addresse)
        with open(self.output+nom,'wb') as f:
            tailleFichier = int(r.headers['content-length'])#Ça va récupérer la taille du fichier à télécharger
            f.write(r.content)
        reussi= tailleFichier==os.path.getsize(self.output+nom)
        #Si le fichier télécharger a la taille théorique alors celle-ci est retournée.
        if reussi:
            return tailleFichier
        else:
            return None

    def telechargerTout(self):
        echecDeSuite=0
        while True:
            try:
                #On va chercher toutes les dates disponible sur le serveur de la NSIDC pour un produit en particulier
                self.log.log('c',Nom,u'Lister les Dates disponibles sur le serveur.')
                ListeDate=self.listeDates()
                self.log.log('r',Nom,u'Lister les Dates disponibles sur le serveur.')
                #Chaque date est entrée comme clé dans un dictionnaire et une adresse du dossier de cette date y est assignée
                self.log.log('i',Nom,str(len(ListeDate))+u' date(s) ont été trouvé.')
                LListeDate=list(ListeDate)
                break
            except:
                echecDeSuite+=1
                if echecDeSuite>3:
                    break
            
        echecDeSuite=0
        for date in LListeDate:
            listeTrucsTelecharges=[]
            #Pour chacune des dates, Une liste des adresse de téléchargement est produite
            try:
                self.log.log('c',Nom,u'Lister les fichier de téléchargement disponibles pour '+date)
                ListeFichier=self.listefichiersATelecharger(ListeDate[date])
                self.log.log('r',Nom,u'Lister les fichier de téléchargement disponibles pour '+date)
                self.log.log('i',Nom,str(len(ListeFichier))+u' fichier(s) ont été trouvés pour '+date)
                for fichier in ListeFichier:
                    self.log.log('c',Nom,u'Télécharment pour le fichier '+fichier+u' du '+date)
                    
                    r=self.telechargerUnfichier(ListeFichier[fichier],fichier)
                    if not r==None:
                        listeTrucsTelecharges.append(fichier)
                        self.log.log('r',Nom,u'Télécharment pour le fichier '+fichier+u' du '+date)
                        self.log.log('i',Nom,u'Le fichier '+fichier+u' du '+date+u' a une taille de '+str(r))
                    else:
                        self.log.log('e',Nom,u'Télécharment pour le fichier '+fichier+u' du '+date)
                    with open(self.output+'listfile'+self.produit.upper()+'.txt','a') as f:
                        f.write(fichier+'\n')
                echecDeSuite=0
                yield date, listeTrucsTelecharges
            except requests.exceptions.ConnectionError:
                echecDeSuite+=1
                if echecDeSuite<3:
                    LListeDate.append(date)
                yield date, listeTrucsTelecharges
def main():
    for x,y in telecharger("mod10a2.006","user","password",date="2010-02-20",delta=20,tuiles=['h12v04','h13v04'],output="test/").telechargerTout():
        print(x,y)
if __name__=='__main__':
    main()
    
