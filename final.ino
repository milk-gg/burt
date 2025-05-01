// For 2025 MATEROV Season

#include <Servo.h>
#include <SPI.h>
Servo myservo;
  
// pins
const int temp = A0;
const int pressure = A1;
const int button = 4;
const int servo = 9;
  
// target depths
const int target_depths_size = 4;
const int target_depths[target_depths_size] = {0, 20, 110, 210};
  
// motor values 
const int motor_stop = 91;
const int max_motor_down = 63;
const int max_motor_up = 101;
const int motor_hover = 79;
const int max_error_range = 60; // used for map() function as the upper boumd

// atmospheric pressure based on pressure in Long Beach from https://barometricpressure.today/cities/long-beach-us
float atmospheric pressure = 101270.0;

//what is the distance from the pressure sensor to the bottom of toobie to calculate what depth it needs to go to???
//todo, add pool depth and get the target depths from that and distance from pressure to bottom of toobie

void setup() 
{
  Serial.begin(9600);

  // set pin
  pinMode(button, INPUT_PULLUP);

  // initializing motor
  delay(1000);
  myservo.attach(servo,1000,2000);
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
  delay(300);

  // goes through every target depth
  for (int i = 0; i < target_depths_size; i++)
  { 
    // if target depth is the air, wait for a button press to log data then skip rest of iteration
    if (i == 0)
    {
      Serial.println("press button again to take air temp");
      while (digitalRead(button) == HIGH) {}
      delay(300);
      log_data(30, get_temperature());
      continue;
    }
    // if for loop is on its second iteration, wait for a button press to confirm MATE Float is in water and log data
    if (i == 1)
    {
      Serial.println("press button once MATE Float is in the water");
      while (digitalRead(button) == HIGH) {}
      delay(300);
      log_data(-20, get_temperature());
      continue;
    }

    if (go_to_depth(target_depths[i]) = 1)
    {
      Serial.println("restarting program");
      break;
    }
    hover(target_depths[i]);  
    log_data(-get_depth(), get_temperature()); 

    // when at end of loop, return to the surface
    if (i == target_depths_size - 1)
    {
      Serial.println("ascending to surface...");
      if (go_to_depth(20) = 1)
      {
        
        break;
      }
      myservo.write(motor_stop);
    }
  }
}

int go_to_depth(int target)
{
  Serial.print("going to depth "); Serial.println(target);

  int speed; 
  int error;

  const int timeout = 20000;
  unsigned const long start_time = millis();

  // while depth is not within 5cm...
  while (abs(get_depth() - target) > 5 && millis() > start_time + timeout)
  {
    long temp_depth = get_depth();
    Serial.print("depth = "); Serial.println(temp_depth);

    error = temp_depth - target;

    // if depth is lower than target go down, based on map()
    if (error < 0)
    {
      speed = map(abs(error), 0, 50, motor_hover, max_motor_down);
      speed = constrain(speed, max_motor_down, motor_hover);
      myservo.write(speed);
    }
    else
    {
      // if depth is higher than target go up based on map()
      speed = map(abs(error), 0, max_error_range, motor_hover, max_motor_up);
      speed = constrain(speed, motor_hover, max_motor_up);
      myservo.write(speed);
    }
    // how often the motor speed is changed
    delay(10);
  }
  if (millis() > start_time + timeout) 
  {
    Serial.print("going to depth "); Serial.print(target); Serial.println(" unsuccessful"); 
    return 1;
  }
  
  //stopping movement once complete
  return 0;
  Serial.print("going to depth "); Serial.print(target); Serial.println(" successful"); 
}

void hover(int temp_target)
{
  Serial.print("hovering at "); Serial.println(temp_target);

  const unsigned long hover_duration = 2000; 
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
        break;
      }
      // motor hover
      myservo.write(80);
    }
    else
    {
      // depth is out of range, reset countdown and correct positioning
      Serial.println("out of range, resetting countdown");
      start_time = millis(); 

      // correcting position
      go_to_depth(temp_target);
    }
    // how often it checks
    delay(10);
  }
}

// gets water depth in cm using formula from https://bluerobotics.com/learn/pressure-depth-calculator/
float get_depth() 
{
  int read = analogRead(pressure); // gets 10 bit voltage
  float v = read * 5.0 / 1023.0; // gets voltage from analog read
  float psi = (v - 0.5) * (30.0 / 4.0); // .5 = 0 PSI, 4.5 = 30 PSI, calculates PSI based on voltage 
  float pascal = psi * 6894.76; // converts psi to pascals
  float gauge_pressure = pascal - atmospheric pressure; // gets guage pressure for blue robotics formula
  float depth_meter = gauge_pressure / (997.0474 * 9.80665) // gets water depth in meters based on blue robotics formula, uses fresh water density for pool water
  return meter * 100; // converts to cm and return
}
  
float get_temperature() 
{
  int adcVal = analogRead(temp);
  float v = adcVal * 5.0 / 1023.0;  
  float Rt = 10.0 * v / (5.0 - v); 
  float tempK = 1.0 / (log(Rt / 10.0) / 3950.0 + 1.0 / 298.15); 
  float tempC = tempK - 273.15;
  return tempC;
}
  
// prints data
void log_data(float temp_depth, float temp_temp)
{
  Serial.print(temp_depth);
  Serial.print(",");
  Serial.println(temp_temp);
}


