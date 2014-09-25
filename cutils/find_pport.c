#include <stdio.h>

#if defined __GLIBC__
    #include <sys/io.h>
#else
    #include <unistd.h>
    #include <asm/io.h>
#endif

int main(){
    register int i, port = 0;
    const int base_addr[3] = {0x3bc, 0x378, 0x278};

    if(iopl(3) != 0){
        fprintf(stderr, "find_pport: Cannot set I/O permissions\n");
        return(127);
    }

    for(i = 0; i < 3; i++){
        outb_p(0, base_adr[i]);
        if(inb_p(base_adr[i]) == 0)
            port = base_adr[i];
    }

    if(port == 0){
        fprintf(stderr, "find_pport: No parallel port found.\n");
        return 127;
    }

    printf("Parallel port found at 0x%x.\n", port);

    return 0;
}
