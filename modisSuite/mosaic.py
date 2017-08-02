# coding: utf8
# Importations
from pyhdf.SD import *
import pyhdf.error 
from pyhdf.V import *
from pyhdf.HDF import *
from pyhdf.VS import *
import re
import numpy as np
from modisSuite import logMod

Nom="modisSuite Mosaic"
# Defining the class to manage attributes from the HDF file
class atribute:
	def __init__(self,raw,name=""):
		self.name=name
		self.raw=raw
		self.GROUP={}
		self.OBJECT={}
		self.variable={}
		colect=""
		colecting=False
		end=""
		lines=self.raw.split('\n')
		progb=re.compile('GROUP=[A-Za-z_0-9]{1,}')
		proge=re.compile('END_GROUP=[A-Za-z_0-9]{1,}')
		progob=re.compile('OBJECT=[A-Za-z_0-9]{1,}')
		progoe=re.compile('END_OBJECT=[A-Za-z_0-9]{1,}')
		for line in lines:
			#Add group
			b=progb.findall(line)
			e=proge.findall(line)
			ob=progob.findall(line)
			oe=progoe.findall(line)
			if (len(e)==0 and len(b)>0) and (not colecting):
				# Begin collecting
				colecting=True
				colect=""
				end=b[0]
				#print(type(e),type(b),type(line))
			elif (len(oe)==0 and len(ob)>0) and (not colecting):
				# Begin collecting
				colecting=True
				colect=""
				end=ob[0]
				#print(type(e),type(b),type(line))
			elif len(e)>0 and len(b)>0 and line.find(end)>-1:
				colecting=False
				# End collecting
				name=end.split("=")[-1]
				self.GROUP[name]=atribute(colect)
			elif len(oe)>0 and len(ob)>0 and line.find(end)>-1:
				colecting=False
				# End collecting
				name=end.split("=")[-1]
				self.OBJECT[name]=atribute(colect)
			elif colecting:
				# Collecting
				# print(line)
				colect+=line+"\n"
			elif  len(b)==0 and len(ob)==0:
				# adding to variable
				try:
					#print(line)
					self.variable[line.split("=")[0].strip()]=line.split("=")[1]
				except IndexError:
					pass
			
	def listgrid(self):
	# list the grids in the group
		try:
			gs=self.GROUP["GridStructure"]
			gg=list(gs.GROUP.keys())
			return len(gg),gg
		except KeyError:
			return -1,[]
	def listgridname(self):
		# list the grids name in the group
		try:
			gs=self.GROUP["GridStructure"]
			gg=[gs.GROUP[x].variable["GridName"] for x in gs.GROUP]
			return len(gg),gg
		except KeyError:
			return -1,[]
	def listdataset(self):
		#Aller chercher les grids
		gr=self.listgrid()[1]
		ds=[]
		for g in gr:
			ds+=list(self.GROUP["GridStructure"].GROUP[g].GROUP["DataField"].OBJECT.keys())
		return ds
	def listdatasetbyname(self):
		#get ds by name
		gr=self.listgrid()[1]
		ds=[]
		for g in gr:
			dsg=self.GROUP["GridStructure"].GROUP[g].GROUP["DataField"].OBJECT
			ds+=[dsg[x].variable["DataFieldName"] for x in dsg]
		return ds
	def getgridbyname(self,name):
		gs=self.GROUP["GridStructure"]
		for x in gs.GROUP:
			if gs.GROUP[x].variable["GridName"] == name:
				return gs.GROUP[x]
		return None 
	def __str__(self):
		st=""
		# Ajouter les variables
		for x in self.variable:
			st+=x+"="+self.variable[x]+"\n"
		# Ajouter les group
		
		for x in self.GROUP:
			st+="GROUP="+x+"\n"
			
			gg=str(self.GROUP[x]).split("\n")
			gg.remove("")
			st+="\n".join(["\t"+h for h in gg])+"\n"
			st+="END_GROUP="+x+"\n"
		# Ajouter les object
		for x in self.OBJECT:
			st+="OBJECT="+x+"\n"
			gg=str(self.OBJECT[x]).split("\n")
			gg.remove("")
			st+="\n".join(["\t"+h for h in gg])+"\n"
			st+="END_OBJECT="+x+"\n"
		return st
        
        





def mosaic(*arg,**args):
	# This function will take files tranfered in *arg and will mosaic them together and produce a new file
	# mosaic(file1,[file2,file3,...],endfile)
	# If only file1 and endfile is given, the function will only produce a copy without any other modification
	try:
		log=args["log"]
	except KeyError:
		log=logMod.Log("",nolog=True)
	if len(arg)>2:
		lfile = arg[:-1]				# This is the list of the NAME of the files to merge
		newfilename = arg[-1]			# This is the final file NAME
		# Should eventually check if files exists and can be read ***IMPROVE***
		lfHDF = []						# This is the list of the FILES to merge
		latt = []							# This is the list of the ATTRIBUTE "StructMetadata.0" of the files
		for fil in lfile:
			try:
				a=SD(fil,SDC.READ)
			except TypeError:
				a=SD(fil.encode('ascii','ignore'),SDC.READ)
			lfHDF.append(a)
			latt.append(atribute(lfHDF[-1].attributes()["StructMetadata.0"],fil))
			
		
		
		## Listing all the GRIDS that the new file will have
		gridlist = []						# This is the list of GRIDS to include in the final file

		for attOfF in latt:
			# Should check if any grid ***IMPROVE***
			gridlist += attOfF.listgridname()[1]		# listgridname return a list of all the grids name

		# remove double entry
		gridlist = list(set(gridlist))


		## Listing all the DATASETS that the new file will have
		dslist = []						# This is the list of DATASETS to include in the final file
		for attOfF in latt:
			# Should check if any grid ***IMPROVE***
			dslist += attOfF.listdatasetbyname()
			
		# remove double entry
		dslist = list(set(dslist))


		
		## Validation of commoun information
###############################################################################
# Some informations have to be the same for each file or else no mosaic can   #
# be made for exemple two files with not the same projection type can't be    #
# merged together. ***IMPROVE*** Maybe in the future we could transform file  #
# so that they have the same projection or some other thing.                  #
###############################################################################

		# List of parameter to check to insure that they are the same
		paramMustSim = ["Projection","ProjParams","SphereCode","GridOrigin"]
		# Dictionary that will keep all the informations about every file
		paramMustSimDict = {}

		for grid in gridlist:
			# Verification of a grid

			first = True			# Variable that will enable the construction of the dict
			paramdict = {}		# Dictionary that keep the actual value that have to be the same
			
			for attOfF in latt:
				# Verification of a file
				bigG = attOfF.getgridbyname(grid)		# Getting all the attributes in the grid of a file
				if bigG is not None:
					# If the grid exists in that file
					if first :
						# If this is the first time that a file is check for that grid
						first = False
						for p in paramMustSim:
							# Checking every parameters that must be the same
							paramdict[p] = bigG.variable[p]
							
						# Validation of same Dtype for each datafield
						go = bigG.GROUP["DataField"].OBJECT
						for r in go:
							paramdict[go[r].variable["DataFieldName"]]=go[r].variable["DataType"]
					else:
						# If it's not the first time that a file is check for that grid
						for p in paramMustSim:
							# Checking every parameters that must be the same
							if not paramdict[p]==bigG.variable[p]:
								# Stop merging and return error ***IMPROVE*** 
								# Maybe do only the things that can be done ***IMPROVE***
								log.log('e',Nom,"Error dataset are not compatible")
								
						# Validation of same Dtype for each datafield
						go=bigG.GROUP["DataField"].OBJECT
						for r in go:
							if not paramdict[go[r].variable["DataFieldName"]]==go[r].variable["DataType"]:
								# Stop merging and return error ***IMPROVE*** 
								# Maybe do only the things that can be done ***IMPROVE***
								log.log('e',Nom,"Error dataset are not compatible")
								
			# Keep all this info for later it's going to be useful
			paramMustSimDict[grid]=paramdict
				
				



		## Determination of new informations
###############################################################################
# Some properties have to be calculated in order to merge. This section is    #
# doing just that                                                             #
###############################################################################

		gridResolX={}			# Getting the RESOLUTION in the X direction for each grid
		gridResolY={}			# Getting the RESOLUTION in the Y direction for each grid
		extremeup={}			# Getting the UPPER coordinates for each grid
		extremedown={}			# Getting the LOWEST coordinates for each grid
		extremeleft={}			# Getting the LEFTMOST coordinates for each grid
		extremeright={}			# Getting the RIGHTMOST coordinates for each grid
		gridDimX={}				# Getting the DIMENSIONS of X direction for each grid
		gridDimY={}				# Getting the DIMENSIONS of Y direction for each grid
		NoValueDS={}			# Getting the fill value of each dataset
		dtypeDS={}				# Getting the DTYPE for each dataset
		dstogrid={}				# Knowing wich is the GRID for each dataset
		filGridULC={}			# Getting the upper left corner of each file for each grid

		for grid in gridlist:
			# For each grid
			filGridULC[grid]={}			# Adding a dictionary for each grid that will contain information on every file
			for attOfF in latt:
				### Determination of resolution of each grid
				# ***IMPROVE*** Should check if bigd is none
				bigG=attOfF.getgridbyname(grid)				# Getting all the attributes in the grid of a file
				
				# Get extreme grid point
				ulp=eval(bigG.variable["UpperLeftPointMtrs"])
				lrp=eval(bigG.variable["LowerRightMtrs"])
				
				# Get grid dimmension
				dimx=int(bigG.variable["XDim"])
				dimy=int(bigG.variable["YDim"])
				
				# Calculate grid resolution
				gridResolX[grid]=(lrp[0]-ulp[0])/dimx
				gridResolY[grid]=(ulp[1]-lrp[1])/dimy
				
				### Determination of new extreme coordinates for each grid
				# up
				try:
					if extremeup[grid]< ulp[1]:
						extremeup[grid]=ulp[1]
				except KeyError:
					extremeup[grid]=ulp[1]
				# down
				try:
					if extremedown[grid]> lrp[1]:
						extremedown[grid]=lrp[1]
				except KeyError:
					extremedown[grid]=lrp[1]
				# left
				try:
					if extremeleft[grid]> ulp[0]:
						extremeleft[grid]=ulp[0]
				except KeyError:
					extremeleft[grid]=ulp[0]
				# right
				try:
					if extremeright[grid]< lrp[0]:
						extremeright[grid]=lrp[0]
				except KeyError:
					extremeright[grid]=lrp[0]
				### Detetermination of dataset to grid name
				if bigG is not None:
					go=bigG.GROUP["DataField"].OBJECT
					for r in go:
						dstogrid[ go[r].variable["DataFieldName"] ] = grid
				## Determination of ULC for each grid in each file
				filGridULC[grid][attOfF.name] = ulp
			## determination of new dimension for each grid
			gridDimY[grid] = int((extremeup[grid]-extremedown[grid])/gridResolY[grid])
			gridDimX[grid] = int((extremeright[grid]-extremeleft[grid])/gridResolX[grid])

		for ds in dslist:
			# For each dataset
			for sd in lfHDF:
				# For each hdf file
				
				# Try opening dataset
				try:
					sds = sd.select(eval(ds))
					# Get fill value
					NoValueDS[ds] = sds.getfillvalue()
					# Get dtype
					dtypeDS[ds] = sds.info()[3]
				except:
					log.log('e',Nom,"no dataset")



		## Start creating new file
###############################################################################
# This is the actual part were stuf appens                                    #
###############################################################################

		# This part is the same for every file in any circumstances
		########## absolute ########################
		
		# Open new file
		try:
			hdf = HDF(newfilename, HC.WRITE  | HC.CREATE  |HC.TRUNC)
			sd  =  SD(newfilename, SDC.WRITE | SDC.CREATE )
		except TypeError:
			hdf = HDF(newfilename.encode('ascii','ignore'), HC.WRITE  | HC.CREATE  |HC.TRUNC)
			sd  =  SD(newfilename.encode('ascii','ignore'), SDC.WRITE | SDC.CREATE )
		
		v=hdf.vgstart()
		vg={}
		vg1={}
		vg2={}
		for grid in gridlist:
			vg[grid]=v.attach(-1,write=1)
			vg[grid]._class="GRID"
			vg[grid]._name=eval(grid)
			vg1[grid]=v.attach(-1,write=1)
			vg2[grid]=v.attach(-1,write=1)
			vg1[grid]._class="GRID Vgroup"
			vg1[grid]._name="Data Fields"
			vg2[grid]._class="GRID Vgroup"
			vg2[grid]._name="Grid Attributes"
			vg[grid].insert(vg1[grid])
			vg[grid].insert(vg2[grid])
		########## absolute ########################


		# Create dataset with the right size
		for ds in dslist:
			theGrid=dstogrid[ds]
			# Get grid name of data set
			sds = sd.create(eval(ds),dtypeDS[ds],(gridDimY[theGrid],gridDimX[theGrid]))
			
			# Set fill value
			fv=NoValueDS[ds]
			try:
				sds.setfillvalue(NoValueDS[ds])
			except OverflowError:
				log.log('e',Nom,"setfillvalue")
				sds.setfillvalue(0)
			## write real data
			for fil in range(len(latt)):
				try:
					# Determine were the data will be writen
					ulc = filGridULC[theGrid][latt[fil].name]
					# Determine the position on the grid
					y = (extremeup[theGrid]-ulc[1])/(extremeup[theGrid]-extremedown[theGrid])
					x = (ulc[0]-extremeleft[theGrid])/(extremeright[theGrid]-extremeleft[theGrid])
					y = int(y*gridDimY[theGrid])
					x = int(x*gridDimX[theGrid])
					# read data from files
					osds = lfHDF[fil].select(eval(ds))
					sh = osds[:].shape
					sds[y:y+sh[0],x:x+sh[1]] = osds[:]
					osds.endaccess()
				except:
					pass
			# Close sds
			vg1[dstogrid[ds]].add(HC.DFTAG_NDG,sds.ref())
			sds.endaccess()


    
		for g in vg1:
			vg1[g].detach()
			vg2[g].detach()
			vg[g].detach()

		# Create attribute table for the file
		attstr="GROUP=GridStructure\n"
		gridcount=1
		for gr in gridlist:
			# Start group grid
			attstr+="\tGROUP=GRID_%i\n"%gridcount
			# Add grid name
			attstr+="\t\tGridName=%s\n"%gr
			# Add dimention
			attstr+="\t\tXDim=%i\n"%gridDimX[gr]
			attstr+="\t\tYDim=%i\n"%gridDimY[gr]
			# Add UpperLeftPointMtrs
			attstr+="\t\tUpperLeftPointMtrs=(%f,%f)\n"%(extremeleft[gr],extremeup[gr])
			# Add lrp
			attstr+="\t\tLowerRightMtrs=(%f,%f)\n"%(extremeright[gr],extremedown[gr])
			# Add projection
			attstr+="\t\tProjection=%s\n"%paramMustSimDict[gr]["Projection"]
			# ProjParams
			attstr+="\t\tProjParams=%s\n"%paramMustSimDict[gr]["ProjParams"]
			# SphereCode
			attstr+="\t\tSphereCode=%s\n"%paramMustSimDict[gr]["SphereCode"]
			# GridOrigin
			attstr+="\t\tGridOrigin=%s\n"%paramMustSimDict[gr]["GridOrigin"]
			
			attstr+="""\t\tGROUP=Dimension
		\t\tEND_GROUP=Dimension
		\t\tGROUP=DataField\n"""

			## Add data sets
			# create list of ds for current grid
			lsdsgr=[]
			dsnum=1
			for ds in dstogrid:
				if dstogrid[ds] == gr:
					# Add object
					attstr+="\t\t\tOBJECT=DataField_%i\n"%dsnum
					# datafield name
					attstr+="\t\t\t\tDataFieldName=%s\n"%ds
					# datatype
					attstr+="\t\t\t\tDataType=%s\n"%paramMustSimDict[gr][ds]
					# dim
					attstr+='\t\t\t\tDimList=("YDim","XDim")\n'
					attstr+="\t\t\tEND_OBJECT=DataField_%i\n"%dsnum
					dsnum+=1
			attstr+="\t\tEND_GROUP=DataField\n"
			attstr+="""\t\tGROUP=MergedFields
		\t\tEND_GROUP=MergedFields\n"""
			attstr+="\tEND_GROUP=GRID_%i\n"%gridcount
			gridcount+=1
		attstr+="""END_GROUP=GridStructure
		GROUP=PointStructure
		END_GROUP=PointStructure
		END"""
		# adding attribute to new file
		att=sd.attr('StructMetadata.0')
		att.set(SDC.CHAR,attstr)
		sd.end()
		hdf.close()
		
		# This should return something somehow
	
