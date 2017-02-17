#!/usr/bin/python3
# coding: utf8
"""
Auteur: Gabriel Desharnais

Module permetant de télécharger des images depuis les serveurs du NSIDC

Module that download images from NSIDC servers
"""
import logMod
import requests
import datetime
import os
import sys  

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
        self.produit=produit.lower()
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
                liste[rs[f+1:g]]=URL+rs[i:e]
                i=g
        listeSourceNSICD()
        return liste
    def listeProduit(self):
        ListeSource=self.listeSource()
        ListeProduit={}
        def listeProduitNSICD():
            for l in ListeSource:
                r=self.session.get(ListeSource[l])
                
                #open("result.html","wb").write(s.get(ListeSource[l]).content)
                rs=r.text
                rss=rs.upper()
                #raw_input(rs)
                i=rss.find(PreTel)#+len(PreTel)
                
                for x in range(6):
                    i=rss[i:].find(PreTel)+len(PreTel)+i
                #raw_input( rss[i:])
                    
                while not rss[i:].find(PreTel)==-1 and (not rs[i:].find("<tr")==-1):
                    i=rss[i:].find(PreTel)+len(PreTel)+i
                    i=rss[i:].find(PreTel)+len(PreTel)+i
                    e=rss[i:].find('"')+i
                    f=rss[e:].find('>')+e+1
                    g=rss[f:].find('/')+f
                    #raw_input( URL+'/'+l+'/'+rs[i:e])
                        
                    ListeProduit[rs[f:g].lower()]=URL+'/'+l+'/'+rs[i:e]
                    i=g
        listeProduitNSICD()
        return ListeProduit
    def listeToutesDates(self):
        ListeDates={}
        def listeToutesDatesNSICD():
            
            l=self.listeProduit()
            r=self.session.get(l[self.produit])
            rs=r.text
            rss=rs.upper()
                #raw_input(rs)
            i=rss.find(PreTel)#+len(PreTel)
                    
            for x in range(6):
                i=rss[i:].find(PreTel)+len(PreTel)+i
            #raw_input( rss[i:])
            while not rss[i:].find(PreTel)==-1 and (not rs[i:].find("<tr")==-1):
                i=rss[i:].find(PreTel)+len(PreTel)+i
                i=rss[i:].find(PreTel)+len(PreTel)+i
                e=rss[i:].find('"')+i
                f=rss[e:].find('>')+e+1
                g=rss[f:].find('/')+f
                    #raw_input( URL+'/'+l+'/'+rs[i:e])
                if not rs[f:g].lower().find("dprecentinserts")==-1:
                    break
                ListeDates[rs[f:g].lower()]=l[self.produit]+rs[i:e]
                i=g
        listeToutesDatesNSICD()
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
        r=self.session.get(addresseDate)
        rs=r.text
        for tuile in self.tuiles:
            tuile=tuile.lower()         #Sur le site le nom des tuiles est en minuscule
            i=0
            for h in range(3):
                i=rs[i:].find(tuile)+len(tuile)+i        #Éliminer le fichier jpg
            #Trouver les fichier xml et hdf
            while not rs[i:].find(tuile)==-1 :
                i=rs[i:].find(tuile)+i
                
                i=rs[i:].find(PreTel.lower())+len(PreTel)+i
                e=rs[i:].find('"')+i
                f=rs[e:].find('>')+e+1
                g=rs[f:].find('<')+f
                
                
                listefichiers[rs[f:g]]=addresseDate+rs[i:e]
                i=g
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
                self.log.log('c',Nom,'Lister les Dates disponibles sur le serveur.')
                ListeDate=self.listeDates()
                self.log.log('r',Nom,'Lister les Dates disponibles sur le serveur.')
                #Chaque date est entrée comme clé dans un dictionnaire et une adresse du dossier de cette date y est assignée
                self.log.log('i',Nom,str(len(ListeDate))+' date(s) ont été trouvé.')
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
                self.log.log('c',Nom,'Lister les fichier de téléchargement disponibles pour '+date)
                ListeFichier=self.listefichiersATelecharger(ListeDate[date])
                self.log.log('r',Nom,'Lister les fichier de téléchargement disponibles pour '+date)
                self.log.log('i',Nom,str(len(ListeFichier))+' fichier(s) ont été trouvés pour '+date)
                for fichier in ListeFichier:
                    self.log.log('c',Nom,'Télécharment pour le fichier '+fichier+' du '+date)
                    
                    r=self.telechargerUnfichier(ListeFichier[fichier],fichier)
                    if not r==None:
                        listeTrucsTelecharges.append(fichier)
                        self.log.log('r',Nom,'Télécharment pour le fichier '+fichier+' du '+date)
                        self.log.log('i',Nom,'Le fichier '+fichier+' du '+date+' a une taille de '+str(r))
                    else:
                        self.log.log('e',Nom,'Télécharment pour le fichier '+fichier+' du '+date)
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
    for x,y in telecharger("myd10a2.006","user","password",date="2010-02-20",delta=20,tuiles=['h12v04','h13v04'],output="test/").telechargerTout():
        print(x,y)
if __name__=='__main__':
    main()
