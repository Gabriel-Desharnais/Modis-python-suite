# -*- coding: utf-8 -*-
"""
Auteur: Gabriel Desharnais

Module permetant de gérer les logs le but étant de simplement passer un objet
qui sera éditer par tous programmes, sous-programmes et modules

Lors de la déclaration d'ojet, il faut spécifié le répertoire où sera écrit le
log, le nom du fichier (si nom spécifié ou "date", la date de création d'objet
Log sera utilisé), s'il faut afficher les logs à l'écran (echo=True), s'il faut
 écrire les logs dans le fichier (nolog=True).
 
 *** __init__ ***
** Param **
 repertoire     str: Le chemain d'accès au répertoire où est enregistré le log
* optionel *
 fichier="date" str: Le nom du fichier (si nom spécifié ou "date", la date de
                     création d'objet Log sera utilisé)
 echo=False    bool: Indique si les entrées dans le log doivent être afficher 
                     (True-->affichage à l'écran)
 nolog=False   bool: Indique si les entrées doivent être inscrite dans le 
                     fichier (False-->Inscription dans le fichier)
***log***
** Param **
 sorte          str: Quelle sorte d'entré est-ce. 
                     'e' --> ERREUR
                     'w' --> AVERTISSEMENT
                     'i' --> INFORMATION
                     'r' --> réussi
                     'c' --> COMMENCÉ
 programme      str: Le nom du programme qui produit cette entrée
 message        str: Le message de cette entrée
* optionel *
echo=""        bool: Permet de changer momentanément la propriété d'affichage 
                     des entées (True --> Affichage à l'écran)
"""
import datetime
class Log:
    def __init__(self,repertoire,fichier="date",echo=False,nolog=False):
        if fichier == "date":
            fichier ='log_{:%Y_%m_%d_%H_%M_%S}.log'.format(datetime.datetime.now())
        if (not repertoire=="") and (not repertoire[-1]=="\\"):
            repertoire+="\\"
        self.acces=repertoire+fichier
        self.echo=echo
        self.TIMESTAMP = '[{:%Y-%m-%d %H:%M:%S}]'
        self.error={'e':' ERREUR ','w':' AVERTISSEMENT ','i':' INFORMATION ','r':' RÉUSSI ','c':' COMMENCÉ '}
        self.nolog=nolog
    def log(self,sorte,programme,message,echo=""):
        if not self.nolog:
            with open(self.acces,'a') as f:
                f.write(self.TIMESTAMP.format(datetime.datetime.now())+programme+':'+self.error[sorte]+message+'\n')
                if echo=="":
                    echo=self.echo
                if echo:
                    try:
                        print(self.TIMESTAMP.format(datetime.datetime.now())+programme+':'+self.error[sorte]+message)
                    except:
                        print(self.TIMESTAMP.format(datetime.datetime.now())+programme+':'+self.error[sorte]+message)
                    
            

def main():
    pass

if __name__=='__main__':
    main()
  
