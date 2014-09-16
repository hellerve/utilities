#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <time.h>
#include <string.h>

static inline void usage(){
    printf("Usage: filestat filename\n");
    exit(0);
}

static inline void die(int code, char* message){
    fprintf(stderr, "%s\n", message);
    exit(code);
}

int main(int argc, char **argv){
    struct stat status;

    if((argc != 2) || (strcmp(argv[1], "-h") == 0))
        usage();

    if(stat(argv[1], &status) != 0)
        die(127, "Cannot get file status.\n");

    printf("File/Dir name:\t%s\nSize:\t\t%ld bytes\n", argv[1], status.st_size);
    if(S_ISDIR(status.st_mode))
        printf("File type:\tdirectory\n");
    else if(S_ISREG(status.st_mode))
        printf("File type:\tregular file\n");
    if(S_ISCHR(status.st_mode))
        printf("Device type:\tcharacter device\n");
    else if(S_ISREG(status.st_mode))
        printf("Device type:\tblock device\n");
    else if(S_ISFIFO(status.st_mode))
        printf("Device type:\tfifo device\n");
    else if(S_ISSOCK(status.st_mode))
        printf("Device type:\tsocket\n");
    printf("Protection:\t%o\nOwner:\t\t%d\nLast modified:\t%s", 
            status.st_mode & 0x1ff, status.st_uid, ctime(&(status.st_mtime)));

    return 0;
}
