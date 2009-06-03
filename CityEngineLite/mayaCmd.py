import maya.cmds as cmds


def eval_T_in_maya(scope):
	#print 'call eval T in maya'
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
	
	ret=[cmds.getAttr(loc[0]+'.translate')[0],cmds.getAttr(loc[0]+'.rotate')[0]]
	cmds.delete(loc)
	return ret


def assign_shape_in_maya(scope):	
	if scope.shape=='':
		if scope.symbol!='':
			newpoly=cmds.polyCreateFacet(name=scope.symbol, p=[(0.0, 0.0, 0.0), (1, 0.0, 0.0), (1,1,0.0),(0.0, 1, 0.0)] )
			cmds.setAttr(newpoly[0]+'.translate',scope.position[0],scope.position[1],scope.position[2])
			cmds.setAttr(newpoly[0]+'.rotate',scope.orient[0],scope.orient[1],scope.orient[2])
			cmds.setAttr(newpoly[0]+'.scale',scope.size[0],scope.size[1],scope.size[2])

	else:
		newpoly=cmds.duplicate([scope.shape])
		#newpoly=cmds.polyCreateFacet( p=[(0.0, 0.0, 0.0), (1, 0.0, 0.0), (1,1,0.0),(0.0, 1, 0.0)] )
		cmds.setAttr(newpoly[0]+'.translate',scope.position[0],scope.position[1],scope.position[2])
		cmds.setAttr(newpoly[0]+'.rotate',scope.orient[0],scope.orient[1],scope.orient[2])
		cmds.setAttr(newpoly[0]+'.scale',scope.size[0],scope.size[1],scope.size[2])



gcurrentScope=CScope()
gparentScope=CScope()

def facade(rule):
	global gcurrentScope
	global gparentScope

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




