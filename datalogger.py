#!/usr/bin/python2
# Copyright (c) 2018 Richard Major. All rights reserved.
# This script forms part of the John Harrison inspired BellPull project to measure the force applied by a bell ringer in a tower
# Code taken from many places so thanks if you recognise anything you wrote.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#     * The above copyright notice and this permission notice shall be included in all copies or substantial
#       portions of the Software.
#     * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#       BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#       IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#       WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#       SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. THE AUTHORS AND COPYRIGHT HOLDERS, HOWEVER,
#       ACCEPT LIABILITY FOR DEATH OR PERSONAL INJURY CAUSED BY NEGLIGENCE AND FOR ALL MATTERS LIABILITY
#       FOR WHICH MAY NOT BE LAWFULLY LIMITED OR EXCLUDED UNDER ENGLISH LAW

import RPi.GPIO as GPIO
import time
import sys
import os
import socket
from gyro import L3GD20
#from L3GD20 import L3GD20
import numpy
def callback1(channel):
    #  Not sure that I'm using this correctly (30/7/17)
    global Switch1
    Switch1=True
    #if GPIO.input(16):
      #  Switch1=True
    #else:
      #  Switch1=False
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(16,GPIO.IN)
GPIO.add_event_detect(16,GPIO.BOTH,callback=callback1)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.0.0.2', 10580) # chanage local host to the other ip.
Connection =False
StartTime=time.time()
Counter=0
message="Testing"
ledcount=0
ledout=True
Switch1=False
# Test for network connection.
# If no connection flas LED rapidly and wait 1 min for correction.
# If no correction detected carry on which will result in the desktop appearing.
# Correct working is shown by slow switching of the LED.
while Connection==False:
    TestTime=StartTime+60
    while time.time()<(TestTime):
        try:
            Counter=Counter+1
            sent = sock.sendto(message, server_address)
            Connection=True
            TestTime=StartTime
        except:
            ledcount=ledcount+1
            if ledcount==300:
                ledcount=0
                if ledout==True:
                    ledout=False
                else:
                    ledout=True
                GPIO.output(26,ledout)



#import the adxl345 module
import adxl345

#create ADXL345 object
accel = adxl345.ADXL345()

# Create gyro object
s = L3GD20(busId = 1, slaveAddr = 0x6b, ifLog = False, ifWriteBlock=False)
# Preconfiguration
s.Set_PowerMode("Normal")
s.Set_AxisX_Enabled(True)
s.Set_AxisY_Enabled(True)
s.Set_AxisZ_Enabled(True)
s.Set_FullScale_Value("2000dps")
s.Set_DataRateAndBandwidth(95, 12.5)
s.Set_FifoMode_Value("Bypass")
s.Init()
s.CalibrateZ()
s.CalibrateX()
s.CalibrateY()

import pygame
import random
from pygame.locals import *
pygame.init()
ScreenSize=(1000,700)
GameScreen=pygame.display.set_mode(ScreenSize)
pygame.display.set_caption("BellPull Monitor Signals")
black=0,0,0
White=255,255,255
LtGreen=0,255,0
DkGreen=0,50,0
Red=255,0,0
Blue=00,0,255
DefaultFont=None
GameFont=pygame.font.Font(DefaultFont,20)
GameText="BellPull (OSWESTRY)  V2.0"
GameTextGraphic=GameFont.render(GameText,True,White)
GameScreen.fill(DkGreen)
GameScreen.blit(GameTextGraphic,(10,10))
pygame.display.update()
xp=100
# Create the surface and pass in a tuple with its length and width
surf = pygame.Surface((2, 2))
# Give the surface a color to differentiate it from the background
surf.fill((255, 255, 255))
rect = surf.get_rect()
# Create the surface and pass in a tuple with its length and width
surf1= pygame.Surface((2, 2))
# Give the surface a color to differentiate it from the background
surf1.fill(Blue)
rect1 = surf1.get_rect()
plot=True
Switch=False
# Set up force measuring.

class HX711:
    def __init__(self, dout, pd_sck, gain=128, readBits=24):
        self.PD_SCK = pd_sck
        self.DOUT = dout
        self.readBits = readBits
        self.twosComplementOffset = 1 << readBits
        self.twosComplementCheck = self.twosComplementOffset >> 1

        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        self.set_gain(gain)

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def waitForReady(self):
        while not self.is_ready():
            pass

    def setChannelGainFactor(self):
        for i in range(self.GAIN):
          GPIO.output(self.PD_SCK, True)
          GPIO.output(self.PD_SCK, False)

    def correctForTwosComplement( self , unsignedValue ):
        if ( unsignedValue >= self.twosComplementCheck ):
            return -self.twosComplementOffset + unsignedValue
        else:
            return unsignedValue

    def read(self):
        self.waitForReady();
        unsignedValue = 0

        for i in range(0,self.readBits):
            GPIO.output(self.PD_SCK, True)
            unsignedValue = unsignedValue << 1
            GPIO.output(self.PD_SCK, False)
            bit = GPIO.input(self.DOUT)
            if ( bit ):
              unsignedValue = unsignedValue | 1

        self.setChannelGainFactor()
        signedValue = self.correctForTwosComplement( unsignedValue )

        self.lastVal = signedValue
        return self.lastVal

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()

        return sum / times

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

############# EXAMPLE
hx = HX711(27, 17,128)
hx.set_scale(7050)
hx.tare()

xp=100



initialtime=time.time()
#endtime=timenow + 120 # allow 2 minutes of sampling
measure= True
ledcount=0
ledout=True
#delaytime=0

timer=time.time()
while measure:
   # if time.time()>endtime:
           # measure=False
    
    #delaytime=0
    delaycount=1
    try:
        # Set timebase plot position as xp
        xp=xp+1
        # Read force gauge
        val = hx.get_units(1)
        py=int(val*2+350)
        #offset = max(1,min(80,int(val+40)))
        #otherOffset = 100-offset;
        # Read accelerometer
        axes = accel.getAxes(False)
        # to get axes as ms^2 use
        #axes = accel.getAxes(False), (True) reports in g

        #put the axes into variables
        x = axes['x']
        y = axes['y'] 
        z = axes['z']
        # Next 2 lines produce a kind of force graph unless coded out
        #print x,y,z
        #print (" "*offset+"#"+" "*otherOffset+"{0: 4.4f}".format(val));

        #Next code produces simple numeric output
        sf= int(val)
        sx=int(x*100)
        sy=int(y*100)
        sz=int(z*100)
        #print sf,sx,sy,szstr(val)+"'"+
        file_string=str(sf)+","+str(sx)+","+str(sy)+","+str(sz)
        

        #Now get gyro readings
        while s.Get_AxisDataAvailable_Value()[0] == 0:
            time.sleep(0.0001)
        #gx = s.Get_CalOutX_Value()
        gx = s.Get_RawOutX_Value()
        while s.Get_AxisDataAvailable_Value()[1] == 0:
            time.sleep(0.0001)        
        #gy = s.Get_CalOutY_Value()
        gy = s.Get_RawOutY_Value()
        while s.Get_AxisDataAvailable_Value()[2] == 0:
            time.sleep(0.0001)        
        #gzz = s.Get_CalOutZ_Value()
        gzz = s.Get_RawOutZ_Value()
        # Now read external switch
        SwitchVal=0
        if Switch1==True:
            #print('Triggered')
            Switch=True
            Switch1=False
        else:
            Switch=GPIO.input(16)
        if Switch==True:
            SwitchVal=1

        file_string=file_string+","+str(gx)+","+str(gy)+","+str(gzz)+str(SwitchVal)
        #print(Switch)
        #if GPIO.event_detected(16):
            #print(Switch1)
      

        #  Following code plots output against timebase
        
        timenow=time.time()
        if xp>900:
            xp=100
        y = 350+sf
        if py<100:
            py=100
        if py>600:
            py=600
        if Switch==False:
            GameScreen.blit(surf, (xp, py))
        else:
            GameScreen.blit(surf1, (xp, py))
        #  flip updates entire screen
        #pygame.display.update()
        pygame.display.update(xp,py,xp+2,py+2)
        # Send data over network
        #delay=time.time()-stime
        # Control sample rate
        endtime=timer+.013
        while time.time()<endtime:
            # delay count provides confidence that
            #   code is functioning fast enough ( 1 indicates possible problem).
            delaycount=delaycount+1
        
        timer=time.time()
        periodtime=timer-initialtime
        message = "{},{},{},{},{},{},{},{},{},{}".format(sf,sx,sy,sz,gx,gy,gzz,periodtime,delaycount,SwitchVal).encode('utf-8')
        # Send data
        sent = sock.sendto(message, server_address)
        #print(message)

        
        ledcount=ledcount+1
        if ledcount==70:
            ledcount=0
            if ledout==True:
                ledout=False
            else:
                ledout=True
            GPIO.output(26,ledout)
            
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
        fo.close()
        break
    

fo.close()
