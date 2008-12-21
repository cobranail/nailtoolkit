/***
 uvDraw utility 0.1
 License: BSD 3rd
	
 cobranail@gmail.com
  2008/12/21
 
***/


#include <boost/regex.hpp>
#include <iostream>
#include <fstream>
#include <cstdio>
#include <stdlib.h>
#include <string.h>
#include <cmath>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <Magick++.h> 

using namespace Magick; 
using namespace std;

typedef struct d2d
	{
		double x;
		double y;
	} D2D;

typedef struct d3d {
	double x;
	double y;
	double z;
} D3D;

typedef struct line {
	D2D sp;
	D2D ep;
} LINE;

typedef struct polyface{
	vector<int> vtxid;
	vector<int> uvid;
} polyFace;


int main (int argc, char * const argv[]) {
	// insert code here...
	if(argc==4) {
		
		ifstream objfile(argv[1]);
		if(!objfile) {
			
			cout<<endl<<"failed to open obj file "<<argv[1]<<endl;
			return 1;
			
		}
		
		vector<D3D> vtxs;
		vector<D2D> uvs;
		vector<polyFace> pfaces;
		
		
		
		string buffer;
		string vtxstr = "^v ([-]?[0-9]*.[0-9]*) ([-]?[0-9]*.[0-9]*) ([-]?[0-9]*.[0-9]*)$";
		string uvstr = "^vt ([-]?[0-9]*.[0-9]*) ([-]?[0-9]*.[0-9]*)$";
		string fstr = "^f (.*$)";
		string fvstr="([0-9]*)/([0-9]*)/[0-9]*";
		
		boost::regex vtx_expression(vtxstr);
		boost::regex uv_expression(uvstr);
		boost::regex f_expression(fstr);
		boost::regex fv_expression(fvstr);
		
		while(!objfile.eof()) {
			getline(objfile,buffer);
			
			
			
			string testString = buffer;
			boost::smatch what;
			string::const_iterator start = testString.begin();
			string::const_iterator end = testString.end();
			if(boost::regex_search(start, end, what, vtx_expression)){
				//prase vtx
				
				string v1(what[1].first, what[1].second);
				string v2(what[2].first, what[2].second);
				string v3(what[3].first, what[3].second);
				//cout<< "vertex : " << v1.c_str() <<" "<< v2.c_str()<<" "<<v3.c_str()<<endl;
				start = what[0].second;
				
				D3D vtx;
				vtx.x=atof(v1.c_str());
				vtx.y=atof(v2.c_str());
				vtx.z=atof(v3.c_str());
				
				vtxs.push_back(vtx);
				
			}
			if(boost::regex_search(start, end, what, uv_expression)){
				//prase uv
				string v1(what[1].first, what[1].second);
				string v2(what[2].first, what[2].second);
				
				//cout<< "uv : " << v1.c_str() <<" "<< v2.c_str()<<endl;
				start = what[0].second;
				
				D2D uv;
				uv.x=atof(v1.c_str());
				uv.y=atof(v2.c_str());
				
				uvs.push_back(uv);
				
				
			}
			if(boost::regex_search(start, end, what, f_expression)){
				
				//prase face
				polyFace pface;
				//cout<<"face: "<<endl;
				string data(what[1].first, what[1].second);
				
				boost::smatch what2;
				string::const_iterator start2 = data.begin();
				string::const_iterator end2 = data.end();
				while( boost::regex_search(start2, end2, what2, fv_expression) ){
					//prase face data
					string vtxi(what2[1].first, what2[1].second);
					string uvi(what2[2].first, what2[2].second);
					
					//cout<<"vtx id: "<<vtxi.c_str()<<", uv id: "<<uvi.c_str()<<endl;
					start2=what2[0].second;
					
					
					pface.vtxid.push_back(atoi(vtxi.c_str()));
					pface.uvid.push_back(atoi(uvi.c_str()));
					
				}
				start = what[0].second;
				pfaces.push_back(pface);
			}
			
		}
		
		objfile.close();
		/*
		cout<<"vector has "<<vtxs.size()<<" vtxs"<<endl;
		cout<<"vector has "<<uvs.size()<<" uvs"<<endl;
		cout<<"vector has "<<pfaces.size()<<" pfaces"<<endl;
		
		
		int i,j;
		for(i=0;i<pfaces.size();i++){
			cout<<"face:"<<i<<" uvid: ";
			for(j=0;j<pfaces[i].uvid.size();j++){
				cout<<" "<<pfaces[i].uvid[j];
			
			
			}
			cout<<endl;
		
		}
		*/
		
		char tag[8]; //header 8 chars
		int ver;     //version
		int imgsize; //outimage size
		int linewidth; //line width
		int ln; //line count
		
		int *lp; //line data block
		
		FILE *f;
		f=fopen(argv[2],"rb");
		fread(tag,sizeof(char),8,f);
		fread(&ver,sizeof(int),1,f);
		fread(&imgsize,sizeof(int),1,f);
		fread(&linewidth,sizeof(int),1,f);
		fread(&ln,sizeof(int),1,f);
		
		lp=new int [ln*2];
		
		fread(lp,sizeof(int),ln*2,f);
		
		fclose(f);	
		
		
		
		
		vector<LINE> lines;
		LINE line;
		
		int i,j,k,m;
		int spid,epid;
		
		for(m=0;m<ln*2;m+=2){
			spid=lp[m];
			epid=lp[m+1];
			//something important:
			//	poly vertex stored in obj file uses 1-based index, 
			//	however, poly vertex in maya is 0-based.
			//	we need to use "id-1" for matching the vertex order.

			
			for(i=0;i<pfaces.size();i++){
				for(j=0;j<pfaces[i].vtxid.size();j++){
					if(pfaces[i].vtxid[j]-1 == spid){
						for(k=0;k<pfaces[i].vtxid.size();k++){
							if(pfaces[i].vtxid[k]-1 == epid){
								
								//cout<<"sp:"<<spid<<", ep:"<<epid<<endl;
								
								
								line.sp.x=uvs[pfaces[i].uvid[j]-1].x;
								line.sp.y=uvs[pfaces[i].uvid[j]-1].y;
								
								
								line.ep.x=uvs[pfaces[i].uvid[k]-1].x;
								line.ep.y=uvs[pfaces[i].uvid[k]-1].y;
								
								lines.push_back(line);
								//cout<<"end"<<endl;
							}
						}
						
					}
					
				}
			}
			
			
		}
		
		Image image( Geometry(imgsize,imgsize), Color("black")  ); 
		
		image.strokeColor("white"); // Outline color
		image.fillColor("black"); // Fill color
		image.strokeWidth(linewidth);
		
		
		for(i=0;i<lines.size();i++){
			
			image.draw( DrawableLine(lines[i].sp.x*imgsize,(1-lines[i].sp.y)*imgsize, lines[i].ep.x*imgsize,(1-lines[i].ep.y)*imgsize) );
		}
		image.write( argv[3] ); 
		
	}
	
	else {
		cout<<"usage:\n	uvdraw objfile uvlfile outimage";
	
	}
	return 0;
	
}

