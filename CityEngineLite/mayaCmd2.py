vtx=cmds.polyInfo(fv=True)
vtx=vtx[0].split()
vtx=vtx[2:]
vtxn=cmds.ls(sl=True,fl=True)
vtxc=[]
for v in vtxn:
	vtxc.append(cmds.xform(v,q=True,a=True,t=True,))

	



def getvtx():

	vtxn=cmds.ls(sl=True,fl=True)
	vtxc=[]
	for v in vtxn:
		vtxc.append(cmds.xform(v,q=True,a=True,t=True,))
	return vtxc





def applyTrans(scope):
	if isinstance(scope,CScope):
		if scope.parent is none:
			cmds.rotate(scope.orient[0],scope.orient[1],scope.orient[2],scope.shape)
			cmds.move(scope.position[0],scope.position[1],scope.position[2],scope.shape,os=True,r=True)

		elif isinstance(scope.parent,CScope):
			cmds.rotate(scope.orient[0],scope.orient[1],scope.orient[2],scope.shape)
			cmds.move(scope.position[0],scope.position[1],scope.position[2],scope.shape,os=True,r=True)	



class CShape:

	vtx=[]

	edge=[]

	face=[]

	D=0

	object=''

	def getT(self):

		pass

	def getR(self):

		pass

	def getS(self):

		pass

	def setT(self):

		pass

	def setR(self):

		pass

	def setS(self):

		pass





def extrudeEdge(d,edge,vtx):
	v=[]
	for i in range(0,3):
		v.append(vtx[edge[1]][i]-vtx[edge[0]][i])

	el=math.sqrt(math.pow(v[0],2)+math.pow(v[2],2))
	newpoly=cmds.polyCreateFacet( p=[(0.0, 0.0, 0.0), (1, 0.0, 0.0), (1,1,0.0),(0.0, 1, 0.0)] )
	#r1=math.degrees(math.acos(v[0]/el))
	r2=math.degrees(math.asin(-v[2]/el))	

	if v[0]>=0:
		r=r2
	else:
		if -v[2]>0:
			r=180-r2
		else:
			r=-180-r2

	

	cmds.scale(el,d,0,newpoly[0])
	cmds.move(vtx[edge[0]][0],vtx[edge[0]][1],vtx[edge[0]][2],newpoly[0])
	cmds.rotate(0,r,0,newpoly[0])
	return newpoly



def extrudeFace(d,vtx):

	#concept code

	vtx2=copy.deepcopy(vtx)
	vtx2=vtx2[1:]+vtx2[0]

	vl=len(vtx)
	vr=range(vl)
	edges=zip(vr,vr[1:]+[vr[0]])
	mface=[]
	for edge in edges:
		#side face
		mface.append(extrudeEdge(d,list(edge),vtx))
	#top face
	toppoly=cmds.polyCreateFacet( p=[tuple(x) for x in vtx] )
	cmds.move(0,d,0,toppoly[0],r=True)
	mface.insert(0,toppoly)
	#bottom face
	#mface.append(face)
	return mface





def me(d):
	vtx=getvtx()
	extrudeFace(d,vtx)

	








def cw(vtx):
	s=((vtx[0][0]-vtx[1][0])*(vtx[0][1]+vtx[1][1])+(vtx[1][0]-vtx[2][0])*(vtx[1][1]+vtx[2][1])+(vtx[2][0]-vtx[0][0])*(vtx[2][1]+vtx[0][1]))/2.0
	return s

	



def pointInTri(p,vtx):
	if cw([vtx[0],vtx[1],p])>0 and cw([vtx[1],vtx[2],p])>0 and cw([vtx[2],vtx[0],p])>0:
		return True
	
	elif cw([vtx[0],vtx[1],p])<0 and cw([vtx[1],vtx[2],p])<0 and cw([vtx[2],vtx[0],p])<0:
		return True

	else:
		return False

		

def pointInPoly(p,vtx):
	vtx2=copy.deepcopy(vtx)
	v0=[vtx2.pop(0)]
	dp=zip(vtx2[:-1],vtx2[1:])
	for dv in dp:
		if pointInTri(p,v0+list(dv)):
		#if point is in one of the sub-tri,then it is in the poly
			return True
	return False





def eval_T_in_maya(scope):
	print 'call eval T in maya'
	loc=cmds.spaceLocator()
	cmds.setAttr(loc[0]+'.translate',scope.position[0],scope.position[1],scope.position[2])
	cmds.setAttr(loc[0]+'.rotate',scope.orient[0],scope.orient[1],scope.orient[2])
	#cmds.setAttr(loc[0]+'.scale',scope.size[0],scope.size[1],scope.size[2])
	for t in scope.T:
		if t[0]=='T':
			if t[2][0]==t[2][1]==t[2]=='R':
				cmds.move(t[3][0],t[3][1],t[3][2],loc[0],r=True,os=True)
			elif t[2][0]==t[2][1]==t[2]=='A':
				cmds.move(t[3][0],t[3][1],t[3][2],loc[0])
			else:
				cmds.move(t[3][0],t[3][1],t[3][2],loc[0],r=True,os=True)

			

		elif t[0]=='R':
			if t[2][0]==t[2][1]==t[2]=='R':
				cmds.rotate(t[3][0],t[3][1],t[3][2],loc[0],r=True,os=True)
			elif t[2][0]==t[2][1]==t[2]=='A':
				cmds.rotate(t[3][0],t[3][1],t[3][2],loc[0])
			else:
				cmds.rotate(t[3][0],t[3][1],t[3][2],loc[0],r=True,os=True)

	return [cmds.getAttr(loc[0]+'.translate')[0],cmds.getAttr(loc[0]+'.rotate')[0]]


def assign_shape_in_maya(scope):
	newpoly=cmds.polyCreateFacet( p=[(0.0, 0.0, 0.0), (1, 0.0, 0.0), (1,1,0.0),(0.0, 1, 0.0)] )
	cmds.setAttr(newpoly[0]+'.translate',scope.position[0],scope.position[1],scope.position[2])
	cmds.setAttr(newpoly[0]+'.rotate',scope.orient[0],scope.orient[1],scope.orient[2])
	cmds.setAttr(newpoly[0]+'.scale',scope.size[0],scope.size[1],scope.size[2])







def facade(rule):
	gcurrentScope=CScope()
	gparentScope=CScope()
	myshape=CStructure()

	myshape.notations=[]
	myshape.symbols=[]
	myshape.predecessor=CScope()
	myshape.scopeStack=[]
	myshape.cmdList=[]
	myshape.subSymbols=[]
	myshape.usingMayaSpace=False
	

	f = open(rule,'r')
	text=f.readlines()
	for str in text:
		myshape.notations.append(parsingNotation(str))
	f.close()
	myshape.evaluate()
	myshape.assignShape()
	



facade('/Users/cobranail/Documents/workspace/mpy/src/tg3.txt')



import math

e=[1,2]

extrudeEdge(3,e,vtxc)