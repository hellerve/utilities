#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <usb.h>

static inline void die(int code, const char* message){
    fprintf(stderr, "%s\n", message);
    exit(code);
}

int main(){
    register int i = 1;
    struct usb_bus *bus;
    struct usb_device *udev;
    usb_dev_handle *udevhd;
    static char buffer[256];

    usb_init();

    usb_find_busses();
    usb_find_devices();

    bus = ubs_get_busses();

    while(bus != NULL){
        printf("%d. Universial Serial Bus:\n", i++);
        udev = bus->devices;
        while(udev != NULL){
            udevhd = usb_open(udev);
            if(udevhd != NULL){
                if(udev->descriptor.iProduct)
                    usb_get_string_simple(udevhd, udev->descriptor.iProduct,
                            buffer, 256);
                else
                    buffer[0] = '\0';

                printf("\t%04X : %04X\t'%s'\n",
                        udev->descriptor.idVendor,
                        udev->descriptor.idProduct,
                        buffer);

                usb_close(udevhd);
            }
            udev = udev->next;
        }
        bus = bus->next;
    }

    if( i == 1)
        die(127, "No USB found");

    return 0;
}       
