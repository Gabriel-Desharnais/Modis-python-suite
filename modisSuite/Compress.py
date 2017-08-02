 # Importations
from pyhdf.SD import *
import pyhdf.error 
from pyhdf.V import *
from pyhdf.HDF import *
from pyhdf.VS import *
import re
import numpy as np
import os



def compress(*arg,**karg):
	# This function compress the file with a given compress parameter
	# compress(file,comression parameter)
	
	fileName=arg[0]
	
	# Open HDF file
	sd_id = SD(fileName, SDC.WRITE )
	
	
	#open evry data set
	for dsname in list(sd_id.datasets().keys()):
		sds_id = sd_id.select(dsname)
		try:
			sds_id.setcompress(*arg[1])         # args depend on compression type
		except HDF4Error as msg:
			print(("Error compressing the dataset with params: "
					"(%d,%d,%d) : %s" % (arg[1]+(msg,))))
			sds_id.endaccess()
			sd_id.end()
			return
		
		sds_id.endaccess()

	# Close hdf file to flush compressed data.
	sd_id.end()
	return None
