#!/usr/bin/python3
# coding: utf8 

# Importations
import numpy as np


# Function to convert points
def cartToSin(xy,diameter):
	def conv(x,y,diameter):
		# Convert radient coordinates to sin
		phy=y/diameter
		lamb=x/diameter
		return (lamb*np.cos(phy),phy)
	if type(xy) == tuple:
		try:
			x,y = xy
		except ValueError:
			# Too much or not enough value in tupple
			return None
		return conv(x,y,diameter)
		
	elif type(xy) == list:
		lcon=[]
		for co in xy:
			try:
				x,y = co
			except ValueError:
				# Too much or not enough value in tupple
				return None
			lcon.append(conv(x,y,diameter))
		return lcon
def sinToCart(xy,diameter):
	def conv(x,y,diameter):
		# Convert radient sin to coordinates
		x/=(diameter)
		y/=(diameter)
		return (x/(np.cos(y)),y)
	if type(xy) == tuple:
		try:
			x,y = xy
		except ValueError:
			# Too much or not enough value in tupple
			return None
		return conv(x,y,diameter)
		
	elif type(xy) == list:
		lcon=[]
		for co in xy:
			try:
				x,y = co
			except ValueError:
				# Too much or not enough value in tupple
				return None
			lcon.append(conv(x,y,diameter))
		return lcon
   
def cooToPixel(xy,boundcoordinate,numPixel):
	return
