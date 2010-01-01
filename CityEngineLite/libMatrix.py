def det(x):
	'''求行列式'''
	row=0
	column=0
	row=len(x)
	if row>0:
		column=len(x[0])
	for c in x:
		if len(c) != column:
			print 'column size error.'
			return False
	r=range(row)
	emua=emu(r)
	sum=0.0
	count=0
	for k in emua:
		product=1.0
		for i,j in zip(r,k):
			product*=x[i][j]
		sum+=((-1)**rsn(k)*product)
		count+=1
	return sum

def rsn(a):
	'''求逆序数'''
	sum=0
	for i,c in enumerate(a):
		for d in a[:i]:
			if d>c:
				sum+=1
	return sum

	
def emu(a):
	'''	求a的全排列 	'''
	if len(a)>1:
		el=[]
		for i,c in enumerate(a):
			b=a[:]
			b.pop(i)
			''' 固定一个值，对其它的进行全排列 '''
			et=emu(b)
			for e in et:
				el.append([c]+e)
				''' e 是 [[],[]]这种形式	'''
		return el
	elif len(a)==1:
		'''
		当len a>1 时 return 的是[[],[]]这种形式
		当len a=1 时，也需要用这种形式
		'''
		return [a]		


def aac(a,i,j):
	'''求代数余子式'''
	b=a[:]
	b.pop(i)
	m=[]
	for c in b:
		d=c[:]
		d.pop(j)
		m.append(d)
	return (-1)**(i+j)*det(m)

def invMat(x):
	m=[]
	row=0
	column=0
	row=len(x)
	if row>0:
		column=len(x[0])
	r=range(row)
	
	detx=det(x)
	
	if detx!=0.0:
		for j in r:
			mc=[]
			for i in r:
				mc.append(aac(x,i,j)/detx)
			m.append(mc[:])
		return m
	else:
		print 'det is 0.'





