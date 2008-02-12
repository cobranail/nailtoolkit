#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <tiffio.h>
int cache_reader(const char *file);
void reverse_int(int *data);
void reverse_float(float *data);
int tiff2dens(int numd,const char * argv[]);

int main (int argc, const char * argv[]) {
	
	tiff2dens(16,argv);
	
    return 0;
}

int cache_reader(const char *file){

	char cacheheader[12];
	char stim[8];
	unsigned int stim_data;
	char etim[8];
	unsigned int etim_data;
	char type[8];
	unsigned int type_data;
	char rate[8];
	unsigned int rate_data;
	char fluidheader[12];
	
	char time[8];
	unsigned int time_data;
	char wres[8];
	unsigned int wres_data;
	char hres[8];
	unsigned int hres_data;
	char dres[8];
	unsigned int dres_data;
	char numd[8];
	unsigned int numd_data;
	
	char dens[8];
	
	float dvol1;
	
	FILE *fp;
	fp=fopen("fc2.mcfp","r");
	
	fread(cacheheader,sizeof(char),12,fp);
	fread(stim,sizeof(char),8,fp);
	fread(&stim_data,sizeof(int),1,fp);
	fread(etim,sizeof(char),8,fp);
	fread(&etim_data,sizeof(int),1,fp);
	fread(type,sizeof(char),8,fp);
	fread(&type_data,sizeof(int),1,fp);
	fread(rate,sizeof(char),8,fp);
	fread(&rate_data,sizeof(int),1,fp);
	fread(fluidheader,sizeof(char),12,fp);
	
	fread(time,sizeof(char),8,fp);
	fread(&time_data,sizeof(int),1,fp);
	fread(wres,sizeof(char),8,fp);
	fread(&wres_data,sizeof(int),1,fp);
	fread(hres,sizeof(char),8,fp);
	fread(&hres_data,sizeof(int),1,fp);
	fread(dres,sizeof(char),8,fp);
	fread(&dres_data,sizeof(int),1,fp);
	fread(numd,sizeof(char),8,fp);
	fread(&numd_data,sizeof(int),1,fp);	
	fread(dens,sizeof(char),8,fp);
	
	
	reverse_int(&stim_data);
	reverse_int(&etim_data);
	reverse_int(&type_data);
	reverse_int(&rate_data);
	reverse_int(&time_data);
	reverse_int(&wres_data);
	reverse_int(&hres_data);
	reverse_int(&dres_data);
	reverse_int(&numd_data);
	
	
	fseek(fp,0xBCL,0);
	fread(&dvol1,sizeof(float),1,fp);
	
	reverse_float(&dvol1);
	
	
	
	fclose(fp);
	
	return numd_data;

}


int tiff2dens(int numd,const char * argv[]){

	FILE *fp;
	fp=fopen(argv[2],"rb+"); //fluidcache, must use "rb+" to get the valid result.
	float dens;
	unsigned long offset=0x8C;
	fseek(fp,offset,0);
	
    TIFF* tif = TIFFOpen(argv[1], "r");
    if (tif) {
	uint32 w, h, i=0, j=0,r,g,b;
	size_t npixels;
	uint32* raster;

	TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &w);
	TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &h);
	npixels = w * h;
	raster = (uint32*) _TIFFmalloc(npixels * sizeof (uint32));
	if (raster != NULL) {
	    if (TIFFReadRGBAImage(tif, w, h, raster, 0)) {
	    
		    for(i = h - 1; i != -1; i--){
			    for(j = 0; j < w; j++){
				    r = TIFFGetR(raster[i * w + j]);
				    g = TIFFGetG(raster[i * w + j]);
				    b = TIFFGetB(raster[i * w + j]);
					dens=r/255.0;
					reverse_float(&dens);
					fwrite(&dens,sizeof(float),1,fp);


			    }
			    
		    }
	    }
	    _TIFFfree(raster);
	}
	TIFFClose(tif);
    }	
	
	fclose(fp);

 return 0;
}


void reverse_int(int *data){

	char *sdata= (char *)data;
	
	char tmp[4];
	tmp[0]=sdata[3];
	tmp[1]=sdata[2];
	tmp[2]=sdata[1];
	tmp[3]=sdata[0];
	
	
	sdata[0]=tmp[0];
	sdata[1]=tmp[1];
	sdata[2]=tmp[2];
	sdata[3]=tmp[3];
	
}

void reverse_float(float *data){

	char *sdata= (char *)data;
	
	char tmp[4];
	tmp[0]=sdata[3];
	tmp[1]=sdata[2];
	tmp[2]=sdata[1];
	tmp[3]=sdata[0];
	
	
	sdata[0]=tmp[0];
	sdata[1]=tmp[1];
	sdata[2]=tmp[2];
	sdata[3]=tmp[3];
	
}