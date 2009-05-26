import sys

def parsingCmd(buf,tag,cmdList):
	cmdList.append([tag,buf])
	return cmdList

def parsingEnc(c,stack):
	
	if c == '(':
		stack.append(')')
	elif c == '[':
		stack.append(']')
	elif c == '{':
		stack.append('}')
	elif c in [')',']','}']:
		if len(stack)>0:
			if c == stack.pop():
				pass
			else:
				return c
		else:
			return c
	return stack	
                    
 
def parsingSuccessor(successor):
	KeyWords=['Subdiv','Repeat','Comp','Roof','Snap','SnapLines','T','R','S','I']
	cmdList=[]
	expect=''
	token=''
	buffer=''
	tokenType=''
	scope='symbol'
	paramEncStack=[]
	symEncStack=[]
	cmdEndStack=[]
	cmdStack=[]
	lastCmd=''
	quote=''
	pc=''
	for c in successor:
		expect =''
		if quote!='':
			if pc !='\\' and c==quote:
				quote=''		
#			print 'c,pc:',c,pc
#			if c in ['"','\'']:			
#				if pc=='\\' and c==quote:
#					buffer+=c
#				else:
#					if quote==c:
#							quote=''
#					elif quote == '':
#						quote=c
			buffer+=c
		else:
			if c == '(':
				if scope=='symbol':
					#in symbol scope, '(' means nothing, only a bracket sign
					if buffer in KeyWords:
						# while '(' following a keyword, it means entering param parsing mode, param mode starts at next char 
						token=buffer
						tokenType='cmd'
						cmdList=parsingCmd(buffer,'CMDSTART',cmdList)
						cmdStack.append(buffer)
						buffer = ''
						scope='param'
					else:
						symEncStack=parsingEnc(c,symEncStack)
						
				elif scope == 'param':
					paramEncStack=parsingEnc(c,paramEncStack)
					buffer+=c
				
			elif c == ')':
				if scope == 'symbol':
					r=parsingEnc(c,symEncStack)
					if r ==')':
						print  'error: mismatch ) in symbol scope.'
						break
					else:
						symEncStack=r
				elif scope == 'param':
					r=parsingEnc(c,paramEncStack)
					if r == ')':
						#leave param mode
						token=buffer
						tokenType='param'
						cmdList=parsingCmd(buffer,'PARAM',cmdList)
						lastCmd=cmdStack.pop()
						cmdList=parsingCmd(lastCmd,'CMDEND',cmdList)
						buffer=''
						scope='symbol'
					else:
						paramEncStack=r
						buffer+=c
			elif c == '[':
				if scope=='symbol':
					cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
					cmdStack.append(c)
					token=buffer
					tokenType='symbol'
					buffer=''
					cmdList=parsingCmd(c,'CMDSTART',cmdList)
					cmdList=parsingCmd(c,'CMDEND',cmdList)
				elif scope == 'param':
					paramEncStack=parsingEnc(c,paramEncStack)
					buffer+=c
			
			elif c==']':
				if scope == 'symbol':
					token=buffer
					tokenType='symbol'
					cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
					buffer=''
					cmdList=parsingCmd(c,'CMDSTART',cmdList)
					cmdList=parsingCmd(c,'CMDEND',cmdList)
					
				elif scope == 'param':
					r=parsingEnc(c,paramEncStack)
					if r == ']':
						print 'error: mismatch ] in param scope.'
						break
					else:
						paramEncStack=r
						buffer+=c
			
			elif c=='{':
				if scope == 'symbol':
					if tokenType == 'param' :
						cmdEndStack.append(cmdList.pop())
						symEncStack=parsingEnc(c,symEncStack)
					else:
						print 'syntax error: { is neither a cmd nor a symbol'
						break
				elif scope == 'param':
					paramEncStack=parsingEnc(c,paramEncStack)
					buffer+=c
			
			elif c == '}':
				if scope == 'symbol':
					r=parsingEnc(c,symEncStack)
					if r=='}':
						print 'error: mismatch } in symbol scope.'
						break
					else:
						symEncStack = r
						token=buffer
						tokenType='symbol'
						cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
						buffer=''
						cmdList.append(cmdEndStack.pop())
				elif scope== 'param':
					r=parsingEnc(c,paramEncStack)
					if r=='}':
						print 'error: mismatch } in param scope.'
						break
					else:
						paramEncStack=r
						buffer+=c
						
			elif c == '|':
				if buffer != '':
					token=buffer
					tokenType='symbol'
					cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
					buffer=''
			
			elif c in [' ','\t']:
				if scope == 'symbol':
					if buffer !='':
						token=buffer
						tokenType='symbol'
						cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
						buffer=''
				elif scope == 'param':
						buffer+=c
					
			elif c in ['"','\'']:
				if scope == 'param':
					if quote == '':
						quote=c
						buffer+=c
			else:
				buffer+=c
			
		pc = c
	#if buffer!='':
	cmdList=parsingCmd(buffer,'SYMBOL',cmdList)
	i=0
	while i<len(cmdList):
		if cmdList[i][1]=='':
			cmdList.pop(i)
		else:
			i+=1
	
	return cmdList

def tokenStream(stream,key):
	quote=''
	token=''
	buffer=''
	pc=''
	encStack=[]
	tokenList=[]
	
	if key in ['"','\'','(',')','\\', '[',']','{','}']:
		return 'error'
	
	for c in stream:
		if quote == '':
			if c == key :				
				if encStack == []:
					token=buffer
					tokenList.append(token)
					buffer=''
			elif c in ['"','\'']:
				quote = c
				buffer+=c
			elif c in '()[]{}':
				r=parsingEnc(c,encStack)
				if type(r) is type(''):
					print 'error: enclose mismatch',c
					break
				else:
					encStack=r
					buffer+=c
			else:
				buffer+=c
		else:
			if pc !='\\' and c==quote:
				quote=''
			buffer+=c
		
		pc = c 
	tokenList.append(buffer)
	
	return tokenList

def parsingNotation(line):
	notation=[]
	nota=[]
	cmd=[]
	s=[]
	
	stream=line.strip()
	if len(stream)>0:
		if stream[0]!='#':
			notation=tokenStream(stream,'~')
			if type(notation) is type([]):
				nota=tokenStream(notation.pop(0),':')
				
				if len(nota)==2:
					nota.append('True')
				if len(nota)==3:
					for successor in notation:
						s=tokenStream(successor,':')
						cmd.append(['SUCCESSOR','---'])
						cmd+=parsingSuccessor(s.pop(0))						
						if s == []:
							cmd.append(['PROB','1'])
						else:
							cmd.append(['PROB',s.pop(0)])
					nota.append(cmd)
					cmd=[]
	
	#print nota				
	return nota





