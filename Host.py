import serial #library to handle the serial port
import io #we will use this to specify a readline() char other than \n (newline)
import tkinter #standard python GUI library
from Tkinter import *

ser = serial.Serial('/dev/ttyACM0', 38400) #setup the serial port
dataFrame = ser.readline() #read a line terminated by \n, but our device may put out a inline tab instead
#usually you should specify a timeout when using a readline(), since it blocks until it receives one

#dataFrame5Bytes = ser.read(5) #command to manually tell how many bytes to take
#do stuff to parse dataFrame and send the appropriate parts to data variables
#display the data variables under the correct titles


#way to manually set the newline in the readline() method to char other than \n with io module
''''
self.ser = serial.Serial(port=self.port,
                         baudrate=38400,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1)
self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),
                               newline = '\r', #change this to whatever the inline tab is, probably '\t'
                               line_buffering = True)
self.ser_io.write("ID\r")
self_id = self.ser_io.readline()
''''

#way to create your own readline() method

def _readline(self):
    eol = b'\r' #specifies end of line character, change this to inline tab escape character '\t'
    leneol = len(eol) #length of end of line character
    line = bytearray() #create an array of bytes to store the line we will read
    while True: #this loop says "never leave me!"
        c = self.ser.read(1) #read one byte from the serial port
        if c: #if there's something there
            line += c #add that byte to the byte array where we store our reads
            if line[-leneol:] == eol: #if
                break
        else:
            break
    return bytes(line)
