#!/usr/bin/python
import time
import serial
import MySQLdb
import datetime



#establish connection to MySQL. You'll have to change this for your database.
dbConn = MySQLdb.connect("localhost","root","lineslines12","Arduino") or die ("could not connect to database")
#open a cursor to the database
cursor = dbConn.cursor()

device = '/dev/ttyACM0' #this will have to be changed to the serial port you are using
try:
 # print "Trying...",device 
  ser = serial.Serial(device, 9600)
except:
  print "Failed to connect on",device

try:
  time.sleep(10)
  ser.write(b'1')
  ser.write(b'4')
  ser.flushInput()
  data = ser.readline()[:-2]
# data = arduino.readline()  #read the data from the arduino
  print "",data
  pieces = data.split("\t")  #split the data by the tab
  print "A guardar ", int(float(pieces[0])), int(float(pieces[1]))
#Here we are going to insert the data into the Database
  try:
    cursor.execute("INSERT INTO log (id,temp,hm) VALUES (%s,%s,%s)", (" ",int(float(pieces[0])),int(float(pieces[1]))))
    print"A guardar 2"
    dbConn.commit() #commit the insert
    cursor.close()  #close the cursor
  except MySQLdb.IntegrityError:
    print "failed to insert data"
  finally:
    cursor.close()  #close just incase it failed
except:
  print "Failed to get data from Arduino!"
