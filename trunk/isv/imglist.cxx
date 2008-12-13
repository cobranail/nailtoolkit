/***
imglist.cxx
prase filename

cobranail@gmail.com
2008/12/13

***/
#include "imglist.h"


int load_images(TQHEAD *head, const char *filename)
{
	

		std::string regstr = "(^.*)(/)([^/]+?)([0-9]+)([.])([^./]+$)";
		boost::regex expression(regstr);
		std::string testString = filename;
		boost::smatch what;
		std::string::const_iterator start = testString.begin();
		std::string::const_iterator end = testString.end();
		boost::regex_search(start, end, what, expression);
		
		
		std::string path(what[1].first, what[1].second);
		std::string name(what[3].first, what[3].second);
		std::string index(what[4].first, what[4].second);
		std::string ext(what[6].first, what[6].second);
		//std::cout<< "path:" << path.c_str() << std::endl;
		//std::cout<< "name:" << name.c_str() << std::endl;
		//std::cout<< "index:" << index.c_str() << std::endl;
		//std::cout<< "ext:" <<ext.c_str() << std::endl;
		start = what[0].second;
		
		
		char buffer[65536];

		

		
		
		imgFile *np_temp,*np,*n1;

		     while (!TAILQ_EMPTY(head)) {
			     n1 = TAILQ_FIRST(head);
			     TAILQ_REMOVE(head, n1, entries);
			     delete n1;
		     }
		     
		int n=-1,i=0;
		
		DIR           *d;
		struct dirent *dir;
		d = opendir(path.c_str());
		
		
		if (d)
		{
			while ((dir = readdir(d)) != NULL)
			{
				sprintf(buffer, "%s", dir->d_name);
				n=-1;
				
				std::ostringstream idx;
				std::string ia;
				idx << index.length();
				ia=idx.str();
				
				//std::string regstr2="(^"+name+")([0-9]+{"+ia+"})(."+ext+"$)";
				std::string regstr2="("+name+")(([0-9]+){"+ia+"})([.]"+ext+")";
				
				//std::cout<<"regstr2:"<<regstr2.c_str()<<std::endl;
				//std::cout<<"buffer:"<<buffer<<std::endl;	
				boost::regex expression2(regstr2);
				
				//std::cout<<"search"<<std::endl;
				std::string testString(buffer);
				boost::smatch what;
				std::string::const_iterator start = testString.begin();
				std::string::const_iterator end = testString.end();
				
				
				
				
				
				if (boost::regex_search(start, end, what, expression2)){
					
					std::string index(what[2].first, what[2].second);
					
					
					start = what[0].second;
					n=atoi(index.c_str());
				}
				
				
				
				if(n>=0){
					np_temp=new imgFile;
					np_temp->filename=new char [strlen(buffer) + strlen( path.c_str() )+2];
					np_temp->index=n;
					np_temp->qindex=i;
					
					sprintf(np_temp->filename,"%s/%s",path.c_str(),buffer);
					//strcpy(np_temp->filename,buffer);
					
					TAILQ_INSERT_TAIL(head, np_temp, entries);
					i++;
				}
				
			}
			
			closedir(d);
		}
		
//		TAILQ_FOREACH(np, head, entries){			
//			printf("index:%d,qindex:%d,file:%s\n",np->index,np->qindex,np->filename);			
//		}
		return i;

}


