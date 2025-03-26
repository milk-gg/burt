#include <Arduino.h>
#include "OneWire.h"
#include "DallasTemperature.h"

// data (truncated raw values depth in cm)
const int data_index = 22;
const long raw_values[data_index] = {8316, 8300, 8703, 8830, 9115, 9335, 9744, 10000, 10370, 10655, 11071, 11430, 11790, 12080, 12327, 12745, 13112, 13358, 13630, 13960, 14255, 14694};
const int depths[data_index] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210};

// pins
const int HX710_OUT = 2;
const int HX710_SCK = 3;
#define ONE_WIRE_BUS 4

// Create a new instance of the oneWire class to communicate with any OneWire device:
OneWire oneWire(ONE_WIRE_BUS);

// Pass the oneWire reference to DallasTemperature library:
DallasTemperature sensors(&oneWire);

const int target_depths_size = 3;
const int target_depths[target_depths_size] = {0, 30, 220};
bool logged[target_depths_size] = {false, false, false}; 

unsigned long prev_time = 0;
const unsigned long interval = 5000; 

void setup() 
{
  pinMode(HX710_OUT, INPUT);
  pinMode(HX710_SCK, OUTPUT);

  // Start up the library:
  sensors.begin();

  Serial.begin(9600);
}

long read_sensor() 
{
  // wait for the current reading to finish
  while (digitalRead(2)) {}

  // read 24 bits
  long result = 0;
  for (int i = 0; i < 24; i++) {
    digitalWrite(3, HIGH);
    digitalWrite(3, LOW);
    result = result << 1;
    if (digitalRead(2)) {
      result++;
    }
  }
  // get the 2s compliment
  result = result ^ 0x800000; 

  // pulse the clock line 3 times to start the next pressure reading
  for (char i = 0; i < 3; i++) 
  { 
    digitalWrite(HX710_SCK, HIGH);
    digitalWrite(HX710_SCK, LOW);
  }

  // return pressure
  return result;
}

float temp()
{
  // Send the command for all devices on the bus to perform a temperature conversion:
  sensors.requestTemperatures();

  // Fetch the temperature in degrees Celsius for device index:
  float temp_temp = sensors.getTempCByIndex(0); // the index 0 refers to the first device

  if (temp_temp == -127.00) 
  {
    Serial.println("Error: Temperature read failed!");
    return -1.0;
  }
  return temp_temp;
}

// round the raw value 
float interpolate_depth(long raw_value) 
{
  long rounded_value = round(raw_value / 1000.0);

  // if below the dataset, return the lowest depth from set
  if (rounded_value <= raw_values[0]) return depths[0];  

  // if above the dataset, extrapolate using the slope of the last two data
  if (rounded_value >= raw_values[data_index - 1]) 
  {      
    float slope = (float)(depths[data_index - 1] - depths[data_index - 2]) / (raw_values[data_index - 1] - raw_values[data_index - 2]);
    return depths[data_index - 1] + slope * (rounded_value - raw_values[data_index - 1]);
  }

  // find the correct range for interpolation
  for (int i = 0; i < data_index - 1; i++) 
  {
    if (rounded_value >= raw_values[i] && rounded_value <= raw_values[i + 1]) 
    {
      float slope = (float) (depths[i + 1] - depths[i]) / (raw_values[i + 1] - raw_values[i]);
      return depths[i] + slope * (rounded_value - raw_values[i]);
    }
  }
  return -1;
}

void log_data(float temp_depth, float temp_temperature)
{
  Serial.print(temp_depth);
  Serial.print(", ");
  Serial.println(temp_temperature);
} 

void loop() 
{ 
  long raw_data = read_sensor();
  float temperature = temp();
  float depth = interpolate_depth(raw_data); 
  unsigned long currentMillis = millis();

  if (temperature != -1.0)
  {
    for (int i = 0; i < target_depths_size; i++) 
    {
      if (abs(depth - target_depths[i]) <= 5 && !logged[i]) 
      {
        if (currentMillis - prev_time >= interval) 
        {
          log_data(depth, temperature);
          logged[i] = true; 
          prev_time = currentMillis;
        }
      }
    }
  } 
}