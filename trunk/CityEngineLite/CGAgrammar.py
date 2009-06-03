import sys

import types
import random
import math
import copy
import fpformat
#from CGAparser import *

class CScope:
	position=[0,0,0]
	orient=[0,0,0]
	size=[1,1,1]
	symbol=''
	D=0
	bound=[]
	shape=''
	locator=''
	parent=None
	T=[]
	# T : ['T','O',['A','A','R'],[x,y,z]],['R','O',['R','R','R'],[u,v,w]]
	def __init__(self,object=None):
		
		if isinstance(object,CScope):
			self.position=copy.copy(object.position)
			self.orient=copy.copy(object.orient)
			self.size=copy.copy(object.size)
			self.symbol=object.symbol
			self.shape=object.shape
			self.T=copy.deepcopy(object.T)
			self.D=object.D
			
	
	def show(self):
		print self.position,self.orient,self.size,self.symbol,self.shape,self.T
		
	def setParent(self,object=None):
		if isinstance(object,CScope):
			self.parent=CScope(object)
			
	def pushT(self,T):
		self.T.append(copy.deepcopy(T))
	
	def popT(self):
		return self.T.pop(0)
		
	def sync(self):
		scopeSpace=eval_T_in_maya(self)
		self.position=list(scopeSpace[0])
		self.orient=list(scopeSpace[1])
		self.T=[]
		pass
'''		
	def shape2scope(self):
		self.position=getForm('T',shape)
		self.orient=getForm('R',shape)
		self.size=getForm('S',shape)
	def scope2shape(self):
		setForm('T',shape,self.position)
		setForm('R',shape,self.orient)
		setForm('S',shape,self.size)
'''

class CStructure:
	notations=[]
	symbols=[]
	predecessor=CScope()
	#currentScope=gcurrentScope
	scopeStack=[]
	cmdList=[];
	subSymbols=[]
	usingMayaSpace=False
	'''
	def __init__(self):
		self.notations=[]
		self.symbols=[]
		self.predecessor=CScope()
		self.scopeStack=[]
		self.cmdList=[];
		self.subSymbols=[]
		self.usingMayaSpace=False
	'''
	def evaluate(self):
		for notation in self.notations:
			
			if len(notation)>0 :
				print notation
				self.parsing(notation)
		for scope in self.symbols:
			print 'Term:',scope.size,scope.symbol

	def assignShape(self):
		for scope in self.symbols:
			assign_shape_in_maya(scope)
	
	def operate(self,cmdList,p):
		global gcurrentScope
		#print 'operate start at',p,cmdList[p]
		param=[]
		symbol=[]
		scopeList=[]
		Func=['Subdiv','Repeat','Comp','Roof','Snap','SnapLines','[',']','T','R','S','I','Extrude']
		SymbolFunc=['Subdiv','Repeat','Comp','Roof']
		SuccessorSymbol=['SUCCESSOR','PROB']
		TransformFunc=['Translate','Rotate','Scale']
		StackFunc=['Push','Pop']
		SnapFunc=['Snap','SnapLines']
		ObjectFunc=['Insert']
		repeatCount=1
		cmdStack=[]
		preCmd=[]
		
		
		for CGAcmd in cmdList:
			#print 'cmd is ',cmd
			if (CGAcmd[0] in SuccessorSymbol):
				p+=1;
			elif (CGAcmd[0] == 'CMDSTART') and (CGAcmd[1] in Func):
				func=CGAcmd[1]
				scopeList=[]
				cmdStack.append(CGAcmd)
				#print 'start with scope ',gcurrentScope.show()
				#next instruction
				p+=1
				
			elif (CGAcmd[0] == 'PARAM') and (cmdStack[-1][0] == 'CMDSTART'):
				if (CGAcmd[0] is 'PARAM'):
					#get the parameters
					#print cmdList[p][1]
					param=tokenStream(CGAcmd[1],',')
					p+=1
				func = cmdStack[-1][1]
				#print func,param
				if func in ['T','R']:
					gcurrentScope.pushT(copy.deepcopy(parsingTRParam(func,param)))
				elif func == 'S':
					parsingSParam(param)
				elif func == 'I':
					#gcurrentScope.shape=param[0]
					tscope=CScope(gcurrentScope)
					tscope.shape=param[0]
					tscope.sync()
					self.subSymbols.append(tscope)
					#scopeList.append(tscope)
				elif func == '[':
					tmpscope=CScope(gcurrentScope)
					self.scopeStack.append(tmpscope)
				elif func == ']':
					tmpscope=self.scopeStack.pop()
					gcurrentScope=CScope(tmpscope)
				elif func == 'Subdiv':
					scopeList=parsingSubdivParam(param)
					for c in scopeList:
						c.show()
				elif func == 'Repeat':
					scopeList=parsingRepeatParam(param)
					repeatCount=len(scopeList)
				elif func == 'Comp':
					pass
				elif func == 'Roof':
					pass
				elif func == 'Snap':
					pass
				elif func == 'SnapLines':
					pass
				'''
				print '---symbols scopeList---'
				
				for sc in self.subSymbols:
					sc.show()
				print '---endprint----'
				'''
				
				#get symbols and nested func 

			#assign a symobl in a cmd scope
			elif CGAcmd[0] == 'SYMBOL':  			


				#print 'currentScope is ', gcurrentScope.show()
				while repeatCount>0:
					if len(scopeList)>0:
						scope=scopeList[0]
						gcurrentScope=CScope(scope)
						gcurrentScope.sync()
						scopeList.pop(0)
					
					s=CGAcmd[1]
					if type(s) is types.StringType:			
						if CGAcmd[1] == 'Empty' :
							pass
							#print 'Symbol : remove'
						else :
							scope=CScope(gcurrentScope)
							scope.symbol=CGAcmd[1]
							scope.sync()
							self.subSymbols.append(scope)
							#print 'Symbol :',CGAcmd[1]
					elif type(s) is types.ListType:
						tp=self.operate(s,0)
					
					repeatCount-=1
				repeatCount=1
	
				p+=1
			elif CGAcmd[0] == 'CMDEND':
				pass
			else:
				print 'Undefined Notation ',CGAcmd
				return len(cmdList)
			#print 'return at',p,cmdList[p]
		return p
	
	
	def parsing(self,notation):
		#print 'subsymbols start:',self.subSymbols
		global gcurrentScope
		
		cmdList=notation[3]
		cmdListLen=len(cmdList)
		p=0
		successors=[]
		while (p<cmdListLen):
	
			if (cmdList[p][0] is 'SUCCESSOR') :
				s=p
			elif (cmdList[p][0] is 'PROB') :
				e=p
				successors.append([s,e,eval(cmdList[p][1])])
			p+=1
			
		self.predecessor.symbol=notation[1]
		i=0
		defaultSymbol=CScope()
		defaultSymbol.symbol='default'
		slen=len(self.symbols)
		if slen==0:
			self.symbols.append(defaultSymbol)
			slen=len(self.symbols)
		while i<slen:
			#print 'predecessor:',self.predecessor
			if self.predecessor.symbol == self.symbols[i].symbol:
				gcurrentScope = CScope(self.symbols[i])
				self.predecessor = CScope(self.symbols[i])
				gparentScope = CScope(self.symbols[i])
				#print 'SUCCESSOR start:'
				r=random.random()
				#print 'random ',r
				cond=eval(notation[2])
				#print 'notation',notation[0],'condition is',cond
				if cond:
					for successor in successors:
						if r>0:
							if r-successor[2]>0:
								r-=successor[2]
				
							else:
								successorIN=cmdList[successor[0]:successor[1]]
								#print 'successor in',successorIN
								self.operate(successorIN,0)
								#ptr=successor[0]
								#print 'choice:',successor
								#print '---------start----------'
								#while ptr<successor[1]:
								#	ptr=self.operate(cmdList,ptr)
									#ptr+=1
								r-=successor[2]
				
					idx=i
					self.symbols.pop(idx)
					self.symbols=self.symbols[:idx]+self.subSymbols+self.symbols[idx:]
					#print self.predecessor.symbol,'have been replaced.'
		
			slen=len(self.symbols)
			sl=len(self.subSymbols)
			if sl==0:
				i+=1
			else:
				i+=sl
			self.subSymbols=[]

def parsingTRParam(t,param):
	
	m=len(param)
	axisid=0
	
	T=[t,'O',['R','R','R'],[0,0,0]]
	if t=='S':
		T[3]=[1,1,1]
	
	if m == 2:
		if 'X' == param[0]:
			axisid=0
		elif 'Y' == param[0]:
			axisid=1
		elif 'Z' == param[0]:
			axisid=2
		
		if type(param[1])==types.ListType:			
			# param=['X',[a,10]]
			if param[0]=='r':
				T[2][axisid]='R'
				
			elif param[0]=='a':
				T[2][axisid]='A'
				
			else:
				T[2][axisid]='R'
			T[3][axisid]=eval(param[1][1])				
		else:				
			T[3][axisid]=eval(param[1])
			T[2][axisid]='R'
			
	elif m==3:
		for i in range(0,3):
			if type(param[i])==types.ListType:
				if param[0]=='r':
					T[2][i]='R'
					
				elif param[0]=='a':
					T[2][i]='A'
					
				else:
					T[2][i]='R'
				T[3][i]=eval(param[1][i])				
					
			else:	
				T[3][i]=eval(param[i])
				T[2][i]='R'
	return T
	
def parsingSParam(param):
	t='S'
	m=len(param)
	axisid=0
	
	if m == 2:
		if 'X' == param[0]:
			axisid=0
		elif 'Y' == param[0]:
			axisid=1
		elif 'Z' == param[0]:
			axisid=2
		val=eval(param[1])
		#print 'val',val,type(val)
		if type(val)==types.ListType:
			if t=='T':
				gcurrentScope.position[axisid]+=val[1]
			elif t=='R':
				gcurrentScope.orient[axisid]+=val[1]	
			elif t=='S':
				gcurrentScope.size[axisid]*=val[1]	
				
		else:	
			if t=='T':
				gcurrentScope.position[axisid]=val
			elif t=='R':
				gcurrentScope.orient[axisid]=val
			elif t=='S':
				gcurrentScope.size[axisid]=val
			
	elif m==3:
		for i in range(0,3):
			val=eval(param[i])
			#print 'val',val,type(val)
			if type(val)==types.ListType:
				if t=='T':
					gcurrentScope.position[i]+=val[1]
				elif t=='R':
					gcurrentScope.orient[i]+=val[1]
				elif t=='S':
					gcurrentScope.size[i]*=val[1]
				
			else:	
				if t=='T':
					gcurrentScope.position[i]=val
				elif t=='R':
					gcurrentScope.orient[i]=val
				elif t=='S':
					gcurrentScope.size[i]=val


def parsingSubdivParam(param):
	global gcurrentScope
	scopeList=[]
	axisid=-1
	axis=''
	scope_sx=0.0
	param_val=[]
	rsum=0.0
	vsum=0.0
	have_r=False
	snap=False
	T1=['T','O',['R','R','R'],[0,0,0]]
	#T2=['S','O',['A','A','A'],[1,1,1]]
	
	if len(param)>0:
		axis=list(param.pop(0))
	
	while len(param)>0:
		ret=param.pop(0)
		#print 'ret:',ret
		param_val.append(eval(ret))
	if 'S' in axis:
		snap=True	
	if 'X' in axis:
		axisid=0
	elif 'Y' in axis:
		axisid=1
	elif 'Z' in axis:
		axisid=2		
	scope_sx=gcurrentScope.size[axisid]
	
	for val in param_val:
		#print 'val is',type(val),val
		if type(val) is types.ListType:
			#print 'r',type(val[1])
			rsum+=float(val[1])
			have_r=True
		else:
			#print 'v',type(val),val
			vsum+=float(val)
	
	if have_r:
		rv=(scope_sx-vsum)/rsum
	s=0
	#print gcurrentScope.show()
	#print 'subdiv start scope',gcurrentScope.position,gcurrentScope.size
	for val in param_val:
		T1[3]=[0,0,0]
		#T2[3]=copy.copy(Ts)		
		tmpscope=CScope(gcurrentScope)
		if type(val) is types.ListType:
			tmpscope.size[axisid]=float(val[1])*rv
		else:
			tmpscope.size[axisid]=float(val)
		T1[3][axisid]=s
		tmpscope.pushT(T1)
		s+=tmpscope.size[axisid]
		#tmpscope.show()

		#convert transform to maya space
		scopeList.append(tmpscope)
	#print 'subdiv pre item s',s
	T1[3][axisid]=scope_sx
	gcurrentScope.pushT(T1)
	return scopeList

def parsingRepeatParam(param):
	global gcurrentScope
	#print 'param',param
	scopeList=[]
	axisid=-1
	axis=''
	scope_sx=0.0
	param_val=[]
	rsum=0.0
	vsum=0.0
	useCount=False
	repeatCount=1
	T1=['T','O',['R','R','R'],[0,0,0]]
	if len(param)>0:
		axis=param.pop(0)
	
	while len(param)>0:
		ret=param.pop(0)
		#print 'ret:',ret
		param_val.append(eval(ret))
	
	if 'X' in axis:
		#scope_sx=gcurrentScope.size[0]
		axisid=0
	elif 'Y' in axis:
		#scope_sx=gcurrentScope.size[1]
		axisid=1
	elif 'Z' in axis:
		#scope_sx=gcurrentScope.size[2]
		axisid=2
	
	if 'D' in axis:
		useCount=True		
	
	scope_sx=gcurrentScope.size[axisid]
	
	for val in param_val:
		vsum+=float(val)
	
	if useCount:
		repeatCount=int(param_val[0])
		#print 'repeatCount',repeatCount
		s=0.0
		for i in range(0,repeatCount):
			T1[3]=[0,0,0]
			tmpscope=CScope(gcurrentScope)
			T1[3][axisid]=s
			#tmpscope.T=[]
			tmpscope.pushT(T1)
			#print s,tmpscope.T,tmpscope.size
			tmpscope.size[axisid]=float(scope_sx)/repeatCount
			#print 'scope_sx/repeatCount',float(scope_sx)/repeatCount
			s+=tmpscope.size[axisid]
			#tmpscope.show()
			scopeList.append(tmpscope)		
		
		
	else:
		repeatCount=int(math.floor(scope_sx/vsum))
		
		s=0.0
		for i in range(0,repeatCount):
			T1[3]=[0,0,0]
			tmpscope=CScope(gcurrentScope)
			T1[3][axisid]=s
			#tmpscope.T=[]
			tmpscope.pushT(T1)
			print tmpscope.T
			tmpscope.size[axisid]=scope_sxrepeatCount
			s+=tmpscope.size[axisid]
			#tmpscope.show()
			scopeList.append(tmpscope)
			
	T1[3][axisid]=scope_sx
	gcurrentScope.pushT(T1)
	print 'repeat sec', len(scopeList)
	for c in scopeList:
		c.show()
	return scopeList


def r(x):
	#print 'x is',type(x),x
	return ['r',eval(x.__str__())]
def a(x):
	return x

def LCTs(scope):
	ts=[0,0,0]
	T=scope.T
	ts=copy.copy(scope.size)
	if len(T)>0:	
		for t in T:
			if t[0] == 'S':
				for i in range(3):
					if t[2][i]=='R':
						ts[i]*=t[3][i]
					elif t[2][i]=='A':
						ts[i]=t[3][i]
	return ts
