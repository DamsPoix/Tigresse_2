#include "UBLOX.hpp"

void UBLOX::begin(int baudrate){
    Serial1.begin(baudrate);
    delay(1000);
    writeTrame(airmodeTrame, 44);
}

void UBLOX::read(){
    while(Serial1.available() > 0){ //on read 
        char carac = Serial1.read();
        if(carac == '\n'){
            String cmd = serialBuffer.substring(1, 6);
            if(cmd == "GPRMC" || cmd == "GPGSV"){
               processData(serialBuffer); 
            }
            
            serialBuffer = "";
        }else if(carac != 13){
            serialBuffer += carac;
        }
    }
}

void UBLOX::writeTrame(uint8_t* trame, uint8_t length){
    for(uint8_t i = 0; i < length; i++){
        Serial1.write(trame[i]);
    }
}

void UBLOX::processData(String str){
    String splited[30];
    uint16_t last_index = 0;
    uint8_t index_array = 0;
    for(uint16_t i = 0; i < str.length(); i++){
        if(str.charAt(i) == ','){
            splited[index_array] = str.substring(last_index+1, i);
            index_array ++;
            last_index = i;
        }
    }
    splited[index_array] = str.substring(last_index+1, str.length());

    /*
    Serial.print("reading stupid splited values from : ");
    Serial.println(serialBuffer);
    for(int i = 0; i < index_array+1; i++){
        Serial.println(splited[i]);
    }
    */

    if(splited[0] == "GPRMC"){ //Recommended minimum data

        //time convertion
        if(splited[1] != ""){
            time = splited[1].substring(0,2) + ":" + splited[1].substring(2, 4) + ":" + splited[1].substring(4, 9);
        }else{
            time = "N/A";
        }
        
        //fix status convertion
        if(splited[2] == "A"){
            fixed = true;
        }else{
            fixed = false;
        }

        //latitude convertion
        if(splited[3] != ""){
            lat = splited[3].substring(0,2).toFloat();
            lat += splited[3].substring(2,10).toFloat()/60;
        }

        //latitude indicator
        if(splited[4] != ""){
            lat_indicator = splited[4].charAt(0);
        }

        //longitude convertion
        if(splited[5] != ""){
            lon = splited[5].substring(0,3).toFloat();
            lon += splited[5].substring(3,11).toFloat()/60;
        }

        //longitude indicator
        if(splited[6] != ""){
            lon_indicator = splited[6].charAt(0);
        }

        //data convertion
        if(splited[9] != ""){
            date = splited[9].substring(0, 2) + "/" + splited[9].substring(2, 4) + "/20" + splited[9].substring(4,6);
        }


    }else if(splited[0] == "GPGSV"){  //GNSS satellites in view
        //process in view data
        inView = splited[3].toInt();
    }else{
    //default

    }
}


String UBLOX::toString(){
    String buff = "";
    buff += date;
    buff += " ";
    buff += time;
    if(fixed){
        buff += " fixed ";
        buff += "(";
        buff += inView;
        buff += "/12) ";
        buff += String(lat,7);
        buff += lat_indicator;
        buff += " ";
        buff += String(lon,7);
        buff += lon_indicator;
    }else{
        buff += " unfixed ";
        buff += "(";
        buff += inView;
        buff += "/12) ";
    }

    return buff;
}

String UBLOX::getTime(){
  return time;
}

String UBLOX::getDate(){
  return date;
}

String UBLOX::getLat(){
  return String(lat,7);
}

String UBLOX::getLon(){
  return String(lon,7);
}
