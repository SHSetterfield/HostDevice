import serial #library to handle the serial port
import io #we will use this to specify a readline() char other than \n (newline)
import Tkinter #standard python GUI library
from Tkinter import *

ser = serial.Serial('/dev/tty.usbmodem1412', 38400) #setup the serial port

CoordinatorData = []

line = []
for index in range(0,57): #data will begin on 0x10
    data = ser.readline(1)
    line.append(data)

print line

del line[0:31]

print "deleted unnecessary bytes 0-31"

print line
if line[14] == 'C':  #then data is for coordinator device
    print "coordinator detected..."
    CoordinatorData.append(line[0]) #coordinator switch state
    CoordinatorData.append(line[4]) #coordinator battery (?)
    CoordinatorData.append(line[8]) #light sensor (cast as number later)

print CoordinatorData
from Tkinter import *

root = Tk()

w = Label(root, text="Coordinator")
w.pack()
x = Label(root, text=CoordinatorData[0])
x.pack()
root.mainloop()
