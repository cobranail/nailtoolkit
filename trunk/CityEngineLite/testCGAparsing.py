from CGAparser import *

f = open(sys.argv[1],'r')
text=f.readlines()
for str in text:
	cmd=parsingNotation(str)
	print cmd
