def getvtx(polyface):
	vss=cmds.polyInfo(polyface,fv=True)[0].split()[2:]
	m=polyface.split('.')[0]
	vtxc=[]
	for v in vss:
		vtxc.append(cmds.xform(m+'.vtx['+v+']',q=True,ws=True,a=True,t=True))
	return vtxc

def getvtx_local(polyface):
	vss=cmds.polyInfo(polyface,fv=True)[0].split()[2:]
	m=polyface.split('.')[0]
	vtxc=[]
	for v in vss:
		vtxc.append(cmds.xform(m+'.vtx['+v+']',q=True,t=True))
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
	return [newpoly,[vtx[edge[0]][0],vtx[edge[0]][1],vtx[edge[0]][2]],[0,r,0],[el,d,0]]



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
	mface.insert(0,[toppoly,[0,d,0],[0,0,0],[1,1,1]])
	#bottom face
	#mface.append(face)
	return mface


def vec2rad(vec1,vec2):
	d1=math.sqrt(float(vec1[0]**2+vec1[1]**2+vec1[2]**2))
	d2=math.sqrt(float(vec2[0]**2+vec2[1]**2+vec2[2]**2))
	if d1==0.0 or d2==0.0:
		return 0.0
	else:
		v=float(vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2])/d1/d2
		return math.acos( min(max(v,-1),1) )
		#1.0 is larger than 1, and math.acos well result 'nan'

def veccross(v1,v2):
	return v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v2[2]*v1[0],v1[0]*v2[1]-v1[1]*v2[0]

def testrot():
	fns=cmds.polyInfo(fn=True)
	fn2=fns[0].split()[2:]
	fn=[]
	for n in fn2:
		fn.append(float(n))
	ry=math.degrees(vec2rad([fn[0],0,fn[2]],[0,0,1.0]))
	rx=math.degrees(vec2rad(fn,[fn[0],0,fn[2]]))
	
	if fn[1]>0:
		rx=-rx
	if fn[0]<0:
		ry=-ry
	print 'y rot:',ry
	print 'x rot:',rx

def calc_rot_xy(fn2):
	pn=[0,0,1.0]
	fn=[]
	for n in fn2:
		fn.append(float(n))
	ry=math.degrees(vec2rad([fn[0],0,fn[2]], pn))
	rx=math.degrees(vec2rad(fn,[fn[0],0,fn[2]]))
	
	if fn[1]>0:
		rx=-rx
	if fn[0]<0:
		ry=-ry
	return ry,rx

def calc_rot_xy2(fn2):
	pn=[0,1.0,0]
	fn=[]
	for n in fn2:
		fn.append(float(n))
	
	if fn[0]==0.0 and fn[2]==0.0:
		ry,rx=0,0
	else:
		ry=math.degrees(vec2rad([fn[0],0,fn[2]], [0,0,-1.0]))
		rx=math.degrees(-vec2rad(fn,pn))
	return ry,rx

def sumseq(seq):
	def add(x,y): return x+y
	return reduce(add, seq, 0)

def center_point(vtx):
	x=sumseq([v[0] for v in vtx])/len(vtx)
	y=sumseq([v[1] for v in vtx])/len(vtx)
	z=sumseq([v[2] for v in vtx])/len(vtx)
	return [x,y,z]

def orig_point(vtx,fn):
	
	vd=veccross(fn,[0,0,1])
	cp=center_point(vtx)
	
	bottom_vtx=[]
	
	for v in vtx:
		if v[1]<cp[1]:
			bottom_vtx.append(v)
	
	bcp=center_point(bottom_vtx)
	
	for v in bottom_vtx:
		if sign(v[0]-bcp[0])==sign(vd[0]) and sign(v[2]-bcp[2])==sign(vd[2]) and v[1]<bcp[1]:
			return v

def new_sideface(vtx,fn):
	fn=veccross([vtx[1][0]-vtx[0][0],vtx[1][1]-vtx[0][1],vtx[1][2]-vtx[0][2]],[vtx[2][0]-vtx[1][0],vtx[2][1]-vtx[1][1],vtx[2][2]-vtx[1][2]])
	r=calc_rot_xy(fn)
	print 'r',r
	vtx2=[]
	vtx3=[]
	for v in vtx:
		v2=rot(v,'y',r[0])
		v3=rot(v2,'x',r[1])
		vtx2.append(v3)
	#print 'vtx2',vtx2
	bound=get_bound(vtx2)
	#print 'bound',bound
	xl=bound[1]-bound[0]
	yl=bound[3]-bound[2]
	zl=bound[5]-bound[4]
	
	for v in vtx2:
		v2=[(v[0]-bound[0])/xl,(v[1]-bound[2])/yl,0]
		vtx3.append(v2)	
	newface=cmds.polyCreateFacet( p=[tuple(x) for x in vtx3] ,ch=False)
	cmds.setAttr(newface[0]+'.visibility',False)
	cmds.setAttr(newface[0]+'.scale',xl,yl,1)
	
	cmds.setAttr(newface[0]+'.rotate',r[1],r[0],0)
	rp=cmds.xform(newface[0]+'.vtx[0]',q=True,ws=True,a=True,t=True)
	
	cmds.setAttr(newface[0]+'.translate',vtx[0][0]-rp[0],vtx[0][1]-rp[1],vtx[0][2]-rp[2])
	return [newface,[vtx[0][0]-rp[0],vtx[0][1]-rp[1],vtx[0][2]-rp[2]],[r[1],r[0],0],[xl,yl,1],vtx3]

def new_topface(vtx,fn):	
	r=calc_rot_xy2(fn)
	print 'r',r
	vtx2=[]
	vtx3=[]
	for v in vtx:
		v2=rot(v,'y',r[0])
		v3=rot(v2,'x',r[1])
		vtx2.append(v3)
	#print 'vtx2',vtx2
	bound=get_bound(vtx2)
	#print 'bound',bound
	xl=bound[1]-bound[0]
	yl=bound[3]-bound[2]
	zl=bound[5]-bound[4]
	
	for v in vtx2:
		v2=[(v[0]-bound[0])/xl,0,(v[2]-bound[4])/zl]
		vtx3.append(v2)	
	newface=cmds.polyCreateFacet( p=[tuple(x) for x in vtx3] ,ch=False)
	cmds.setAttr(newface[0]+'.visibility',False)
	cmds.setAttr(newface[0]+'.scale',xl,1,zl)
	
	cmds.setAttr(newface[0]+'.rotate',r[1],r[0],0)
	rp=cmds.xform(newface[0]+'.vtx[0]',q=True,ws=True,a=True,t=True)
	
	cmds.setAttr(newface[0]+'.translate',vtx[0][0]-rp[0],vtx[0][1]-rp[1],vtx[0][2]-rp[2])
	return [newface,[vtx[0][0]-rp[0],vtx[0][1]-rp[1],vtx[0][2]-rp[2]],[r[1],r[0],0],[xl,1,zl],vtx3]

def offset_vtx(vtx,d):
	vo=zip([vtx[-1]]+vtx[:-1],vtx,vtx[1:]+[vtx[0]])
	nv3d=[]
	if is2Dvtxs(vtx,'XY'):
		for vp in vo:
			nv2d=offsetVector([vp[0][0]-vp[1][0],vp[0][1]-vp[1][1]],[vp[2][0]-vp[1][0],vp[2][1]-vp[1][1]],d)
			nv3d.append([nv2d[0]+vp[1][0],nv2d[1]+vp[1][1],0.0])
	elif is2Dvtxs(vtx,'XZ'):
		for vp in vo:
			nv2d=offsetVector([vp[0][0]-vp[1][0],vp[0][2]-vp[1][2]],[vp[2][0]-vp[1][0],vp[2][2]-vp[1][2]],d)
			nv3d.append([nv2d[0]+vp[1][0],0.0,nv2d[1]+vp[1][2]])
	return nv3d

def offset_face_in_maya(scope,d):
	if scope.shape!='':
		r0=cmds.getAttr(scope.shape+'.rotate')[0]
		t0=cmds.getAttr(scope.shape+'.translate')[0]
		t01=cmds.xform(scope.shape+'.vtx[0]',q=True,a=True,ws=True,t=True)
		cmds.setAttr(scope.shape+'.translate',0,0,0)
		cmds.setAttr(scope.shape+'.rotate',0,0,0)
		vtxs0=getvtx(scope.shape+'.f[0]')
		cmds.delete(scope.shape)
		bound0=get_bound(vtxs0)
		vtxs0a=[]		
		if is2Dvtxs(vtxs0,'XY'):
			p='XY'
		elif is2Dvtxs(vtxs0,'XZ'):
			p='XZ'
			for vtx in vtxs0:
				vtxs0a.append([vtx[2],vtx[0],vtx[1]])
			vtxs0=copy.deepcopy(vtxs0a)
			vtxs0a=[]
		
				
		vtxs1=offset_vtx(vtxs0,d)
		
		if p=='XZ':
			for vtx in vtxs1:
				vtxs0a.append([vtx[1],vtx[2],vtx[0]])
			vtxs1=copy.deepcopy(vtxs0a)
			vtxs0a=[]
		
		bound=get_bound(vtxs1)
		#print 'bound',bound
		xl=float(bound[1]-bound[0])
		yl=float(bound[3]-bound[2])
		zl=float(bound[5]-bound[4])
		vtxs2=[]
		vtxs3=[]
		if p=='XY':
			for v in vtxs1:
				vtxs2.append([(v[0]-bound[0])/xl,(v[1]-bound[2])/yl,0])
				vtxs3.append([v[0]/xl,v[1]/yl,0])
		elif p=='XZ':
			for v in vtxs1:
				vtxs2.append([(v[0]-bound[0])/xl,0,(v[2]-bound[4])/zl])
				vtxs3.append([v[0]/xl,0,v[2]/zl])
				
		newface0=cmds.polyCreateFacet( p=[tuple(x) for x in vtxs3] ,ch=False)		
		newface=cmds.polyCreateFacet(n=scope.shape, p=[tuple(x) for x in vtxs2] ,ch=False)
		cmds.setAttr(newface[0]+'.visibility',False)
		if p=='XY':
			cmds.setAttr(newface0[0]+'.scale',xl,yl,1)
			cmds.setAttr(newface[0]+'.scale',xl,yl,1)
		elif p=='XZ':
			cmds.setAttr(newface0[0]+'.scale',xl,1,zl)
			cmds.setAttr(newface[0]+'.scale',xl,1,zl)
		
		cmds.setAttr(newface0[0]+'.rotate',r0[0],r0[1],0)
		cmds.setAttr(newface[0]+'.rotate',r0[0],r0[1],0)
		
		cmds.setAttr(newface0[0]+'.translate',t0[0],t0[1],t0[2])	
		rp0=cmds.xform(newface0[0]+'.vtx[0]',q=True,ws=True,a=True,t=True)
		rp=cmds.xform(newface[0]+'.vtx[0]',q=True,ws=True,a=True,t=True)
		
		cmds.setAttr(newface[0]+'.translate',rp0[0]-rp[0],rp0[1]-rp[1],rp0[2]-rp[2])
		cmds.delete(newface0[0])
		
		if p=='XY':
			return [newface,[rp0[0]-rp[0],rp0[1]-rp[1],rp0[2]-rp[2]],[r0[1],r0[0],0],[xl,yl,1],vtxs2]
		elif p=='XZ':
			return [newface,[rp0[0]-rp[0],rp0[1]-rp[1],rp0[2]-rp[2]],[r0[1],r0[0],0],[xl,1,zl],vtxs2]	
			
		

def get_bound(vtx):
	print vtx
	x=[vtx[0][0],vtx[0][0]]
	y=[vtx[0][1],vtx[0][1]]
	z=[vtx[0][2],vtx[0][2]]
	for v in vtx:
		if v[0]<x[0]:
			x[0]=v[0]
		elif v[0]>x[1]:
			x[1]=v[0]
		
		if v[1]<y[0]:
			y[0]=v[1]
		elif v[1]>y[1]:
			y[1]=v[1]
			
		if v[2]<z[0]:
			z[0]=v[2]
		elif v[2]>z[1]:
			z[1]=v[2]
	
	return x+y+z

def matrix_mutil(a,b):
	return [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]



def rot(v,ax,deg):
	rad=math.radians(deg)
	if ax=='x':
		a=[[1,0,0],[0,cos(rad),sin(rad)],[0,-sin(rad),cos(rad)]]
	elif ax=='y':
		a=[[cos(rad),0,-sin(rad)],[0,1,0],[sin(rad),0,cos(rad)]]
	elif ax=='z':
		a=[[cos(rad),sin(rad),0],[-sin(rad),cos(rad),0],[0,0,1]]
		
	b=[[v[0]],[v[1]],[v[2]]]
	r=matrix_mutil(a,b)
	'''
	for i in [0,1,2]:
		if -0.0000000000000001<r[i][0]<0.0000000000000001:
			r[i][0]=0
	'''		
	return [r[0][0],r[1][0],r[2][0]]



'''
I suggest using a linear algebra package, but if you insist in using lists
> of lists:
>
> >>> b = [[1, 2, 3,  4],
> ...      [4, 5, 6,  7],
> ...      [7, 8, 9, 10]]
> >>>
> >>> a = [[1, 2, 3],
> ...      [4, 5, 6]]
> >>>
> >>> ab = [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]
> >>> ab
> [[30, 36, 42, 48], [66, 81, 96, 111]]
>
> Straightforward from the definition of matrix multiplication.
'''
def normal_vec(v):
	m=math.sqrt(float(v[0]**2+v[1]**2+v[2]**2))
	return [max(-1,min(1,v[0]/m)), max(-1,min(1,v[1]/m)) , max(-1,min(1,v[2]/m)) ]

def get_faces_in_maya(scope,type):
	global gcurrentScope
	faces=[]
	
	faceCount=cmds.polyEvaluate( [scope.shape], f=True )
	tagfaces=[]
	
	if type=='sidefaces':
		for i in xrange(faceCount):
			fns=cmds.polyInfo(scope.shape+'.f['+str(i)+']',fn=True)
			fn=fns[0].split()[2:]
			fn3=[float(fn[0]), float(fn[1]),float(fn[2])]
			fn4=normal_vec(fn3)
			if -0.99<=math.fabs(fn4[1])<=0.99:
				tagfaces.append(scope.shape+'.f['+str(i)+']')
				vtx=getvtx(scope.shape+'.f['+str(i)+']')
				newpoly=new_sideface(vtx,fn4)
				faces.append(newpoly)
	elif type=='topfaces':
		for i in xrange(faceCount):
			fns=cmds.polyInfo(scope.shape+'.f['+str(i)+']',fn=True)
			fn=fns[0].split()[2:]
			fn3=[float(fn[0]), float(fn[1]),float(fn[2])]
			fn4=normal_vec(fn3)
			if 1.0>=fn4[1]>0.99:
				tagfaces.append(scope.shape+'.f['+str(i)+']')
				vtx=getvtx(scope.shape+'.f['+str(i)+']')
				newpoly=new_topface(vtx,fn4)
				faces.append(newpoly)
	elif type=='bottomfaces':
		for i in xrange(faceCount):
			fns=cmds.polyInfo(scope.shape+'.f['+str(i)+']',fn=True)
			fn=fns[0].split()[2:]
			fn3=[float(fn[0]), float(fn[1]),float(fn[2])]
			fn4=normal_vec(fn3)
			if -1.0<=fn4[1]<-0.99:
				tagfaces.append(scope.shape+'.f['+str(i)+']')
				vtx=getvtx(scope.shape+'.f['+str(i)+']')
				newpoly=new_topface(vtx,fn4)
				faces.append(newpoly)
			
	return faces

def testnf():
	
	s=cmds.ls(sl=True,fl=True)
	fns=cmds.polyInfo(fn=True)
	fn2=fns[0].split()[2:]
	fn3=[float(fn2[0]), float(fn2[1]),float(fn2[2])]
	print 'fn is ',fn3
	poly=s[0].split('.')[0]
	vss=cmds.polyInfo(fv=True)[0].split()[2:]
	vtxc=[]
	for v in vss:
		vtxc.append(cmds.xform(poly+'.vtx['+v+']',q=True,ws=True,a=True,t=True))
	
	print 'vtxc',vtxc
	new_topface(vtxc,fn3)

def extrude_face_in_maya(shape,d):
	vtx=getvtx(shape)
	faces=extrudeFace(d,vtx)
	#print 'g faces:',len(faces),faces
	return faces

def extrude_in_maya(shape,d,param):
	off=0.0
	if 'F' in param[0]:
		off=eval(param[-1])
	cmds.polyExtrudeFacet(shape, kft=True,ws=False, ltz=d,offset=off) 
	if 'D' in param[0]:
		cmds.delete(shape+'.f[1]')
		
def deactive_shape_in_maya(scopes):
	for scope in scopes:
		if scope.shape!=''and cmds.objExists(scope.shape):
			cmds.setAttr(scope.shape+'.visibility', False)		

def active_shape_in_maya(scopes):
	for scope in scopes:
		if scope.shape!='' and cmds.objExists(scope.shape):
			cmds.setAttr(scope.shape+'.visibility', True)	

def scale4render(scopes):
	for scope in scopes:
		if scope.shape!='' and cmds.objExists(scope.shape):
			cmds.setAttr(scope.shape+'.scaleZ', 1)		

def clear_inactive_in_maya(scopes):
	for scope in scopes:
		if cmds.objExists(scope.shape) :
			if cmds.getAttr(scope.shape+'.visibility') is False:
			cmds.delete(scope.shape)
		
def is2D(scope,axis):
	faceCount=cmds.polyEvaluate( [scope.shape], f=True )
	for i in xrange(faceCount):
		vtxs=getvtx_local(scope.shape+'.f['+str(i)+']')
		b=get_bound(vtxs)
		if b[5]-b[4]>0.0 and b[3]-b[2]>0.0 and b[1]-b[0]>0.0:
			return False
		if axis=='XZ':
			if b[3]-b[2]>0.0:
				return False
		elif axis=='XY':
			if b[5]-b[4]>0.0:
				return False
	return True
		
def is2Dvtxs(vtxs,axis):
	b=get_bound(vtxs)
	if b[5]-b[4]>0.0 and b[3]-b[2]>0.0 and b[1]-b[0]>0.0:
		return False
	if axis=='XZ':
		if b[3]-b[2]>0.0:
			return False
	elif axis=='XY':
		if b[5]-b[4]>0.0:
			return False
	return True


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





gcurrentScope=CScope()
gparentScope=CScope()

def facade(rule):
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
	return myshape
	



facade('/Users/cobranail/Documents/nailtoolkit/CityEngineLite/test4.txt')
