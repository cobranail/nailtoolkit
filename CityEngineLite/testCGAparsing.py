from CGAparser import *
import types
f = open(sys.argv[1],'r')
text=f.readlines()
ws=''
cmd=[]
def nt(ws,cmd):
	print ws,
	if type(cmd) is types.ListType:
		for x in cmd:
			if type(x) is types.ListType:
				print '\n'
				nt(ws+'    ',x)
			else:
				print x,
		#print '\n'
	else:
		print cmd

for str in text:
	cmd=parsingNotation(str)
	if len(cmd)>0:
		print cmd,'\n'
		nt(ws,cmd)
		print '\n'
