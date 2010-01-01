from math import *

def vectorMAngle(v):
	ang=0.0
	v2=[0.0,0.0]
	m=hypot(v[0],v[1])
	if v[0]==v[1]==0 or v[0]==v[1]==0.0:
		ang = 0.0
	else:
		v2[0]=min(max(v[0]/m,-1),1)
		v2[1]=min(max(v[1]/m,-1),1)
		if v2[0]>=0 and v2[1]>=0:
			ang = degrees(acos(v2[0]))
		elif v2[0]>=0 and v2[1]<0:
			ang = degrees(asin(v2[1]))+360
		elif v2[0]<0 and v2[1]>=0:
			ang = degrees(acos(v2[0]))
		elif v2[0]<0 and v2[1]<0:
			ang = 360-degrees(acos(v2[0]))
	
	return ang

def matrix_mutil(a,b):
	return [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]

def centerMAngle(v1,v2):
	a1=vectorMAngle(v1)
	a2=vectorMAngle(v2)
	
	if a2<a1:
		a2+=360
	ca=(a2-a1)/2
	return ca

def centerVector(v1,v2):
	a=radians(centerMAngle(v1,v2))
	return [v1[0]*cos(a)-v1[1]*sin(a), v1[0]*sin(a)+v1[1]*cos(a)]
	
def offsetDistant(ang,d):
	p=cos(radians(ang-90))
	d2=d
	if p>0:
		d2=d/p
	return d2

def offsetVector(v1,v2,d):
	cv=centerVector(v1,v2)
	d2=offsetDistant(centerMAngle(v1,v2),d)
	a=radians(vectorMAngle(cv))
	return [cos(a)*d2,sin(a)*d2]


	