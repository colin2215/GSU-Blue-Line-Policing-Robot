# GSU-Blue-Line-Policing-Robot
Raspberry Pi-Based Data Acquisition System for Tensiometry
This project implements a high-performance data acquisition system using a Raspberry Pi, MCC172 DAQ HATs, and a mechanical tapper. It is designed to measure wave speeds using an accelerometer, synchronize GPIO signals, and save data for analysis.

Features
Data Collection: Collects and logs high-frequency accelerometer data using MCC172 DAQ HATs.
PWM Signal Generation: Outputs precision PWM signals to control a mechanical tapper for wave generation.
Bell Curve Waveform: Optionally generates smooth bell-shaped pulses for precise measurements.
Data Logging: Saves calibration data, GPS location, and accelerometer measurements to SD cards or USB drives.
GPIO Synchronization: Monitors and responds to external triggers, managing DAQ and PWM events.
Hardware Requirements
Raspberry Pi (tested on Raspberry Pi 4)
MCC172 DAQ HAT (1 or 2 units, depending on configuration)
Arduino (for auxiliary operations)
RTC Module (e.g., DS3231 for accurate timekeeping)
Mechanical Tapper
Accelerometer
USB Drive (for data storage)
Software Requirements
Ensure you have the following libraries installed on your Raspberry Pi:

Python 3.x
pigpio
numpy
matplotlib
adafruit-mcp4725
serial
Install missing packages using:

pip install numpy matplotlib adafruit-circuitpython-mcp4725 pyserial
Setup Instructions
Hardware Configuration:

Connect MCC172 DAQ HATs to the Raspberry Pi.
Wire the mechanical tapper and accelerometer to the GPIO pins.
Connect the RTC module to I2C pins (default: GPIO 2 and GPIO 3).
Ensure the GPS module is connected to a serial port (default: /dev/ttyACM0).
Enable GPIO and I2C:

Enable I2C via raspi-config.
sudo raspi-config
Run the Code:

Ensure daqfuncjosh.py and runmejosh.py are in the same directory.
Start the script:
python3 runmejosh.py
Project Workflow
Initialization:

Configures GPIO pins and DAQ HATs.
Connects to GPS and calibration devices.
Trigger Monitoring:

Waits for an external trigger to start data collection.
Data Collection:

Reads accelerometer data from the DAQ HATs.
Saves calibration and GPS data to files.
Signal Generation:

Generates PWM or bell-shaped pulses to control the mechanical tapper.
Data Saving:

Logs all collected data to SD cards or USB drives.
Outputs
Tensio Data: Binary files containing accelerometer readings.
Calibration Data: Text files with calibration device logs.
GPS Data: Text files with GGA (GPS) messages.
Timing Data: CSV files with precise timestamps for triggers.
Acknowledgments
Special thanks to the MCC DAQ team and Raspberry Pi community for their resources and support in making this project possible.
