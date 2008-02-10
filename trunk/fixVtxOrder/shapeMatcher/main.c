/* 
 * File:   main.c
 * Author: Liu Shengjie
 *
 * Created on December 15, 2007, 11:46 AM
 * Jan 15, 2008
 *		Fix "Bus error" issue.
 *		Cleanup source.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

//从文件中读取面点的信息，保存在info中
void getFVInfo(int **info, int *infosize, const char *filename);

//unused
void testoutput(int *array,int n);

//从文件中读取映射面和点的关系
void getFVMap(int *map, const char *filename);

//把数组右移一个元素，sp是起始位置，只循环移动从sp开始的向后n个元素
void shiftArrayRight(int *array, int sp, int n);

//对齐数组，把dest的点数组向右循环移动offset个元素
void alignArray(int *array, int sp, int n, int offset);

//unused
int initGetFVInfo(int **srcInfo, int *srcInfoS,int **destInfo, int *destInfoS ,int *fvMap);

//输出完成映射后的点，无重复，n就是物体上点的个数
void outputVtxMapper(const char *filename,int *srcVtxList,int *destVtxList,int n);



typedef struct Face{
int id;
int vtxNum;
int *vtx;
struct Face *next;
}Face,*pFace;

typedef struct faceList{
 Face *faces;
 int length;
}faceList,*pFaceList;

//从list移除面id，并且返回面id的地址
Face *deleteFaceById(faceList *list,int id);

//unused
void insertFaceWithOrder(faceList *list, Face *face);

//在list的最后追加face
void appendFace(faceList *list,Face *face);

//按照src和dest的面和点的拓扑关系对齐点，srcFid和srcVid分别是src中要对应的面和点的id，移动操作实施在destlist中的面点上
void alignByFV(faceList *srclist, faceList *destlist, int srcFid,int srcVid,int destFid,int destVid);

//
void alignByVV(faceList *srclist, faceList *destlist, int srcVid1,int srcVid2,int destVid1,int destVid2,int srcFid, int destFid);

//创建一个面的节点
Face *createFace(int id,int vtxNum,int *vtx);

//unused
void distroyFace(Face *face);

//根据面id来定位面，并返回地址
Face *locateFaceByF(faceList *list,int Fid);

//unused 根据有序2点的id来定位面，并返回面的地址
Face *locateFaceByV(faceList *list,int Vid1,int Vid2);

//根据有序2点的id来定位面，并返回面的id
int getFaceIdByVV(faceList *list, int Vid1,int Vid2);

//映射所有的面点，smappedFaceArray保存映射后的src的有序面的id，smappedVtxArray保存映射后的src的有序点的id，FEinfo未使用，mapper是用户给出的映射关系
void mapAllFV(int *smappedFaceArray,int *smappedVtxArray,int *dmappedFaceArray,int *dmappedVtxArray,int *FEinfo,faceList *srclist,faceList *destlist,int *mapper);


int main (int argc, const char * argv[]) {
    // insert code here...
    


    if(argc!=5){
		puts("argv[] missing!");
		puts("Usage:shapeMatcher srcFVInfoFile destFVInfoFile mapperFile outputFile");
		return -1;
	}
	
	int *srcInfo[3],*destInfo[3];
	int srcInfoS[2],destInfoS[2];	//infoS[0]存储顶点数，infoS[1]存储面数
	int fvMap[4];


        int i=0;
        faceList sflist;
        sflist.faces=NULL;
        sflist.length=0;
        Face *sfnode=NULL;
        
        faceList dflist;
        dflist.faces=NULL;
        dflist.length=0;
        Face *dfnode=NULL;
        
        int *smappedFaceArray=NULL,*smappedVtxArray=NULL;
        int *dmappedFaceArray=NULL,*dmappedVtxArray=NULL;
        int *FEinfo;
        
            
	getFVInfo(srcInfo,srcInfoS,argv[1]);
	getFVInfo(destInfo,destInfoS,argv[2]);
	
	if(srcInfoS[0]!=destInfoS[0] || srcInfoS[1]!=destInfoS[1]) {
		
		puts("vtxNum or faceNum mismatch.Exit.\n");
		return -1;
		
	}
	
	getFVMap(fvMap,argv[3]);
	

        
		smappedVtxArray=(int *)malloc(sizeof(int)*(srcInfoS[0]));
		smappedFaceArray=(int *)malloc(sizeof(int)*(srcInfoS[1]));

		dmappedVtxArray=(int *)malloc(sizeof(int)*(destInfoS[0]));
		dmappedFaceArray=(int *)malloc(sizeof(int)*(destInfoS[1]));
		
		FEinfo=(int *)malloc(sizeof(int)*(destInfoS[1]));
		

        for(i=0;i<srcInfoS[1];i++){
            
            sfnode=createFace(i,srcInfo[1][i],(*(srcInfo+2)+srcInfo[0][i]));
            appendFace(&sflist,sfnode);
          
     
	        dfnode=createFace(i,destInfo[1][i],(*(destInfo+2)+destInfo[0][i]));
	        appendFace(&dflist,dfnode);
			
			if(sfnode->vtxNum!=dfnode->vtxNum) {
				printf("Topology mismatch.src face %d is different from dest face %d. Exit\n",sfnode->id,dfnode->id);
				return -1;
			}
			
	            
	    }
     
	    
	
	    mapAllFV(smappedFaceArray, smappedVtxArray,dmappedFaceArray, dmappedVtxArray,FEinfo,&sflist, &dflist,fvMap);
	    
	    
		
		//优化映射后点的数量，去掉重复的点
	    int *svl=NULL,*dvl=NULL;
		//tag是重复点标志
	    int len=srcInfoS[0],tag=0,j=0,k=0;
	    svl=(int *)malloc(sizeof(int)*(srcInfoS[0]));
	    dvl=(int *)malloc(sizeof(int)*(destInfoS[0]));
	    
	    for(i=0;i<len;i++){
	    	tag=0;
	    	for(j=0;j<i;j++){
	    		if(svl[j]==smappedVtxArray[i]) tag=1;
	    	}
	    	
	    	if(!tag) {
	    		svl[k]=smappedVtxArray[i];
	    		dvl[k]=dmappedVtxArray[i];
	    		k++;
	    	}
	    	
	    }
	    
	    
	outputVtxMapper(argv[4],svl,dvl,k);
    return 0;
}

Face *createFace(int id,int vtxNum,int *vtx){
    
    Face *face=(Face *)malloc(sizeof(Face));
    
    
    face->id=id;
    face->vtxNum=vtxNum;
    
    face->vtx=(int *)malloc(sizeof(int)*vtxNum);
    
    while(vtxNum>0){
        vtxNum-=1;
        face->vtx[vtxNum]=vtx[vtxNum];
    }
    face->next=NULL;
    return face;

}

void appendFace(faceList *list,Face *face){
    Face *ptr=list->faces;
	
	if(list->length==0){
		
		list->faces=face;
		
	}
	else {
 
        while(ptr->next!=NULL){

            ptr=ptr->next;

        }
        ptr->next=face;

	}

    list->length++;
}


Face *locateFaceByF(faceList *list, int Fid){
	
	Face *ptr=list->faces;
	while(ptr!=NULL){
		
		if(ptr->id==Fid) return ptr;
		ptr=ptr->next;
	}
	return NULL;
}


Face *locateFaceByV(faceList *list, int Vid1,int Vid2){
	
	Face *ptr=list->faces;
	int j=0,n;
	while(ptr!=NULL){
		n=ptr->vtxNum;
		for(j=n-1;j>=0;j--){
			
			if(ptr->vtx[j]==Vid1) {
				
				if(ptr->vtx[(j+n-1)%n]==Vid2 || ptr->vtx[(j+n+1)%n]==Vid2) return ptr; //目前的测试都正常，不过可能会有不能工作的情况 
				
				/* 
				 
				for(k=n-1;k>=0;k--){
					if(ptr->vtx[k]==Vid2) return ptr;
				} 
												  
				*/
			}
		
		}
		
		ptr=ptr->next;
	}
	return NULL;
	
}


int getFaceIdByVV(faceList *list, int Vid1,int Vid2){
	
	Face *ptr=list->faces;
	int j=0,n;
	while(ptr!=NULL){
		n=ptr->vtxNum;
		for(j=n-1;j>=0;j--){
			
			if(ptr->vtx[j]==Vid1) {
				
				if(ptr->vtx[(j+n-1)%n]==Vid2 || ptr->vtx[(j+n+1)%n]==Vid2) return ptr->id; //目前的测试都正常，不过可能会有不能工作的情况
				
				/* 
				 
				for(k=n-1;k>=0;k--){
					if(ptr->vtx[k]==Vid2) return ptr->id;
				} 
												  
				*/
			}
		
		}
		
		ptr=ptr->next;
	}
	return -1;
}

void alignByFV(faceList *srclist, faceList *destlist, int srcFid, int srcVid, int destFid, int destVid) {

	Face *srcface=locateFaceByF(srclist, srcFid);
	Face *destface=locateFaceByF(destlist, destFid);

	if (srcface!=NULL && destface!=NULL) {

		int i=0;
		for (i=0; i<srcface->vtxNum && srcVid!=srcface->vtx[i]; i++)
			;
		int slp=i;

		for (i=0; i<destface->vtxNum && destVid!=destface->vtx[i]; i++)
			;
		int dlp=i;

		alignArray(destface->vtx, 0, destface->vtxNum, slp-dlp);
	}

}
void alignByVV(faceList *srclist, faceList *destlist, int srcVid1,int srcVid2,int destVid1,int destVid2, int srcFid,int destFid) {
	
		Face *srcface=locateFaceByV(srclist, srcVid1,srcVid2);   //定位face需要2个顶点
		Face *destface=locateFaceByV(destlist, destVid1,destVid2);
	
	
		int i=0;
		for(i=0;i<srcface->vtxNum && srcVid1!=srcface->vtx[i];i++); //确定顶点的顺序只需要一个顶点  
		int slp=i;

		for(i=0;i<destface->vtxNum && destVid1!=destface->vtx[i];i++);
		int dlp=i;

		alignArray(destface->vtx, 0, destface->vtxNum, slp-dlp);
	
}


Face *deleteFaceById(faceList *list,int id){
    if (list->length>0) {
		list->length--;

		Face *ptr=list->faces;
		Face *dptr=list->faces;

		if (ptr->id==id) { //first one is.
			list->faces=ptr->next;
			ptr->next=NULL;
			return ptr;
		}
		else {
			while(ptr!=NULL){
				if(ptr->id==id){
		            dptr->next=ptr->next;
		            ptr->next=NULL;
					return ptr;
				}
				dptr=ptr;
				ptr=ptr->next;
				
			}
			
		}

	}

        return NULL;
    
 
   

}


void mapAllFV(int *smappedFaceArray, int *smappedVtxArray, int *dmappedFaceArray, int *dmappedVtxArray, int *FEinfo, faceList *srclist, faceList *destlist, int *mapper) {
	
	Face *snode=NULL, *dnode=NULL, *smptr=NULL, *dmptr=NULL;
	static faceList smlist, dmlist; //必须用static声明，否则就会bus error。
	smlist.faces=NULL;
	dmlist.faces=NULL;
	smlist.length=0;
	smlist.length=0;
	
	//vp记录已经映射的点的个数，vf记录已经映射面的个数
	int fp=0, vp=0, i=0, sfid=0, dfid=0;
	int n=0;
	
	alignByFV(srclist, destlist, mapper[0], mapper[1], mapper[2], mapper[3]); //对齐参考面和参考顶点
	
	snode=deleteFaceById(srclist, mapper[0]); //把参考面从面列表中移动到已对齐面列表中
	dnode=deleteFaceById(destlist, mapper[2]);
	appendFace(&smlist, snode);
	appendFace(&dmlist, dnode);
	
	smappedFaceArray[fp]=mapper[0]; //src与dest的面对应关系 
	dmappedFaceArray[fp]=mapper[2];
	FEinfo[fp]=0; //记录每个已对齐面中已经访问的边数
	fp++;
	for (i=0; i<snode->vtxNum; i++) {
		smappedVtxArray[vp+i]=snode->vtx[i]; //src与dest的点对应关系
		dmappedVtxArray[vp+i]=dnode->vtx[i];
	}
	vp+=snode->vtxNum;
	
	smptr=smlist.faces;
	dmptr=dmlist.faces;
	
	while(srclist->length>0){
		
		smptr=smlist.faces;
		dmptr=dmlist.faces;
		
		while (smptr!=NULL) {
		//从所有已经映射的面中取出有序的2点，每新增加一个映射面都会重新测试所有映射面中的所有每一对有序点是否连着一个未映射的面
		//不能和上一级的while合并，否则会导致有些面被错过	
			n=smptr->vtxNum;
			for (i=0; i<n; i++) {
				
				sfid=getFaceIdByVV(srclist, smptr->vtx[i], smptr->vtx[(i+1)%n]); //根据已经映射的面上的几何相邻的2点来确定与之相连的未映射面的id，
				dfid=getFaceIdByVV(destlist, dmptr->vtx[i], dmptr->vtx[(i+1)%n]);
				
				if (sfid>=0 && dfid>=0) {
					
					alignByFV(srclist, destlist, sfid, smptr->vtx[i], dfid,
							  dmptr->vtx[i]);
					
					snode=deleteFaceById(srclist, sfid); //把参考面从面列表中移动到已对齐面列表中
					dnode=deleteFaceById(destlist, dfid);
					appendFace(&smlist, snode);
					appendFace(&dmlist, dnode);
					
					smappedFaceArray[fp]=sfid; //src与dest的面对应关系 
					dmappedFaceArray[fp]=dfid;
					//FEinfo[fp]++; //记录每个已对齐面中已经访问的边数
					fp++;
					for (i=0; i<snode->vtxNum; i++) {
						smappedVtxArray[vp+i]=snode->vtx[i]; //src与dest的点对应关系
						dmappedVtxArray[vp+i]=dnode->vtx[i];
						
					}//for (i=0; i<snode->vtxNum; i++)
					vp+=snode->vtxNum;
			
				}//if (sfid>=0 && dfid>=0)
			}
			
			smptr=smptr->next;
			dmptr=dmptr->next;
			
		}//while (smptr!=NULL)
		
	}//while(srclist->length>0)
	
}


void getFVInfo(int **info, int *infosize ,const char *filename){

	char buffer[1024];
	char *ns;
	
	FILE *srcFp;
	
	int *fvLnrSP=NULL,*fvLnrN=NULL;//fvLnrSP=face-vertex start positon，fvLnrN=number of vertex of each face
	int *vtxGroup=NULL;	//vertexs
	int vtxlen=0,fn=0;

	
	if((srcFp=fopen(filename,"r"))!=NULL) {
		
		fgets(buffer,1024,srcFp);
		while(!feof(srcFp)){
			if(strlen(buffer)>1) {

				ns=strtok(buffer," \n"); //对buffer用空格和'\n'进行截断，获取face id
				fn++;
				fvLnrSP=(int*)realloc((void*)fvLnrSP,(sizeof(int)*fn));
				fvLnrSP[fn-1]=vtxlen;
				ns=strtok(NULL," \n");	//获取面的点数
				fvLnrN=(int*)realloc((void*)fvLnrN,(sizeof(int)*fn));
				fvLnrN[fn-1]=atoi(ns);
				
				
				ns=strtok(NULL," \n"); //开始获取vertex id
				while(ns!=NULL){
					vtxlen++;
					
					vtxGroup=(int*)realloc((void*)vtxGroup,(sizeof(int)*vtxlen));
					vtxGroup[vtxlen-1]=atoi(ns);
					ns=strtok(NULL," \n");//这里也是用空格和'\n'
					
				}
			}
			fgets(buffer,1024,srcFp);
			
		}
		fclose(srcFp);
	}
	
	infosize[0]=vtxlen; //
	infosize[1]=fn; //face number
	
	info[0]=fvLnrSP;
	info[1]=fvLnrN;
	info[2]=vtxGroup;

}
void getFVMap(int *map,const char *filename){

	char buffer[1024];
	char *ns;
	FILE *fp;
	if((fp=fopen(filename,"r"))!=NULL){
		fgets(buffer,1024,fp);
		ns=strtok(buffer," \n");
		map[0]=atoi(ns);
		ns=strtok(NULL," \n");
		map[1]=atoi(ns);
		ns=strtok(NULL," \n");
		map[2]=atoi(ns);
		ns=strtok(NULL," \n");
		map[3]=atoi(ns);
	}
	fclose(fp);
}

void outputVtxMapper(const char *filename, int *srcVtxList,int *destVtxList,int n){
	int i=0;
	FILE *fp;
	if((fp=fopen(filename,"w"))!=NULL){
		for(i=0;i<n;i++){
			fprintf(fp,"%d %d\n",srcVtxList[i],destVtxList[i]);
		}
	}
	fclose(fp);
}

void testoutput(int *array,int n){
	int i=0;
	for(i=0;i<n;i++){
		printf("%d ",array[i]);
	}
	putchar('\n');
}

void shiftArrayRight(int *array, int sp, int n){


	int tmp=array[sp+n-1];
	int i;
	for(i=n-1;i>0;i--){
		array[sp+i]=array[sp+i-1];	
	}
	array[sp]=tmp;
}

void alignArray(int *array, int sp, int n, int offset){

	if(offset<0) offset=offset+n;
	while(offset>0){
		shiftArrayRight(array,sp,n);
		offset--;
	}
}

int initGetFVInfo(int **srcInfo, int *srcInfoS,int **destInfo, int *destInfoS ,int *fvMap){
/***	
	slp: (src)local position
	sgp: (src)global position
	sop: (src)original position
	
	eg: abcdefg[hijkl]mn..
		i: lp=1, op=7, gp=op+lp=8
	
***/	
	int i=0;
	int sop=srcInfo[0][fvMap[0]];
	for(i=0;i<srcInfo[1][fvMap[0]] && fvMap[1]!=srcInfo[2][sop+i];i++); 
	int slp=i;

	
	int dop=destInfo[0][fvMap[2]];
	for(i=0;i<destInfo[1][fvMap[2]] && fvMap[3]!=destInfo[2][dop+i];i++);
	int dlp=i;

	
	return (slp-dlp);
	
}
