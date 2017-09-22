#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

ESP8266WiFiMulti WiFiMulti;

const char* ssid = "Tardis";
const char* password = "geronimo";
bool state = true;

MPU6050 accelgyro(0x68);

int16_t ax, ay, az;
int16_t gx, gy, gz;

//#define OUTPUT_READABLE_ACCELGYRO // Slower, don't use this
#define OUTPUT_BINARY_ACCELGYRO

int b = 100; // Number of datapoints to read before sending. Change size of array on next line accordingly
int16_t data[100*7];
char str[64];

void setup() {
    // join I2C bus
    Wire.begin(5,4);

    // initialize serial communication for debugging purposes
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.print(accelgyro.testConnection() ? "1. MPU6050 connection successful" : "1. MPU6050 connection failed");
    
    while(accelgyro.testConnection() == false) { // If MPU is not connected, wait for it
        delay(100);
        Serial.print(".");
    }

    accelgyro.setFullScaleAccelRange(MPU6050_ACCEL_FS_16); // Set acc scale to max (16G)
    accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_2000); // Set gyro scale to max (2000 degrees per sec)
    
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
            accelgyro.getMotion6(&data[index++], &data[index++], &data[index++], &data[index++], &data[index++], &data[index++]);
        }
        // If client doesn't respond to data, stop sending since the connection broke
        if(client.write((uint8_t*)data, sizeof(int16_t)*b*7) == 0)
            break;
    }
}