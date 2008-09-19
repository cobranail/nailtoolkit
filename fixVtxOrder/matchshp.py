#shapematcher python version
#cobranail 2008/09/15

import maya.cmds
def topomatch(f1,v1,f2,v2):
	
	ls=maya.cmds.ls
	polyInfo=maya.cmds.polyInfo
	xform=maya.cmds.xform
	
	meshsel=ls(sl=True)
	
	

	faceList0=[]
	faceList1=[]
	faceList2=[]
	faceList3=[]
	

	facelist_s=polyInfo(meshsel[0],fv=True)
	facelist_d=polyInfo(meshsel[1],fv=True)	
	
	
	for f in facelist_s:
		g=f.split()
		g.pop(0)
		g[0]=g[0][:-1]
		h=[]
		k=[]
		k.append(int(g[0]))
		g.pop(0)
		for i in g:
			h.append(int(i))
			
		k.append(len(h))
		k.append(h)
		faceList0.append(k)
	  
	for f in facelist_d:
		g=f.split()
		g.pop(0)
		g[0]=g[0][:-1]
		h=[]
		k=[]
		k.append(int(g[0]))
		g.pop(0)
		for i in g:
			h.append(int(i))
			
		k.append(len(h))
		k.append(h)
		faceList1.append(k)
	  
	
	
	for f in faceList0:
		if f[0]==f1:
			faceList2.append(f)
			
	for f in faceList1:
		if f[0]==f2:
			faceList3.append(f)
			
			
	iv1=faceList2[0][2].index(v1)
	iv2=faceList3[0][2].index(v2)
	
	faceList2[0][2]=faceList2[0][2][iv1:]+faceList2[0][2][:iv1]
	faceList3[0][2]=faceList3[0][2][iv2:]+faceList3[0][2][:iv2]
	
	i=0
	
	matchface=False
	tlist=zip(faceList2,faceList3)
	
	for fa,fb in tlist:
		#print tlist
		
		for v0,v1,v2,v3 in zip(fa[2],fa[2][1:]+fa[2][:1],fb[2],fb[2][1:]+fb[2][:1]):
			for fa1 in faceList0:
				if v0 in fa1[2] and v1 in fa1[2]:
					#print fa1
					matchface=False
					for fb1 in faceList1:
						if v2 in fb1[2] and v3 in fb1[2]:
							if matchface :
								print 'topologic error.\n'
							else:
								matchface=True
								i+=1
								iv1=fa1[2].index(v0)
								iv2=fb1[2].index(v2)
								  
								fa1[2]=fa1[2][iv1:]+fa1[2][:iv1]
								fb1[2]=fb1[2][iv2:]+fb1[2][:iv2]
								faceList2.append(fa1)
								faceList3.append(fb1)
								faceList0.remove(fa1)
								faceList1.remove(fb1)   
								tlist.append((fa1,fb1))
		      #print 'Match face:',fa1,fb1
		      

	vtxlist0=[]
	vtxlist1=[]
	
	for f1,f2 in zip(faceList2,faceList3):
		for v1,v2 in zip(f1[2],f2[2]):
			if v1 not in vtxlist0 and v2 not in vtxlist1:
				vtxlist0.append(v1)
				vtxlist1.append(v2)
				
				
				
	#print zip(vtxlist0,vtxlist1)
	
	
	for v1,v2 in zip(vtxlist0,vtxlist1):
		t1=xform( meshsel[1]+'.vtx['+str(v2)+']',q=True, a=True, os=True, t=True )
		xform( meshsel[0]+'.vtx['+str(v1)+']', a=True, os=True, t=t1 )
