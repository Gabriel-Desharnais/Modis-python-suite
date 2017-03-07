#!/usr/bin/python3
# coding: utf8 

class imageModis:
    def __init__(self,files,*arg,**args):
        self.files=files
class Afile:
    def __init__(self,name,date,link,typ,*arg,**args):
        self.name=name
        self.date=date
        self.typ=typ
        self.link=link
        self.size=0
        self.tile=0
        self.product=0
        self.dateTelechargement=""
        self.telecharge=True
