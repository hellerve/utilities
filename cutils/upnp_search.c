#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/poll.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUF_SIZE 20000
#define TIMEOUT 3000
#define UPNP_ADDR "239.255.255.250"
#define UPNP_PORT 1900

static inline void die_close(int code,  int sock_fd, const char* message){
    fprintf(stderr, "%s\n", message);
    if(sock_fd > -1)
        close(sock_fd);
    exit(code);
}

int main(){
    register int sock_fd, length, i, err;
    struct sockaddr_in server_addr, from_addr;
    socklen_t addr_size;
    struct pollfd pollfd;
    static char buffer[BUF_SIZE];

    sock_fd = socket(PF_INET, SOCK_DGRAM, 0);
    if(sock_fd == -1)
        die_close(127, -1, "upnp_search: Cannot create new socket");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(UPNP_PORT);
    inet_aton(UPNP_ADDR, &(server_addr.sin_addr));

    strcpy(buffer, "M-SEARCH * HTTP/1.1\r\n"
                   "HOST: 239.255.255.250:190\r\n"
                   "MAN: \"ssdp:discover\"\r\n"
                   "MX: 2\r\n"
                   "ST: ssdp:all\r\n"
                   "\r\n");


    length = sendto(sock_fd, buffer, strlen(buffer), 0, 
                    (struct sockaddr *) &server_addr,
                    sizeof(struct sockaddr));

    if(length != strlen(buffer))
        die_close(127, sock_fd, "upnp_search: sendto() failed");

    pollfd.fd = sock_fd;
    pollfd.events = POLLIN | POLLPRI;
    i = 0;
    while(1){
        err = poll(&pollfd, 1, TIMEOUT);
        if(err < 0)
            die_close(127, sock_fd, "upnp_search(): poll() failed");
        else if(err == 0){
            if(i == 0)
                printf("<No response received.>\n");
            break;
        }
        else{
            addr_size = sizeof(struct sockaddr_in);
            length = recvfrom(sock_fd, buffer, BUF_SIZE-1, 0,
                    (struct sockaddr *)&from_addr,
                    &addr_size);

            if(length == -1)
                die_close(127, sock_fd, "upnp_search: recvfrom() failed");
            else{
                buffer[length] = '\0';
                printf("\33[1m---- Response from %s: ----\33[0m\n%s\n",
                    inet_ntoa(from_addr.sin_addr), buffer);
            }
            i = 1;
        }
    }
    close(sock_fd);
    return 0;
}
