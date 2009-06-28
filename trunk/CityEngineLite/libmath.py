from math import *

def vectorMAngle(v):
	ang=0.0
	m=hypot(v[0],v[1])
	if v[0]==v[1]==0 or v[0]==v[1]==0.0:
		ang = 0.0
	else:
		v[0]=min(max(v[0]/m,-1),1)
		v[1]=min(max(v[1]/m,-1),1)
		if v[0]>=0 and v[1]>=0:
			ang = degrees(acos(v[0]/m))
		elif v[0]>=0 and v[1]<0:
			ang = degrees(asin(v[1]/m))+360
		elif v[0]<0 and v[1]>=0:
			ang = degrees(acos(v[0]/m))
		elif v[0]<0 and v[1]<0:
			ang = 360-degrees(acos(v[0]/m))
	
	return ang

def matrix_mutil(a,b):
	return [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]

def centerMAngle(v1,v2):
	return (vectorMAngle(v2)-vectorMAngle(v1))/2

def centerVector(v1,v2):
	a=radians(centerMAngle(v1,v2))
	return [v1[0]*cos(a)-v1[1]*sin(a), v1[0]*sin(a)+v1[1]*cos(a)]
	
def offsetDistant(ang,d):
	p=cos(ang-90)
	d2=d
	if p>0:
		d2=d/p
	return d2

def offsetVector(v1,v2,d):
	cv=centerVector(v1,v2)
	d2=offsetDistant(centerMAngle(v1,v2))
	return [v1[0]+d2*cv[0],v1[1]+d2*cv[1]]


	