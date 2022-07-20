#ifndef UBLOX_HPP_INCLUDED
#define UBLOX_HPP_INCLUDED

#include "Arduino.h"

class UBLOX
{
    public :
        void begin(int baudrate);
        void read();
        String toString();
        String getTime();
        String getDate();
        String getLat();
        String getLon();


    private :
        float lat = -1;
        char lat_indicator = '0';
        float lon = -1;
        char lon_indicator = '0';
        float nbrSat = 0;
        bool fixed = false;
        uint8_t inView = 0;
        String time = "";
        String date = "";
        uint8_t airmodeTrame[44] = {0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x08, 0x03, 0x00, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00, 0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00, 0x64, 0x00, 0x2C, 0x01, 0x00, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4F, 0x1F};
        String serialBuffer = "";
        
        
        void writeTrame(uint8_t* trame, uint8_t length);
        void processData(String str);

};

#endif //UBLOX_HPP_INCLUDED
