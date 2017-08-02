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
        arg=[f.path for f in self.returnHDF()]+[mosName,]
        ms.mosaic(*arg)
        return imageModis([Afile("","","","hdf",mosName),])
    def clip(self,pixel=(0,0)):
        return imageModis([f.clip(pixel=pixel) for f in self.files])
    def subset(self,sublist=[]):
        return imageModis([f.subset(sublist=sublist) for f in self.files])
    def compress(self,*args,**kargs):
        return imageModis([f.compress(*args) for f in self.files])
    def delete(self):
        for f in self.files:
            f.delete()
    def move(self,newfolder):
        for f in self.files:
            f.move(newfolder)
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
    def move(self,newfolder):
        newpath=os.path.join(newfolder,os.path.basename(self.path))
        os.rename(self.path,newpath)
        self.path=newpath
    # Should add copy function
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
        ms.compress(self.path,args)
