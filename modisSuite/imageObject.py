#!/usr/bin/python3
# coding: utf8 

class imageModis:
    def __init__(self,files,*arg,**args):
        self.files=files
class Afile:
    def __init__(self,name,date,typ,size,tile,product,*arg,**args):
        self.name=name
        self.date=date
        self.typ=typ
        self.size=size
        self.tile=tile
        self.product=product
        self.dateTelechargement=""
        self.telecharge=True
