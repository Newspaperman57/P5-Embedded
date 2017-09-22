// I2C device class (I2Cdev) demonstration Arduino sketch for MPU6050 class
// 10/7/2011 by Jeff Rowberg <jeff@rowberg.net>
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib
//
// Changelog:
//      2013-05-08 - added multiple output formats
//                 - added seamless Fastwire support
//      2011-10-07 - initial release

/* ============================================
I2Cdev device library code is placed under the MIT license
Copyright (c) 2011 Jeff Rowberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
*/

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"
#include "MPU6050.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti WiFiMulti;

const char* ssid = "Tardis";
const char* password = "geronimo";

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);
// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro1(0x68);
MPU6050 accelgyro2(0x69);
//MPU6050 accelgyro(0x69); // <-- use for AD0 high

int16_t ax, ay, az;
int16_t gx, gy, gz;



// uncomment "OUTPUT_READABLE_ACCELGYRO" if you want to see a tab-separated
// list of the accel X/Y/Z and then gyro X/Y/Z values in decimal. Easy to read,
// not so easy to parse, and slow(er) over UART.
#define OUTPUT_READABLE_ACCELGYRO

// uncomment "OUTPUT_BINARY_ACCELGYRO" to send all 6 axes of data as 16-bit
// binary, one right after the other. This is very fast (as fast as possible
// without compression or data loss), and easy to parse, but impossible to read
// for a human.
//#define OUTPUT_BINARY_ACCELGYRO


#define LED_PIN 13
bool blinkState = false;

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin(5,4);
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro1.initialize();
    accelgyro2.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro1.testConnection() ? "1. MPU6050 connection successful" : "1. MPU6050 connection failed");
    if(accelgyro1.testConnection() == false)
      while(true) {delay(1000);}
    accelgyro1.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
    accelgyro1.setFullScaleGyroRange(MPU6050_GYRO_FS_2000);

    Serial.println(accelgyro2.testConnection() ? "2. MPU6050 connection successful" : "2. MPU6050 connection failed");
    if(accelgyro2.testConnection() == false)
      while(true) {delay(1000);}
    accelgyro2.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
    accelgyro2.setFullScaleGyroRange(MPU6050_GYRO_FS_2000);
    
    // We start by connecting to a WiFi network
    WiFiMulti.addAP(ssid, password);
    Serial.print("\nConnecting to wifi");
    while(WiFiMulti.run() != WL_CONNECTED) {
      Serial.print(".");
      delay(500);
    }
    Serial.print("\n");

    // use the code below to change accel/gyro offset values
    /*
    Serial.println("Updating internal sensor offsets...");
    // -76	-2359	1688	0	0	0
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    accelgyro.setXGyroOffset(220);
    accelgyro.setYGyroOffset(76);
    accelgyro.setZGyroOffset(-85);
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    */
    pinMode(0, OUTPUT);
    
    // Print the IP address
    Serial.println(WiFi.localIP());
}

void loop() {
    // read raw accel/gyro measurements from device
    char str[64];
    
    const uint16_t port = 8085;
    const char * host = "192.168.43.155"; // ip or dns

    Serial.print("connecting to ");
    Serial.println(host);
    
    // Use WiFiClient class to create TCP connections
    WiFiClient client;

    if (!client.connect(host, port)) {
        Serial.println("connection failed");
        Serial.println("wait 1 sec...");
        delay(1000);
        return;
    }
  
    int tax1 = 0;
    int tay1 = 0;
    int taz1 = 0;
    int tgx1 = 0;
    int tgy1 = 0;
    int tgz1 = 0;
    int tax2 = 0;
    int tay2 = 0;
    int taz2 = 0;
    int tgx2 = 0;
    int tgy2 = 0;
    int tgz2 = 0;
    while(1) {
      tax1 = 0;
      tay1 = 0;
      taz1 = 0;
      tgx1 = 0;
      tgy1 = 0;
      tgz1 = 0;
      tax2 = 0;
      tay2 = 0;
      taz2 = 0;
      tgx2 = 0;
      tgy2 = 0;
      tgz2 = 0;
      for(int i = 0; i < 8; i++){
        accelgyro1.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        tax1 += ax;
        tay1 += ay;
        taz1 += az;
        tgx1 += gx;
        tgy1 += gy;
        tgz1 += gz;
        accelgyro2.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        tax2 += ax;
        tay2 += ay;
        taz2 += az;
        tgx2 += gx;
        tgy2 += gy;
        tgz2 += gz;
      }
      int milli = millis();
      sprintf(str, "1\t%08d\t%06d\t%06d\t%06d\t%06d\t%06d\t%06d\n",milli, tax1/8, tay1/8, taz1/8, tgx1/8, tgy1/8, tgz1/8);
      client.print(str);      
      sprintf(str, "2\t%08d\t%06d\t%06d\t%06d\t%06d\t%06d\t%06d\n",milli, tax2/8, tay2/8, taz2/8, tgx2/8, tgy2/8, tgz2/8);
      client.print(str);
    }
}
