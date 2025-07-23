
import os
import sys
import RPi.GPIO as  GPIO
from time import sleep
import time
import urllib.request		
from time import sleep          
import serial               
import webbrowser
import cv2
import smbus
import telepot
bus = smbus.SMBus(1)
bus.write_byte_data(0x53, 0x2C, 0x0B)
value = bus.read_byte_data(0x53, 0x31)
value &= ~0x0F;
value |= 0x0B;  
value |= 0x08;
bus.write_byte_data(0x53, 0x31, value)
bus.write_byte_data(0x53, 0x2D, 0x08)
def getAxes():
    bytes = bus.read_i2c_block_data(0x53, 0x32, 6)
        
    x = bytes[0] | (bytes[1] << 8)
    if(x & (1 << 16 - 1)):
        x = x - (1<<16)

    y = bytes[2] | (bytes[3] << 8)
    if(y & (1 << 16 - 1)):
        y = y - (1<<16)

    z = bytes[4] | (bytes[5] << 8)
    if(z & (1 << 16 - 1)):
        z = z - (1<<16)

    x = x * 0.004 
    y = y * 0.004
    z = z * 0.004

    x = x * 9.80665
    y = y * 9.80665
    z = z * 9.80665

    x = round(x, 2)
    y = round(y, 2)
    z = round(z, 2)

 
    return x,y,z
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def handle(msg):
  global telegramText
  global chat_id
  global receiveTelegramMessage
  
  chat_id = msg['chat']['id']
  telegramText = msg['text']
  
  print("Message received from " + str(chat_id))
  
  if telegramText == "/start":
    bot.sendMessage(chat_id, "Welcome")
  else:
    
    receiveTelegramMessage = True

def capture():
    
    print("Sending photo to " + str(chat_id))
    bot.sendPhoto(chat_id, photo = open('./image.jpg', 'rb'))





prv=0
def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    #print("NMEA Time: ", nmea_time,'\n')
    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    try:
        lat = float(nmea_latitude)                  #convert string into float for calculation
        longi = float(nmea_longitude)               #convertr string into float for calculation
    except:
        lat=0
        longi=0
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position




gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0",timeout=1)              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

mot=22
fr=17
buz=27
sw=4
GPIO.setup(fr, GPIO.IN)
GPIO.setup(sw, GPIO.IN)
GPIO.setup(buz,GPIO.OUT)
GPIO.output(buz,False)
GPIO.setup(mot,GPIO.OUT)
GPIO.output(mot,True)
time.sleep(2)
kk=0

bot = telepot.Bot('6811918079:AAEtt7_ZELihZZxEqU_zceN9BCe2-PWHg9E')
chat_id='6290203312'
bot.message_loop(handle)

print("Telegram bot is ready")

bot.sendMessage(chat_id, 'BOT STARTED')
time.sleep(2)


try:
        while(True):
 
            x,y,z=getAxes()
            impact=1-GPIO.input(sw)
            fval=1-GPIO.input(fr)
            
            
            
            print("X:" + str(x))
            print("Y:" + str(y))
            print("IMPACT:" + str(impact))
            print("Y:" + str(fval))
            
            
            received_data = (str)(ser.readline())                   #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
            if(kk==0):
                lat_in_degrees=0
                lat_in_degrees=0
                map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map

            if (GPGGA_data_available>0):
                kk=1
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                GPS_Info()                                          #get time, latitude, longitude
                map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
            
            map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
            print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
            print()


            if(x>5 or x<-5 or y>5 or y<-5):
                print('Fall Accident deteccted')
                sss=1                
                GPIO.output(mot,False)
                GPIO.output(buz,True)
                bot.sendMessage(chat_id, 'Fall Accident deteccted at '+ map_link)
                time.sleep(5)
                GPIO.output(buz,False)
                
            if(fval==1):
                print('Fire Accident deteccted')
                                
                GPIO.output(mot,False)
                GPIO.output(buz,True)
                bot.sendMessage(chat_id, 'Fire Accident deteccted at '+ map_link)
                time.sleep(5)
                GPIO.output(buz,False)
            if(impact==1):
                print('Impact Accident deteccted')
                                
                GPIO.output(mot,False)
                GPIO.output(buz,True)
                bot.sendMessage(chat_id, 'Impact Accident deteccted at '+ map_link)
                time.sleep(5)
                GPIO.output(buz,False)


except KeyboardInterrupt:
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)

