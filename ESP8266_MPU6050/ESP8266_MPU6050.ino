#include <I2Cdev.h>
// #include "MPU6050.h"
#include <Wire.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#define MPU_ADDR 0x68

ESP8266WiFiMulti WiFiMulti;

const char* ssid = "Tardis";
const char* password = "geronimo";
bool state = true;

int b = 100; // Number of datapoints to read before sending. Change size of array on next line accordingly
int16_t data[100*7];
char str[64];

void setup_mpu6050() {
  Wire.begin(5,4);
  mpu6050_setRegister(0x6b, 0);
  mpu6050_setRegister(0x1b, 0b11000);
  mpu6050_setRegister(0x1c, 0b11000);
}

void mpu6050_setRegister(uint8_t addr, uint8_t val) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(addr);  // PWR_MGMT_1 register
  Wire.write(val);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);  
}

void mpu6050_get_data(
  int16_t* ax, int16_t* ay, int16_t* az, 
  int16_t* rx, int16_t* ry, int16_t* rz) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom((uint8_t)MPU_ADDR,(size_t)14,true);  // request a total of 14 registers
  *ax=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  *ay=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  *az=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Wire.read(); Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  *rx=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  *ry=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  *rz=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

void setup() {
    // join I2C bus
    setup_mpu6050();

    // initialize serial communication for debugging purposes
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    
    // Connect to wifi network
    WiFiMulti.addAP(ssid, password);
    Serial.print("\nConnecting to wifi");
    
    // Wait for connection
    while(WiFiMulti.run() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    
    Serial.print("\n");

    // Print the IP address
    Serial.println(WiFi.localIP());
}

void loop() {

    // Define target to send data to
    const uint16_t port = 8085;
    const char * host = "192.168.43.155";

    Serial.print("connecting to ");
    Serial.println(host);

    // Use WiFiClient class to create TCP connections to target
    WiFiClient client;

    // Wait for connection
    if (!client.connect(host, port)) {
        Serial.println("connection failed");
        Serial.println("wait 1 sec...");
        delay(1000);
        return;
    }

    int16_t index;
    int mil;
    int lastMillis = millis();
    while(1) { // run forever
        index = 0;
        // Gather b datapoints
        for(int i = 0; i < b; i++){  
            mil = millis();
            data[index++] = mil -lastMillis;
            lastMillis = mil;
            mpu6050_get_data(&data[index++], &data[index++], &data[index++], &data[index++], &data[index++], &data[index++]);
            // accelgyro.getMotion6(&data[index++], &data[index++], &data[index++], &data[index++], &data[index++], &data[index++]);
        }
        // If client doesn't respond to data, stop sending since the connection broke
        if(client.write((uint8_t*)data, sizeof(int16_t)*b*7) == 0)
            break;
    }
}
