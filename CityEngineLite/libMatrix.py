def det(x):
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
	sum=0
	for i,c in enumerate(a):
		for d in a[:i]:
			if d>c:
				sum+=1
	return sum

	
def emu(a):
	if len(a)>1:
		el=[]
		for i,c in enumerate(a):
			b=a[:]
			b.pop(i)
			et=emu(b)
			for e in et:
				el.append([c]+e)
		return el
	elif len(a)==1:
		return [a]		


def aac(a,i,j):
	b=a[:]
	b.pop(i)
	m=[]
	for c in b:
		d=c[:]
		d.pop(j)
		m.append(d)
	return (-1)**(i+j)*det(m)
	
def matrix_mutil(a,b):
	return [[sum(i*j for i, j in zip(row, col)) for col in zip(*b)] for row in a]


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
		print 'x',x

def isAllZeroes(a):
	for c in a:
		if c!=0:
			return False
	return True

def linearEqSolver(m):
	a=[x[:-1] for x in m]
	b=[[x[-1]] for x in m]
	zero_column=[]
	zero_row=[]
	
	d=len(a)
	
	for i,c in enumerate(a):
		if isAllZeroes(c):
			zero_row.append(i)
	for i,c in enumerate(a[0]):
		if isAllZeroes([f[i] for f in a]):
			zero_column.append(i)
	zero_column.reverse()
	zero_row.reverse()
	
	for i in zero_row:
		a.pop(i)
		b.pop(i)
	for r in a:
		for j in zero_column:
			r.pop(j)
	
	if det(a)!=0:
		p = matrix_mutil(invMat(a),b)
		zero_column.reverse()
		for c in zero_column:
			p.insert(c,[0])
		return p
			
	return False

