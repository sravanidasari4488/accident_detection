🚨 Smart Accident & Fire Detection System using Raspberry Pi Zero
An intelligent IoT-based safety system that detects accidents and fire, captures live images, estimates the intensity, and sends real-time alerts (with location, photos, and intensity data) to emergency contacts like police, ambulance, and relatives via Telegram.

📌 Features
 Detects fire using flame or smoke sensors
 Detects accidents based on sudden impact (accelerometer)
 Captures photo at the time of incident using Pi Camera
 Fetches GPS location
 Calculates intensity of the accident/fire
 Sends alert messages + photos + location + intensity via Telegram Bot to:
  Nearby police station
  Ambulance service
  Relatives or close friends

Tech Stack
 Hardware:
Raspberry Pi Zero W
Flame Sensor / Smoke sensor
MPU6050 (Accelerometer + Gyroscope)
NEO-6M GPS Module
Raspberry Pi Camera Module
Buzzer, LEDs, GSM Module

 Software:
Python 3
RPi.GPIO, smbus, cv2 (OpenCV), serial, telepot (Telegram API)
Telegram Bot API
Google Maps API (optional for link formatting)

 How It Works
Sensor Monitoring
MPU6050 detects sudden jerks (accidents)
Flame sensor checks for fire or high temperature
Photo Capture & Location Fetching
On detecting incident, Pi Camera captures a real-time image
GPS module gets live coordinates
Telegram Alert
A Telegram bot sends an alert message with:
Live photo
GPS location link
Alerts sent to emergency groups or individual contacts

 Hardware Connections
Component	Pi Zero Pin
MPU6050	SDA → GPIO2, SCL → GPIO3
GPS Module	TX → GPIO15, RX → GPIO14
Flame Sensor	D0 → GPIO17
Camera Module	CSI Camera Port
Buzzer/LED	Any GPIO Pin
