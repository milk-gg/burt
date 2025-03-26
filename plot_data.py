import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up serial connection (change 'COM5' to your Arduino's port)
ser = serial.Serial('COM5', 9600)  # Adjust COM port as necessary
time.sleep(2)  # Give Arduino some time to initialize

# Initialize data lists
depth_data = []
temperature_data = []

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 320)  # Depth range (0-320 cm), adjust as needed
ax.set_ylim(0, 50)   # Temperature range (0-50°C), adjust as needed
ax.set_xlabel('Depth (cm)')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Depth vs Temperature')
ax.grid(True)

# Variables for real-time plotting
start_time = time.time()

# Function to update the plot
def update_plot(frame):
    global depth_data, temperature_data, start_time

    # Read data from the Arduino (assuming the format is Depth,Temperature)
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")  # Print the raw data from Arduino
            
            # Process the data (Assuming the Arduino sends depth and temperature in this format)
            try:
                depth, temperature = map(float, line.split(','))  # Split based on comma
                # Store data for graphing
                depth_data.append(depth)
                temperature_data.append(temperature)

                # Limit the number of data points on the graph (optional)
                if len(depth_data) > 100:  # Limit to 100 points
                    depth_data = depth_data[1:]
                    temperature_data = temperature_data[1:]

                # Update the plot with new data
                ax.clear()  # Clear the previous plot to prevent overlap
                ax.set_xlim(0, 210)  # Reset depth range (0-210 cm)
                ax.set_ylim(0, 50)   # Reset temperature range (0-50°C)
                ax.set_xlabel('Depth (cm)')
                ax.set_ylabel('Temperature (°C)')
                ax.set_title('Depth vs Temperature')
                ax.grid(True)

                ax.plot(depth_data, temperature_data, 'bo-', label='Depth vs Temp')
                ax.legend()

            except ValueError:
                print("Error parsing data from Arduino. Expected format: Depth,Temperature")

    except serial.SerialException as e:
        print(f"Error reading from serial port: {e}")

    return []

# Set up the animation to update the plot in real time
ani = animation.FuncAnimation(fig, update_plot, blit=False, interval=1000)

# Show the plot
plt.show()

# Close the serial port when done
ser.close()