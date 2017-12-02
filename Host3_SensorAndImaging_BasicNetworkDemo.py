import serial
import io
import Tkinter
from Tkinter import *
import ast
import time

root = Tk()
#sensor device global data (actually in router mode)
EndDeviceData = []
EndDeviceSwitch = StringVar()
EndDeviceLight = IntVar()

#coordinator device global data
CoordinatorData = []
CoordinatorSwitch = StringVar()
CoordinatorLight = IntVar()
print 'declaring imaging data vars'
#imaging device global data
ImagingData =[]
ImagingSwitch = StringVar()
ImagingFace = StringVar()
#'/dev/ttyACM0' on PC
ser = serial.Serial('/dev/tty.usbmodem1412', 38400)
print 'serial connection succesful'

def readSerial():
    print 'executing readserial()'
    #delete old data buffers before we pass through again on recursive calls
    line = []
    del CoordinatorData[:]
    del EndDeviceData[:]
    del ImagingData[:]
    for index in range(0,80): 
        data = ser.readline(1) 
        line.append(data)
    print "this is the raw appended line: "
    print line
    #now parse line for beginning of switch data
    for index in range(0,60):
        if (line[index] == 'F') or (line[index] == 'T'):
            startIndex=index
            break
    print "found an F at index: "
    print startIndex
    line = line[startIndex:80]
    print "sliced list to start of data fields..."
    for index in range(0,len(line)):
        if (line[index] == 'C') or (line[index] == 'E') or (line[index] == 'R') or (line[index] == 'I'):
            nameIndex=index
            print "found name start at index: "
            print nameIndex
            break

    print line
    if line[nameIndex] == 'C':  #then data is for coordinator device
        print "coordinator detected..."
        CoordinatorData.append(line[0]) #coordinator switch state
        CoordinatorData.append(line[4]) #coordinator battery (?)
        CoordinatorData.append(line[8]) #Light sensor data
        print "here's the coordinator switch data for this read: "
        print CoordinatorData[0]
        CoordinatorSwitch.set(CoordinatorData[0])
        CoordinatorLight.set(ord(CoordinatorData[2]))
        
    if line[nameIndex] == 'R':  #then data is for End device, which is actually a router for now
        print "Sensor Node detected..."
        EndDeviceData.append(line[0]) #coordinator switch state
        EndDeviceData.append(line[4]) #coordinator battery (?)
        EndDeviceData.append(line[8]) #Light sensor data
        print "the size of the EndDeviceData list is: "
        print len(EndDeviceData)
        print "here's the end device light sensor data..."
        print EndDeviceData[2]
        EndDeviceSwitch.set(EndDeviceData[0])
        EndDeviceLight.set(ord(EndDeviceData[2]))

    if line[nameIndex] == 'I':  #then data is for Imaging Node, which is a renamed router device
        print "Imaging Node detected, appending data..."
        ImagingData.append(line[0]) #imaging node switch state
        print ImagingData
        ImagingData.append(line[4]) #imaging node face ID
        print ImagingData
        ImagingData.append(line[8]) #unused
        print ImagingData
        print "the size of the EndDeviceData list is: "
        print len(ImagingData)
        print "here's the imaging node face ID..."
        print ImagingData[1]
        ImagingSwitch.set(ImagingData[0])
        faceStatus = 'not detected'
        if ImagingData[1]!= 'U':
           faceStatus = 'detected'
        ImagingFace.set(faceStatus)


    root.after(100, readSerial) #change this number to alter the frequency of readSerial calls


root.wm_title("SmartCity Network Data")
a = Label(root, text="Coordinator Button:")
a.pack()
x = Label(root, width = 60, height=7, takefocus=0, textvariable=CoordinatorSwitch)
x.pack()
b = Label(root, text="Coordinator Light Sensor:")
b.pack()
y = Label(root, width = 60, height=7, takefocus=0, textvariable=CoordinatorLight)
y.pack()

c = Label(root, text="Sensor Node Button:")
c.pack()
q = Label(root, width = 60, height=7, takefocus=0, textvariable=EndDeviceSwitch)
q.pack()
d = Label(root, text="Sensor Node Light Sensor:")
d.pack()
r = Label(root, width = 60, height=7, takefocus=0, textvariable=EndDeviceLight)
r.pack()
print 'declaring labels for imaging node...'
e = Label(root, text="Imaging Node Button:")
e.pack()
s = Label(root, width = 60, height=7, takefocus=0, textvariable=ImagingSwitch)
s.pack()
f = Label(root, text="Face Detection Status:")
f.pack()
t = Label(root, width = 60, height=7, takefocus=0, textvariable=ImagingFace)
t.pack()

readSerial()
root.mainloop()
