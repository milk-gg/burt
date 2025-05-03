#include <Servo.h>
#include <SPI.h>
Servo myservo;
const int numPoints = 22;
const long rawValues[numPoints] = {8316, 8300, 8703, 8830, 9115, 9335, 9744, 10000, 10370, 10655, 11071, 11430, 11790, 12080, 12327, 12745, 13112, 13358, 13630, 13960, 14255, 14694};
const int depths[numPoints] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210};
const int buttonPin = 4;
long pres;
long temp;
long depth;
float airTemp;
float surfTemp;
float midTemp;
float deepTemp;
float tempC;
unsigned long startTime;
unsigned long currentTime;
void setup() {
  pinMode(2, INPUT);   // Connect HX710 OUT to Arduino pin 2
  pinMode(3, OUTPUT);  // Connect HX710 SCK to Arduino pin 3
  pinMode(4, INPUT_PULLUP);
  delay(10000);
  Serial.begin(9600);
  myservo.attach(9,1000,2000);
  Serial.println("Initializing ESC");
  myservo.write(180);
  delay(5000);
  myservo.write(91);
  delay(1000);
  Serial.println("ESC Initialized");
  delay(3000);
  startTime = millis();
  
}

void loop() {
 Serial.println("Press START button");
 while (digitalRead(buttonPin) == HIGH) { // Wait until the button is pressed (LOW state)
    // Do nothing
  }
 
 outside_air_temp(); 
 Serial.println(" ");

 place_in_water();
 Serial.println(" ");
 
 middle(); 
 Serial.println(" ");
Serial.print("Temperature at -110cm = ");
    temperature();
    midTemp = tempC;

 bottom();
 Serial.println(" ");  
 Serial.println(" ");
Serial.print("Temperature at -210cm = ");
    temperature();
    deepTemp = tempC;
     ascend();
 Serial.println(" ");      
 
 endloop();
}
 

void outside_air_temp() {
 Serial.print("Outside Air Temperature = ");
 temperature();
 pressure();
 Serial.println(" ");
 airTemp = tempC;

 //Good place to automatically calibrate pressure sensor ambient pressure value?????
 

 Serial.println("5 Second Countdown to Place into Pool");
 Serial.print("5 ");
 delay(1000);
 Serial.print("4 ");
 delay(1000);
//  Serial.print("18 ");
 delay(1000);
 Serial.print("3 ");
 delay(1000);
//  Serial.print("2 ");
 delay(1000);
 Serial.print("1 ");
 delay(1000);
//  Serial.print("14 ");
//  //delay(1000);
//  Serial.print("13 ");
//  //delay(1000);
//  Serial.print("12 ");
//  //delay(1000);
//  Serial.print("11 ");
//  //delay(1000);
//  Serial.print("10 ");
//  //delay(1000);
//  Serial.print("9 ");
//  //delay(1000);
//  Serial.print("8 ");
//  //delay(1000);
//  Serial.print("7 ");
//  //delay(1000);
//  Serial.print("6 ");
//  //delay(1000);
//  Serial.print("5 ");
//  //delay(1000);
//  Serial.print("4 ");
//  //delay(1000);
//  Serial.print("3 ");
//  //delay(1000);
//  Serial.print("2 ");
//  //delay(1000);
//  Serial.print("1 ");
//  //delay(1000);
//  Serial.print("0 ");
//  Serial.println(" ");
  
}

void place_in_water(){
// Serial.println("Taking Surface Water Temperature - 2 Second Adjustment Countdown");
//  Serial.print("20 ");
//  delay(1000);
//  Serial.print("19 ");
//  delay(1000);
//  Serial.print("18 ");
//  //delay(1000);
//  Serial.print("17 ");
//  //delay(1000);
//  Serial.print("16 ");
//  //delay(1000);
//  Serial.print("15 ");
//  //delay(1000);
//  Serial.print("14 ");
//  //delay(1000);
//  Serial.print("13 ");
//  //delay(1000);
//  Serial.print("12 ");
//  //delay(1000);
//  Serial.print("11 ");
//  //delay(1000);
//  Serial.print("10 ");
//  //delay(1000);
//  Serial.print("9 ");
//  //delay(1000);
//  Serial.print("8 ");
//  //delay(1000);
//  Serial.print("7 ");
//  //delay(1000);
//  Serial.print("6 ");
//  //delay(1000);
//  Serial.print("5 ");
//  //delay(1000);
//  Serial.print("4 ");
//  //delay(1000);
//  Serial.print("3 ");
//  //delay(1000);
//  Serial.print("2 ");
//  //delay(1000);
//  Serial.print("1 ");
//  //delay(1000);
//  Serial.print("0 ");
//  Serial.println(" ");
//  Serial.print("-20cm Depth Temperature = ");
 temperature();
 surfTemp = tempC;
 pressure();
 //delay (1000);
  
}
    

void middle(){
  Serial.println("Decending to -110cm");
    startTime = millis();
    while(millis() - startTime < 20000){
    pressure();
    if(pres <= 110.00){
      myservo.write(68);
    }
    else if (pres >= 120.00){
      myservo.write(79);
    }
    }
}

void bottom(){
  Serial.println("Decending to -210cm");
    startTime = millis();
    while(millis() - startTime < 10000){
    pressure();
    if(pres <= 210.00){
      myservo.write(68);
    }
    else if (pres >= 220.00){
      myservo.write(79); 
    }
    }
}

void ascend(){
 Serial.println("Ascending to Surface");
 Serial.println(" ");
    while(pres > 40){
    myservo.write(100);
    pressure();
// Serial.println(" ");
Serial.println("At the Surface");
// Serial.println("Thank You, Have a Nice Day.");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
// Serial.println(" ");
}
}

void endloop(){
  myservo.write(91);              
log_data(0, airTemp);
  log_data(20, surfTemp);
  log_data(110, midTemp);
  log_data(210.00, deepTemp);

  Serial.println("                           Benton Underwater Robotics");
  Serial.println(" ");
  Serial.print("     Outside Air Temperature = ");
  Serial.println(airTemp);
  Serial.println(" ");
  Serial.print("     20cm Water Temperature = ");
  Serial.println(surfTemp);
  Serial.println(" ");
  Serial.print("     110cm Water Temperature = ");
  Serial.println(midTemp);
  Serial.println(" ");
  Serial.print("     210cm Water Temperature = ");
  Serial.println(deepTemp);
}

void log_data(float temp_depth, float temp_temp)
{
  Serial.print(temp_depth);
  Serial.print(",");
  Serial.println(temp_temp);
}

void temperature() {
  myservo.write(91);
  delay(30);
  int adcVal = analogRead(A0);
  // Calculate voltage
  float v = adcVal * 5.0 / 1024;
  // Calculate resistance value of thermistor
  float Rt = 10 * v / (5 - v);
  // Calculate temperature (Kelvin)
  float tempK = 1 / (log(Rt / 10) / 3950 + 1 / (273.15 + 25));
  // Calculate temperature (Celsius)
  tempC = tempK - 273.15;
  Serial.println(tempC);

  
}


long readSensor() {
  while (digitalRead(2)) {} // Wait for data ready

  long result = 0;
  for (int i = 0; i < 24; i++) {
    digitalWrite(3, HIGH);
    digitalWrite(3, LOW);
    result = result << 1;
    if (digitalRead(2)) {
      result++;
    }
  }
  result = result ^ 0x800000; // Convert from two's complement

  for (char i = 0; i < 3; i++) { // Start next measurement
    digitalWrite(3, HIGH);
    digitalWrite(3, LOW);
  }

  return result;
}

// Round the raw value instead of truncating and interpolate depth
float interpolateDepth(long rawValue) {
  long roundedValue = round(rawValue / 1000.0); // Round instead of truncating

  // Debugging: Print rounded value
  //Serial.print("Rounded Value: ");
  //Serial.println(roundedValue);

  if (roundedValue <= rawValues[0]) return depths[0];  // Below range → Return min depth
  if (roundedValue >= rawValues[numPoints - 1]) {      // Above range → Estimate based on last trend
    float slope = (float)(depths[numPoints - 1] - depths[numPoints - 2]) / (rawValues[numPoints - 1] - rawValues[numPoints - 2]);
    return depths[numPoints - 1] + slope * (roundedValue - rawValues[numPoints - 1]);
  }

  // Find the correct range for interpolation
  for (int i = 0; i < numPoints - 1; i++) {
    if (roundedValue >= rawValues[i] && roundedValue <= rawValues[i + 1]) {
      float slope = (float)(depths[i + 1] - depths[i]) / (rawValues[i + 1] - rawValues[i]);
      
      // Debugging: Print interpolation range
     // Serial.print("Interpolating between: ");
      //Serial.print("Raw("); Serial.print(rawValues[i]); Serial.print(") Depth("); Serial.print(depths[i]); Serial.print(") ");
      //Serial.print("and Raw("); Serial.print(rawValues[i + 1]); Serial.print(") Depth("); Serial.print(depths[i + 1]); Serial.println(")");

      return depths[i] + slope * (roundedValue - rawValues[i]);
    }
  }
  return -1; // Error: Should never reach here
}

void pressure() {
 
long rawData = readSensor();
  long roundedData = round(rawData / 1000.0); // Round instead of truncating
  float depth = interpolateDepth(rawData); // Pass original rawData for correct interpolation
  
  //Serial.print("Raw Value: ");
  //Serial.print(rawData);
 // Serial.print(" | Rounded Value: ");
 // Serial.print(roundedData);
  //Serial.print("Depth = -");
  //Serial.print(depth);
  //Serial.println("cm");
  pres = depth;
  //Serial.println(pres);
  
  delay(100);
   
   
} 




void test(){
  Serial.println("Clockwise");
    myservo.write(85);              
    delay(4000);
    
    Serial.println("STOP");
    myservo.write(91);              
    delay(4000);
    
    Serial.println("Counter Clockwise");
    myservo.write(100);              
    delay(4000);
    

    Serial.println("STOP");
    myservo.write(91);              
    delay(4000);
}