 # coding: utf8
 # Importations
from pyhdf.SD import *
import pyhdf.error 
from pyhdf.V import *
from pyhdf.HDF import *
from pyhdf.VS import *
import re
import numpy as np
import os
from modisSuite import logMod

Nom="modisSuite Compress"
def compress(*arg,**karg):
	# This function compress the file with a given compress parameter
	# compress(file,comression parameter)
	
	fileName=arg[0]
	
	try:
		log=karg["log"]
	except KeyError:
		log=logMod.Log("",nolog=True)
	
	
	# Open HDF file
	try:
		sd_id = SD(fileName, SDC.WRITE )
	except TypeError:
		sd_id = SD(fileName.encode('ascii','ignore'), SDC.WRITE )
	
	
	#open evry data set
	for dsname in list(sd_id.datasets().keys()):
		sds_id = sd_id.select(dsname)
		try:
			sds_id.setcompress(*arg[1])         # args depend on compression type
		except HDF4Error as msg:
			log.log('e',Nom,"Error compressing the dataset")
			sds_id.endaccess()
			sd_id.end()
			return
		
		sds_id.endaccess()

	# Close hdf file to flush compressed data.
	sd_id.end()
	return None
