/*
  For MATEROV 2025 Season
*/

#include <Servo.h>
#include <SPI.h>
Servo myservo;
  
// data (truncated raw values and their corresponding depth in cm)
const int data_index = 22;
const long raw_values[data_index] = {8316, 8300, 8703, 8830, 9115, 9335, 9744, 10000, 10370, 10655, 11071, 11430, 11790, 12080, 12327, 12745, 13112, 13358, 13630, 13960, 14255, 14694};
const int depths[data_index] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210};
  
// pins
const int out = 2;
const int sck = 3;
const int button = 4;
  
//target depths
const int target_depths_size = 4;
const int target_depths[target_depths_size] = {0, 20, 110, 210};
  
void setup() 
{
  Serial.begin(9600);

  // set pins
  pinMode(out, INPUT);
  pinMode(sck, OUTPUT);
  pinMode(button, INPUT_PULLUP);

  //initializing motor
  delay(1000);
  myservo.attach(9,1000,2000);
  Serial.println("Initializing ESC");
  myservo.write(180);
  delay(5000);
  myservo.write(91);
  delay(1000);
  Serial.println("ESC Initialized");
  delay(3000);
}
  
void loop() 
{ 
  // waiting for button to be pressed to begin
  Serial.println("press button to start");
  while (digitalRead(button) == HIGH) {}

  // goes through every target depth
  for (int i = 0; i < target_depths_size; i++)
  { 
    // if target depth is the air, wait for a button press to log data then skip rest of iteration
    if (i == 0)
    {
      Serial.println("press button again to take air temp");
      while (digitalRead(button) == HIGH) {}
      log_data(30, get_temperature());
      continue;
    }
    // if for loop is on its second iteration, wait for a button press to confirm MATE Float is in water and take temp
    if (i == 1)
    {
      Serial.println("press button once MATE Float is in the water");
      while (digitalRead(button) == HIGH) {}
      log_data(-20, get_temperature());
      continue;
    }
    go_to_depth(target_depths[i]);  
    hover(target_depths[i]);  
    log_data(-get_depth(), get_temperature()); 

    if (i == target_depths_size - 1)
    {
      go_to_depth(5);
      Serial.println("succesfull");
    }
  }
}

void go_to_depth(int target)
{
  Serial.print("Going to depth "); Serial.println(target);

  // while pressure is not within 5cm...
  while (abs(get_depth() - target) > 5)
  {
    long temp_depth = get_depth();
    Serial.print("depth = "); Serial.println(temp_depth);

    if (temp_depth < target)
    {
      // set motor to go down
      Serial.println("going down...")
      myservo.write(75); 
    }
    else
    {
      // going up...
      Serial.println("going up...");
      myservo.write(106);
    }
    // making sure to not bombard motor and serial print
    delay(1000);
  }
  //stopping movement once complete
  Serial.print("going to depth "); Serial.print(target); Serial.println(" successful"); 
  myservo.write(91); 
}

void hover(int temp_target)
{
  Serial.print("hovering at "); Serial.println(temp_target);

  const unsigned long hover_duration = 10000; 
  unsigned long start_time = millis();

  while (true)
  {
    long temp_depth = get_depth();
    Serial.print("depth = "); Serial.println(temp_depth);

    // if depth is within 5 cm error, check if countdown should continue
    if (abs(temp_depth - temp_target) <= 5)
    {
      // stop motor and break when countdown finished
      if (millis() - start_time >= hover_duration)
      {
        Serial.println("hover complete");
        myservo.write(91); 
        break;
      }
      // stop motor if in range
      myservo.write(91);
    }
    else
    {
      // depth is out of range, reset countdown and correct positioning
      Serial.println("out of range, resetting countdown");
      start_time = millis(); 

      // correcting position
      go_to_depth(temp_target);
    }
    // to not bombard motor and serial print
    delay(1000);
  }
}

// get raw value from pressure sensor, from https://swharden.com/blog/2022-11-14-hx710b-arduino/
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
    digitalWrite(out, HIGH);
    digitalWrite(sck, LOW);
  }
  
  // return pressure
  return result;
}
  
// interpolate depth based on data set
long interpolate_depth(long raw_value) 
{
  long rounded_value = round(raw_value / 1000.0);
  
  // if below dataset, return lowest depth from set
  if (rounded_value <= raw_values[0]) return depths[0];  
  
  // if above dataset, extrapolate using the slope of the last two data
  if (rounded_value >= raw_values[data_index - 1]) 
  {      
    long slope = (long)(depths[data_index - 1] - depths[data_index - 2]) / (raw_values[data_index - 1] - raw_values[data_index - 2]);
    return depths[data_index - 1] + slope * (rounded_value - raw_values[data_index - 1]);
  }
  
  // find the correct range for interpolation
  for (int i = 0; i < data_index - 1; i++) 
  {
    if (rounded_value >= raw_values[i] && rounded_value <= raw_values[i + 1]) 
    {
      long slope = (long) (depths[i + 1] - depths[i]) / (raw_values[i + 1] - raw_values[i]);
      return depths[i] + slope * (rounded_value - raw_values[i]);
    }
  }
  return 0;
}

// getting depth via read_sensor() and interpolate_depth() functions
long get_depth() 
{
  long raw_data = read_sensor();
  long rounded_data = round(raw_data / 1000.0); 
  long temp_depth = interpolate_depth(raw_data); 
  return temp_depth;
} 
  
float get_temperature() {
  int adcVal = analogRead(A0);
  float v = adcVal * 5.0 / 1024.0;  
  float Rt = 10.0 * v / (5.0 - v); 
  float tempK = 1.0 / (log(Rt / 10.0) / 3950.0 + 1.0 / 298.15); 
  float tempC = tempK - 273.15;
  return tempC;
}
  
// prints data
void log_data(long temp_depth, long temp_temp)
{
  Serial.print("depth (cm):");
  Serial.print(temp_depth);
  Serial.print(',');
  Serial.print("temp:");
  Serial.println(temp_temp);
} 
