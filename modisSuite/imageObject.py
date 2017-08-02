#!/usr/bin/python3
# coding: utf8 
import random
import os
import modisSuite as ms
class imageModis:
    def __init__(self,files,*arg,**args):
        self.files=files
    def returnHDF(self):
        ls=[]
        for f in self.files:
            if f.typ=="hdf":
                ls.append(f)
        return ls
    def mosaic(self,mosName=""):
        if mosName=="":
            mosName=os.path.join(os.path.dirname(self.files[0].path),'%f.hdf'%random.random())
        ms.mosaic(*[f.path for f in self.returnHDF()],mosName)
        return imageModis([Afile("","","","hdf",mosName),])
    def delete(self):
        for f in self.files:
            f.delete()
class Afile:
    def __init__(self,name,date,link,typ,path,*arg,**args):
        self.name=name
        self.date=date
        self.typ=typ
        self.link=link
        self.path=path
        self.size=0
        self.tile=0
        self.product=0
        self.dateTelechargement=""
        self.telecharge=True
    def delete(self):
        os.remove(self.path)
    def clip(self,clipName="",**args):
        if clipName=="":
            clipName=os.path.join(os.path.dirname(self.path),'%f.hdf'%random.random())
        ms.clip(self.path,clipName,pixel=args["pixel"])
        return Afile("","","","hdf",clipName)
    def subset(self,subName="",sublist=[],**args):
        if subName=="":
            subName=os.path.join(os.path.dirname(self.path),'%f.hdf'%random.random())
        ms.subset(self.path,subName,*sublist)
        return Afile("","","","hdf",subName)
    def compress(self,*args,**kargs):
        ms.compress(self.path,*args)
