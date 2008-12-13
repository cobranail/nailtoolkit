#include <dirent.h> 
#include <stdio.h>

#include <boost/regex.hpp>
#include <iostream>
#include "queue.h"
#include <stdlib.h>
#include <string.h>
#include <cmath>
#include <sstream>
#include <string>

typedef struct imgfile{
	int index;
	int qindex;
	char *filename;
	TAILQ_ENTRY(imgfile) entries;
} imgFile;

typedef TAILQ_HEAD(tailhead, imgfile) TQHEAD;

int load_images(TQHEAD *head, const char *filename);

