#include "MQTT.h"

void callback(char* topic, byte* payload, unsigned int length);

/**
 * if want to use IP address,
 * byte server[] = { XXX,XXX,XXX,XXX };
 * MQTT client(server, 1883, callback);
 * want to use domain name,
 * exp) iot.eclipse.org is Eclipse Open MQTT Broker: https://iot.eclipse.org/getting-started
 * MQTT client("iot.eclipse.org", 1883, callback);
 **/
MQTT client("HostName=Distance.azure-devices.net;DeviceId=MyPi;SharedAccessKey=QZTLCy8s1EA2lP56YRiRptybyjwPoLAfazSwUk09FmY=", 1883, callback);
int led1 = D1;
// byte server[] = { 192, 168, 8, 113};
// MQTT client(server, 1883, callback);


// recieve message
void callback(char* topic, byte* payload, unsigned int length) {
 Particle.variable("distance", (int)payload);
 Spark.variable("distance", (int)payload);
    
    
//   if (!strcmp(p, "RED"))
//         RGB.color(255, 0, 0); 
    // client.publish("outTopic/", "hello");
    
  
    delay(10000);
}


void setup() {
    RGB.control(true);

    // connect to the server
    client.connect("sparkclient");

    // publish/subscribe
    if (client.isConnected()) {
        client.publish("outTopic/message","hello world");
        
        client.subscribe("inTopic/message");
        
    }
}

void loop() {
    if (client.isConnected())
        client.loop();
     
}

