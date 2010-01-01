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
	return [[m,-l,0,m*vtx[0][0]-l*vtx[0][1]],[n,0,-l,n*vtx[0][0]-l*vtx[0][2]]]
	
def insector(vp,vl):
	r1=planeParam(vp)
	r2=lineParam(vl)
	a=[r1[:3]]
	b=[[-r1[-1]]]
	for m in r2:
		a.append(m[:3])
		b.append([m[-1]])
	if det(a)!=0:
		p = matrix_mutil(invMat(a),b)
		return p[0]+p[1]+p[2]
	return False

def inGraph(p,vp,vl):
	if min(vl[0][0],vl[1][0])<=p[0]<=max(vl[0][0],vl[1][0]) and pointInTri3D(p,vp):
		return True
	return False
