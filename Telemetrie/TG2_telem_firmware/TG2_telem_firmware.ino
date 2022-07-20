#include "MPU9250.h"
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include "UBLOX.hpp"

//global pinout
#define INT_ALTI 5
#define INT_IMU 6
#define RF_TX 9
#define RF_EN 10
#define TRG 11
#define ALARM_LED 12
#define BUZZER_PIN 13
bool serial = true;
bool logSD = true;
bool liftoff = false;

//IMU parameters
MPU9250 mpu;
float mpuQuaternion[3];
float quaternionScalar;
float mpuAccel[3];
float mpuMag[3];
float worldAccel[3];
float worldSpeed[3] = {0,0,0};
float worldPos[3] = {0,0,0};
unsigned long last_millis;

//BMP parameters
Adafruit_BMP3XX bmp;
float initialPressure = 0;
float altitude = 0;
float temperature = 0;

//SD card parameters
File root;
String rootFilename = "/logs/";
String logBuffer;

//UBLOX MAX8
UBLOX gps;

//RF
int bitrate = 2400;
int rf_delay = 0;
int rf_index = 0;
String rf_trame = "";

void setup() {
  if(serial){
    Serial.begin(115200);
    Serial.println("Start telem...");
  }
  
  initPins();
  ringtone();
  
  initMPU();
  ackTone();
  initBMP();
  ackTone();
  gps.begin(9600);
  ackTone();

  
  if(logSD){
    init_SD();
    ackTone();
  }

  //on enable la RF
  digitalWrite(RF_EN, LOW);
  
  last_millis = millis();
}

void loop() {
  if (mpu.update()) {

    mpuQuaternion[0] = mpu.getQuaternionX();
    mpuQuaternion[1] = mpu.getQuaternionY();
    mpuQuaternion[2] = mpu.getQuaternionZ();
    quaternionScalar = mpu.getQuaternionW();

    mpuAccel[0] = -mpu.getAccX();
    mpuAccel[1] = mpu.getAccY();
    mpuAccel[2] = mpu.getAccZ();

    mpuMag[0] = mpu.getMagX();
    mpuMag[1] = mpu.getMagY();
    mpuMag[2] = mpu.getMagZ();

    float dot1 = 2.0f*dot(mpuQuaternion, mpuAccel);
    float dot2 = (quaternionScalar*quaternionScalar) - dot(mpuQuaternion,mpuQuaternion);
    float cross1[3] = {0,0,0};
    cross(mpuQuaternion, mpuAccel, cross1);

    worldAccel[0] = dot1*mpuQuaternion[0] + dot2*mpuAccel[0] + 2.0f*quaternionScalar*cross1[0];
    worldAccel[1] = dot1*mpuQuaternion[1] + dot2*mpuAccel[1] + 2.0f*quaternionScalar*cross1[1];
    worldAccel[2] = dot1*mpuQuaternion[2] + dot2*mpuAccel[2] + 2.0f*quaternionScalar*cross1[2];

    //removing gravitationnal part
    worldAccel[2] -= 1; //ca a l air d etre en g askip mais c est chelou

    int dt = millis() - last_millis;
    last_millis = millis();

    //worldSpeed[0] += worldAccel[0]*9.81f*dt/1000.0f; //convertis en m/s
    //worldSpeed[1] += worldAccel[1]*9.81f*dt/1000.0f; //convertis en m/s
    worldSpeed[2] += worldAccel[2]*9.81f*dt/1000.0f; //convertis en m/s

    //worldPos[0] += worldSpeed[0]*dt/1000.0f; //convertis en m
    //worldPos[1] += worldSpeed[1]*dt/1000.0f; //convertis en m
    //worldPos[2] += worldSpeed[2]*dt/1000.0f; //convertis en m

    if(!liftoff){
      worldSpeed[2] = 0; //tant que pas decolle, egal a zero
    }

    if(millis() > 30000){//simule le liftoff vu que le trigger est pas envoye
      liftoff = true;
    }

    //traitement de l'altimetre : 
    if(bmp.performReading()){
      if(!liftoff){
        initialPressure = (initialPressure + bmp.pressure)/2;
      }else{
        altitude =  bmp.readAltitude(initialPressure/100.0f);
      }
      temperature = bmp.temperature;
    }

    gps.read();

    digitalWrite(ALARM_LED, digitalRead(TRG));

    //envoie de la RF
    if(rf_index > rf_trame.length()){
      float accMean = sqrt((worldAccel[0]*worldAccel[0])+(worldAccel[1]*worldAccel[1])+(worldAccel[2]*worldAccel[2]));
      //float agg = mpu.getPitch() > mpu.getRoll() ? :
      rf_trame = "";
      rf_index = 0;
      rf_trame +=  "$TRG:" + gps.getLat() + ";" + gps.getLon() + ";" + String(altitude,2) + ";" + String(temperature,1) + ";" + String(accMean,2) + "\n";
      //Serial.print(rf_trame);
    }else{
      writeChar(rf_trame.charAt(rf_index));
    }
    rf_index ++;
    
  
    if(logSD){ // date;time; millis; Qw;Qx;Qy;Qz; Ax;Ay;Az; Mx;My;Mz; altiBMP; temperature; lat;long
      logBuffer += gps.getDate() + ";" + gps.getTime() + ";";
      logBuffer += String(millis()) + ";";
      logBuffer += String(quaternionScalar,5) + ";" + String(mpuQuaternion[0],5) + ";" + String(mpuQuaternion[1],5) + ";" + String(mpuQuaternion[2],5) + ";";
      logBuffer += String(-mpuAccel[0],5) + ";" + String(mpuAccel[1],5) + ";" + String(mpuAccel[2],5) + ";";
      logBuffer += String(mpuMag[0],5) + ";" + String(mpuMag[1],5) + ";" + String(mpuMag[2],5) + ";";
      logBuffer += String(altitude,5) + ";";
      logBuffer += String(temperature,5) + ";";
      logBuffer += gps.getLat() + ";" + gps.getLon() + "\n"; //GPS
      saveToSD();
    }
    
  }
}

void ringtone(){
  tone(BUZZER_PIN, 659, 104);
  delay(104);
  delay(24);
  tone(BUZZER_PIN, 554, 82);
  delay(82);
  delay(47);
  tone(BUZZER_PIN, 554, 370);
  delay(370);
  tone(BUZZER_PIN, 494, 93);
  delay(93);
  delay(23);
  tone(BUZZER_PIN, 554, 117);
  delay(117);
  tone(BUZZER_PIN, 659, 267);
  delay(267);
}

void errorTone(){
  tone(BUZZER_PIN, 7500, 100);
  delay(100);
  delay(50);
  tone(BUZZER_PIN, 7500, 100);
  delay(100);
  delay(50);
  tone(BUZZER_PIN, 7500, 100);
  delay(100);
  delay(50);
}

void ackTone(){
  tone(BUZZER_PIN, 6000, 100);
  delay(100);
  delay(100);
  tone(BUZZER_PIN, 3000, 100);
  delay(100);
  delay(500);
}

void initPins(){
  pinMode(INT_ALTI, INPUT);
  pinMode(INT_IMU, INPUT);
  pinMode(RF_TX, OUTPUT);
  pinMode(RF_EN, OUTPUT);
  pinMode(TRG, INPUT);
  pinMode(ALARM_LED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(RF_TX, LOW);
  digitalWrite(RF_EN, HIGH);
  digitalWrite(ALARM_LED, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  
}

void initMPU(){
  float accX = 622.29;
  float accY = 8925.95;
  float accZ = -4652.39;
  float gyroX = 267.20;
  float gyroY = -410.56;
  float gyroZ = 1646.90;
  float magbiasX = 44.51;
  float magbiasY = 50.02;
  float magbiasZ = -294.45;
  float magscaleX = 0.99;
  float magscaleY = 1.03;
  float magscaleZ = 0.98;
  
  Wire.begin();
  delay(2000);

  MPU9250Setting setting;
  setting.accel_fs_sel = ACCEL_FS_SEL::A16G;
  setting.gyro_fs_sel = GYRO_FS_SEL::G500DPS;
  setting.mag_output_bits = MAG_OUTPUT_BITS::M16BITS;
  setting.fifo_sample_rate = FIFO_SAMPLE_RATE::SMPL_200HZ;
  setting.gyro_fchoice = 0x03;
  setting.gyro_dlpf_cfg = GYRO_DLPF_CFG::DLPF_41HZ;
  setting.accel_fchoice = 0x01;
  setting.accel_dlpf_cfg = ACCEL_DLPF_CFG::DLPF_45HZ;


  if(!mpu.setup(0x68, setting)) {  // 0x68 : niveau bas ; 0x69 : niveau haut
    fetchError(F("MPU connection failed. Please check your connection with `connection_check` example."));
  }

  mpu.setAccBias(accX, accY, accZ);
  mpu.setGyroBias(gyroX, gyroY, gyroZ);
  mpu.setMagBias(magbiasX, magbiasY, magbiasZ);
  mpu.setMagScale(magscaleX, magscaleY, magscaleZ);
  
}

void cross(float A[3], float B[3], float res[3]){
    res[0] = A[1] * B[2] - A[2] * B[1];
    res[1] = A[2] * B[0] - A[0] * B[2];
    res[2] = A[0] * B[1] - A[1] * B[0];
}

float dot(float A[3], float B[3])
{
    float res = 0;
    for (int i = 0; i < 3; i++)
        res = res + A[i] * B[i];
    return res;
}

void init_SD(){

  if (!SD.begin(4)) {
    fetchError(F("initialization of SD failed!"));
  }

  if(!SD.exists(rootFilename)){
    if(serial){
      Serial.println("No logs folder, creating one..."); 
    }
    
    if(!SD.mkdir(rootFilename)){
      fetchError(F("Cannot create logs folder !"));
    }
  }

  root = SD.open(rootFilename);

  int index = 0;

   while (true) {
    File entry =  root.openNextFile();
    if (! entry) {
      break;
    }
    entry.close();
    index ++;
  }

  root.close();

  if(serial){
    Serial.print("Creating the "); Serial.print(index); Serial.println(" logs file.");
  }
  
  rootFilename += String(index) + ".csv";
  root = SD.open(rootFilename, FILE_WRITE);
  
  if(root){
    root.println("date;time;millis;Qw;Qx;Qy;Qz;Ax;Ay;Az;Mx;My;Mz;altiBMP;temperature;lat;long");
  }else{
    fetchError("Errors while openning file : " + rootFilename);
  }

  logBuffer.reserve(1024);
}


void saveToSD(){
  //writing to SD card non blocking
  unsigned int chunkSize = root.availableForWrite();
  if (chunkSize && logBuffer.length() >= chunkSize) {
    root.write(logBuffer.c_str(), chunkSize);
    // remove written data from buffer
    logBuffer.remove(0, chunkSize);
  }
}


void initBMP(){
  if(!bmp.begin_I2C()){
    fetchError(F("Could not find a valid BMP3 sensor, check wiring!"));
  }

  // Set up oversampling and filter initialization
  bmp.setTemperatureOversampling(BMP3_NO_OVERSAMPLING); //oversamp to x1 comme indique par le construct pour utilisation drone
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_8X); // same ..
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_1);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);


  for(int i = 0; i < 30; i++){
    if(bmp.performReading()){
        initialPressure += bmp.pressure;
    }else{
      if(serial){
        Serial.println(F("BMP failed to perform reading"));
        errorTone();
      }
    }
    delay(100);
  }
  
  if(initialPressure == 0){
    fetchError(F("Failed to initialize pressure"));
  }

  initialPressure = initialPressure/30;
  
}

void fetchError(String str){
  while(1){
    if(serial){
      Serial.println(str);
    }
    errorTone();
    delay(5000); 
  }
}

void writeChar(char carac){
  digitalWrite(RF_TX, HIGH);
  delayMicroseconds(1000000.0/bitrate);
  for(uint8_t i = 0; i < 8; i++){
    digitalWrite(RF_TX, ((carac >> i) & 1) ? LOW: HIGH);
    delayMicroseconds(1000000.0/bitrate);
  }
  digitalWrite(RF_TX, LOW);
  delayMicroseconds(2000000.0/bitrate);
}
