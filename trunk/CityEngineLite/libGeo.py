def planeParam(vtx):
	a=((vtx[1][1]-vtx[0][1])*(vtx[2][2]-vtx[0][2])-(vtx[1][2]-vtx[0][2])*(vtx[2][1]-vtx[0][1]))
	b=((vtx[1][2]-vtx[0][2])*(vtx[2][0]-vtx[0][0])-(vtx[1][0]-vtx[0][0])*(vtx[2][2]-vtx[0][2]))
	c=((vtx[1][0]-vtx[0][0])*(vtx[2][1]-vtx[0][1])-(vtx[1][1]-vtx[0][1])*(vtx[2][0]-vtx[0][0]))
	d=(0-(a*vtx[0][0]+b*vtx[0][1]+c*vtx[0][2]))
	return [a,b,c,d]

def lineParam(vtx):
	l=vtx[1][0]-vtx[0][0] #x
	m=vtx[1][1]-vtx[0][1] #y
	n=vtx[1][2]-vtx[0][2] #z
	
	if fabs(l)<0.000000001:
		l=0
	if fabs(m)<0.000000001:
		m=0
	if fabs(n)<0.000000001:
		n=0
	
	if (not l==m==0) and (not n==l==0):
		return [[m,-l,0,m*vtx[0][0]-l*vtx[0][1]],[n,0,-l,n*vtx[0][0]-l*vtx[0][2]]]
	elif (not l==m==0) and (not n==m==0):
		return [[m,-l,0,m*vtx[0][0]-l*vtx[0][1]],[0,n,-m,n*vtx[0][1]-m*vtx[0][2]]]
	elif (not l==n==0) and (not n==m==0):
		return [[n,0,-l,n*vtx[0][0]-l*vtx[0][2]],[0,n,-m,n*vtx[0][1]-m*vtx[0][2]]]
	
def intersector(vp,vl):
	r1=planeParam(vp)
	r2=lineParam(vl)
	#print 'vl',vl
	#print 'r2',r2
	a=[r1[:3]]
	b=[[-r1[-1]]]
	for m in r2:
		a.append(m[:3])
		b.append([m[-1]])
	if det(a)!=0:
		p = matrix_mutil(invMat(a),b)
		return p[0]+p[1]+p[2]
	else:
		#print a,b
		#print 'det is 0'
		return False


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

def pointOnTri(p,vtx):
	d=[ x+[1.0] for x in vtx ]
	if fabs(0.5*det(d)) < 0.000000000000001:
		#print 'area is 0'
		if (min(vtx[0][0],vtx[1][0],vtx[2][0])<=p[0]<=max(vtx[0][0],vtx[1][0],vtx[2][0])) or (min(vtx[0][1],vtx[1][1],vtx[2][1])<=p[1]<=max(vtx[0][1],vtx[1][1],vtx[2][1])):
			#print '2d true'
			return True
		#print '2d false'
		
	else:
		if cw([vtx[0],vtx[1],p])>=0 and cw([vtx[1],vtx[2],p])>=0 and cw([vtx[2],vtx[0],p])>=0:
			return True
		elif cw([vtx[0],vtx[1],p])<=0 and cw([vtx[1],vtx[2],p])<=0 and cw([vtx[2],vtx[0],p])<=0:
			return True
		#print '3d false'
	return False


def pointInTri3D(p3D,vtx3D):
	#p3D is point in 3d space
	#vtx3D is a vertex list of a tri in 3D space
	pxy=p3D[:2]
	pyz=p3D[1:]
	pxz=p3D[::2]
	vxy=[a[:2] for a in vtx3D ]
	vyz=[a[1:] for a in vtx3D ]
	vxz=[a[::2] for a in vtx3D]
	if pointInTri(pxy,vxy) and pointInTri(pyz,vyz) and pointInTri(pxz,vxz):
		return True
	return False

def pointOnTri3D(p3D,vtx3D):
	#p3D is point in 3d space
	#vtx3D is a vertex list of a tri in 3D space
	pxy=p3D[:2]
	pyz=p3D[1:]
	pxz=p3D[::2]
	vxy=[a[:2] for a in vtx3D ]
	vyz=[a[1:] for a in vtx3D ]
	vxz=[a[::2] for a in vtx3D]
	
	if pointOnTri(pxy,vxy) and pointOnTri(pyz,vyz) and pointOnTri(pxz,vxz):
		return True
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

def pointInPoly3D(p3D,vtx3D):
	vtx2=copy.deepcopy(vtx3D)
	v0=[vtx2.pop(0)]
	dp=zip(vtx2[:-1],vtx2[1:])
	for dv in dp:
		if pointInTri3D(p,v0+list(dv)):
		#if point is in one of the sub-tri,then it is in the poly
			return True
	return False


def inGraph(p,vp,vl):
	if min(vl[0][0],vl[1][0])<=p[0]<=max(vl[0][0],vl[1][0]) and pointInTri3D(p,vp):
		return True
	return False

def onGraph(p,vp,vl):
	if min(vl[0][0],vl[1][0])<=p[0]<=max(vl[0][0],vl[1][0]) and pointOnTri3D(p,vp):
		return True
	return False
	
def polyEdgeIntersection(pvtx,evtx):
	vtx0=copy.deepcopy(pvtx)
	intersections=[]	
	count=len(vtx0)
	i=0
	while i<count and intersections==[]:
		vtx2=vtx0[i:]+vtx0[:i]
		v0=[vtx2.pop(0)]
		dp=zip(vtx2[:-1],vtx2[1:])
		
		for dv in dp:
			ip = intersector(v0+list(dv),evtx)
			if ip :
				if min(evtx[0][0],evtx[1][0])<=ip[0]<=max(evtx[0][0],evtx[1][0]) and pointOnTri3D(ip,v0+list(dv)):
					intersections.append(ip)
			#if point is in one of the sub-tri,then it is in the poly
		i+=1	
	return intersections