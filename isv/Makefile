imgread:
imgread : imgread.cpp
	c++ -L/opt/ImageMagick-6.4.6/lib -I/opt/ImageMagick-6.4.6/include/ImageMagick -lMagick++ -o imgread imgread.cpp 
isv:
isv : isv.cxx imglist.cxx
	c++ -L/opt/regexpp3/libs -I/opt/regexpp3 -lboost_regex -L/opt/ImageMagick-6.4.6/lib -I/opt/ImageMagick-6.4.6/include/ImageMagick -lMagick++ `/opt/fltk/bin/fltk-config --cxxflags --ldflags` -o isv isv.cxx imglist.cxx
	/Developer/Tools/Rez -t APPL -o isv /opt/fltk/include/FL/mac.r
	/usr/bin/sips -i fb.png
	/Developer/Tools/DeRez -only icns fb.png > tempicns.rsrc
	/Developer/Tools/Rez -append tempicns.rsrc -o isv
	/Developer/Tools/SetFile -a C isv
timer:
timer : timer.cxx
	c++ `/opt/fltk/bin/fltk-config --cxxflags --ldflags` -o timer timer.cxx	
regx:
regx : regx.cpp
	c++ -L/opt/regexpp3/libs -I/opt/regexpp3 -lboost_regex -o regx regx.cpp
imseq:
imseq : imseq.cpp
	c++ -L/opt/regexpp3/libs -I/opt/regexpp3 -lboost_regex -o imseq imseq.cpp	


