/*
 ============================================================================
 Name        : lsystem.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <tiffio.h>
#include "queue.h"



typedef struct arstate{
	float x,y;
	float agl;
	
	SLIST_ENTRY(arstate) entries;
	
} ARState;

typedef struct seg{
	float spx,spy;
	float epx,epy;
	char drawable;
	char color[3];
	SLIST_ENTRY(seg) entries;
	
} Seg;

typedef struct bound{
	float xmax;
	float ymax;
	float xmin;
	float ymin;
	
} Bound;

float max(float a, float b){
	
	if(a>b) return a;
	else return b;
	
}

float min(float a, float b){
	
	if(a<b) return a;
	else return b;
}

void drawPixel(char *buffer, int w, int h, int x, int y, char rgb[]){
	
	//image bound check
	x=x>(w-1)?(w-1):(0>x?0:x);
	y=y>(h-1)?(h-1):(0>y?0:y);
	
	
	buffer[y*(w)*3+x*3+0]=rgb[0];
	buffer[y*(w)*3+x*3+1]=rgb[1];
	buffer[y*(w)*3+x*3+2]=rgb[2];
	

}


void drawLine(char *buffer, int w, int h, float sp[], float ep[], char rgb[]){
	
	float x1=sp[0];
	float y1=sp[1];
	float x2=ep[0];
	float y2=ep[1];

	int step = (int)max(fabs(ep[0]-sp[0]), fabs(ep[1]-sp[1]));

	if (step!=0) {
		float dx=(x2-x1)/step;
		float dy=(y2-y1)/step;

		//printf("%f,%f, %f, %f\n", x1, y1, x2, y2);
		while (step>=0) {
			//printf("%d,%d,%d\n",step,(int)(x1+dx*step), (int)(y1+dy*step));
			drawPixel(buffer, w, h, (int)(x1+dx*step), (int)(y1+dy*step), rgb);

			step--;
		}
	}
	else {
		printf("%f,%f\n",ep[0]-sp[0],ep[1]-sp[1]);
		
	}

}

void drawFigure(char *raster, int width, int height, char *str){
	
	char *p;
	p=str;
	float step = 1;
	float da = M_PI_2/3.0;
	float a[2]={5,5};
	float b[2]={500,500};
	float sp[2],ep[2];
	char rgb[3];
  	rgb[0]=0;
	rgb[1]=255;
	rgb[2]=0;
	int i=1;
	
    SLIST_HEAD(slisthead, seg) line =
	 SLIST_HEAD_INITIALIZER(line);
     struct slisthead *headp;		     /* Singly-linked List head. */

     
     //state stack
     SLIST_HEAD(sliststack, arstate) stateStack = 
     SLIST_HEAD_INITIALIZER(stateStack);
 
     
     
     Bound bnd;
     bnd.xmax=0;
     bnd.xmin=0;
     bnd.ymax=0;
     bnd.ymin=0;
     
     ARState state;
     state.x=0;
     state.y=0;
     state.agl=0;
     
     
     Seg * np;
     ARState * asp;
     
     SLIST_INIT(&line); 		     /* Initialize the list. */
     SLIST_INIT(&stateStack);
     
     while (*p!='\0') {
    	 
    	 if(*p=='F'){
    		 
		     np = malloc(sizeof(struct seg));	/* Insert at the head. */
		     np->spx=state.x;
		     np->spy=state.y;
		     
		     state.x+=step*cos(state.agl);
		     state.y+=step*sin(state.agl);
		     
     
		     np->epx=state.x;
		     np->epy=state.y;
		     
		     
		     np->drawable=1;
		     
		     bnd.xmax=max( max(bnd.xmax, np->spx), np->epx );
		     bnd.xmin=min( min(bnd.xmin, np->spx), np->epx );
		     bnd.ymax=max( max(bnd.ymax, np->spy), np->epy );
		     bnd.ymin=min( min(bnd.ymin, np->spy), np->epy );
		     
		     {SLIST_INSERT_HEAD(&line, np, entries);}
		     
		     i++;
		  
    		 
    	 }
    	 
    	 else if (*p=='f') {
    		 
		     np = malloc(sizeof(struct seg));	/* Insert at the head. */
		     np->spx=state.x;
		     np->spy=state.y;
		     
		     state.x+=step*cos(state.agl);
		     state.y+=step*sin(state.agl);
		     
		     np->epx=state.x;
		     np->epy=state.y;
		     
		     np->drawable=0;
		     
		     bnd.xmax=max( max(bnd.xmax, np->spx), np->epx );
		     bnd.xmin=min( min(bnd.xmin, np->spx), np->epx );
		     bnd.ymax=max( max(bnd.ymax, np->spy), np->epy );
		     bnd.ymin=min( min(bnd.ymin, np->spy), np->epy );
		     
		     {SLIST_INSERT_HEAD(&line, np, entries);}
    	 }
    	 
    	 else if (*p=='+') {
    		 
    		 state.agl+=(da+(float)((random () % 200)-50));
    	 }
    	 else if (*p=='-') {
    		 state.agl-=(da+(float)((random () % 200)-50));
    	 }
    	 else if (*p=='[') {
    		 asp = malloc(sizeof(struct arstate));
    		 asp->x=state.x;
    		 asp->y=state.y;
    		 asp->agl=state.agl;
    		 
    		 {SLIST_INSERT_HEAD(&stateStack, asp, entries);}
    		 
    	 }
    	 else if (*p==']') {
    		 
    		 asp = SLIST_FIRST(&stateStack);
    		 SLIST_REMOVE_HEAD(&stateStack, entries);      /* Deletion from the head. */
    		 
    		 state.x=asp->x;
    		 state.y=asp->y;
    		 state.agl=asp->agl;
    		      
    		 free(asp);
    		 
    	 }   	 
    	 
    	 else
    	 {}
    	 p++;
    	 
     }//while
    
     float maxbound=max((bnd.xmax-bnd.xmin),(bnd.ymax-bnd.ymin));
     float offsetx=(maxbound-(bnd.xmax-bnd.xmin))/2.0;
     float offsety=(maxbound-(bnd.ymax-bnd.ymin))/2.0;
     
     
 	SLIST_FOREACH(np, &line, entries) {
 	    if (np->drawable==1 ) {
 	    	sp[0]=(np->spx+fabs(bnd.xmin)+offsetx)*(width-1)/maxbound;
 	    	ep[0]=(np->epx+fabs(bnd.xmin)+offsetx)*(width-1)/maxbound;
 	    	
 	    	sp[1]=(fabs(bnd.ymax)-(np->spy-offsety))*(height-1)/maxbound;
 	    	ep[1]=(fabs(bnd.ymax)-(np->epy-offsety))*(height-1)/maxbound;
 	    	//puts("checkpoint 3");
 	    	//printf("sp: %f , %f , %f , %f\n",ep[0],np->spx,sp[1],np->spy);
 	    	drawLine(raster, width, height, sp, ep, rgb);
 	    }
 	}
 	//printf("%f, %f, %f , %f\n",bnd.xmax,bnd.ymax,bnd.xmin,bnd.ymin);
	printf("i=%d\n",i);
}


void writetiff(char *str){
  TIFF *output;
  uint32 width, height;
  char *raster;
  
  char rgb[3];

  // Open the output image
  if((output = TIFFOpen("output.tif", "w")) == NULL){
    fprintf(stderr, "Could not open outgoing image\n");
    exit(42);
  }
  // We need to know the width and the height before we can malloc
  width = 1024;
  height = 1024;
  if((raster = (char *) malloc(sizeof(char) * width * height * 3)) == NULL){
    fprintf(stderr, "Could not allocate enough memory\n");
    exit(42);
  }
  // Magical stuff for creating the image
  
  //*raster=255;
  //*(raster+1)=255;
  //*(raster+2)=255;
  
  	rgb[0]=0;
	rgb[1]=255;
	rgb[2]=0;
  
	drawFigure(raster, width, height, str);

	
  // Write the tiff tags to the file
  TIFFSetField(output, TIFFTAG_IMAGEWIDTH, width);
  TIFFSetField(output, TIFFTAG_IMAGELENGTH, height);
  TIFFSetField(output, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT);
  TIFFSetField(output, TIFFTAG_COMPRESSION, COMPRESSION_LZW);
  TIFFSetField(output, TIFFTAG_PLANARCONFIG, PLANARCONFIG_CONTIG);
  TIFFSetField(output, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_RGB);
  TIFFSetField(output, TIFFTAG_BITSPERSAMPLE, 8);
  TIFFSetField(output, TIFFTAG_SAMPLESPERPIXEL, 3);
  // Actually write the image
  if(TIFFWriteEncodedStrip(output, 0, raster, width * height * 3) == 0){
    fprintf(stderr, "Could not write image\n");
    exit(42);
  }
  TIFFClose(output);
  
}



char * replaceString(char *str1, char *str2, char *str){
	char *tmpstr=NULL;
	char *newstr=NULL;
	
	newstr=(char*)malloc(sizeof(char)*(strlen(str)+1)*(strlen(str2)+1));
	
	char *newstrout;
	newstrout=newstr;
	
	
	while(*str!='\0'){

		if(*str=='F') {
			
			tmpstr=str2;

			while(*tmpstr!='\0') {
				*newstr=*tmpstr;
				newstr++;
				tmpstr++;
				
			}//while(*tmpstr!='\0')
			
		}//if
		else{
			*newstr=*str;
			newstr++;
		
		}//else
		str++;
	}//while
	*(++newstr)='\0';	puts("2");
	return newstrout;
	
}


int main(int argc, char *argv[]) {
	
	char *str="FF";
	char *rule1='F';
	char *rule2="F[+F]+F[-F]F";
	char *outstr;
	char *tmp;
	
	outstr=(char*)malloc(sizeof(char)*(strlen(str)+1));
	strcpy(outstr,str);
	int i=0;
	while(i<5) {
	/*	if(outstr!=NULL){
			free(outstr);
			outstr=NULL;
		}*/
		
		
		//puts("1");
		tmp=replaceString(rule1,rule2,outstr);
		//puts(tmp);
		free(outstr);
		outstr=tmp;
		i++;
	}
	
	writetiff(outstr);
	return EXIT_SUCCESS;
}
