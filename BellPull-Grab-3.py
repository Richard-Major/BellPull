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
import socket
import sys
import time
import random
import math
import os
import pygame

from pygame.locals import *


def MouseCheck(record, LastChangeTime):
    global sf,sx,sy,sz,gx,gy,gz,timer,confidence,Switch
    #print('Mouse check')
    #Read data here
    data, address = sock.recvfrom(4096) # 4096 is the maximum size

    if data:
                # if we have data.. process it
        #print( data.decode('utf-8') )
        temp=str(data.decode('utf-8'))                
        INFO=temp.split(',')
        #print(INFO)
        sf=INFO[0]
        sx=INFO[1]
        sy=INFO[2]
        sz=INFO[3]
        gx=INFO[4]
        gy=INFO[5]
        gz=INFO[6]
        timer=INFO[7]
        Switch=INFO[9]
        #print(Switch)
        confidence=INFO[8]
        Plot_Force=int(float(sf)*float(a)+float(b))
        #print(Plot_Force)
        #Assume max force is 1000 and min is -100
        # Ensure it is in range
        if Plot_Force>1000:
            Plot_Force=1000
        if Plot_Force<-100:
            Plot_Force=-100
        # Draw red rect up to force and then green rect above
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness) 
        #Top is 50 down
        #Bottom is 450 down, so 400 represent 1100 force units
        # Calculate divide point
        Divide=int((Plot_Force+100)*400/1100)-36
        pygame.draw.rect(screen, GREEN, (25,50,15,(450-Divide)),0)
        pygame.draw.rect(screen, RED, (25,(450-Divide),15,Divide),0)        
        pygame.display.flip()           
        
    for event in pygame.event.get():
        #print('Event')
        if event.type==pygame.MOUSEBUTTONDOWN:
            if time.time()-LastChangeTime>2:
                LastChangeTime=time.time()
                if record == True:
                    record = False
                else:
                    record=True
    return record
                
    


###------------------------------------------
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.0.0.2', 10580) # this needs to be localhost as thats where the messages are sent to...
sock.bind( server_address ) # start listening
print('ready to receive data')
#Get calibration
fo1 = open("Setup/Calibration.csv", "r")
Cal_Data=fo1.readline()
fo1.close()
INFO=Cal_Data.split(',')
a=INFO[0]
b=INFO[1]
while True:
    pygame.init()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    DarkGrey =(200,200,200)
    size = (400, 500)
    screen = pygame.display.set_mode(size)
    screen.fill(DarkGrey)
    pygame.display.set_caption("BellPull Data Collector")
    #pygame.draw.rect(screen, RED, [50, 50, 150, 150], 0)
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
    pygame.display.flip() 
    text = font.render("Click anywhere to START/STOP", True, BLACK)
    screen.blit(text, [50, 25])
    pygame.display.flip()

    TowerImage = pygame.image.load("Church_sketch.jpg").convert()
    TowerImage = pygame.transform.scale(TowerImage, (150, 200))
    x = 220; # x coordnate of image
    y = 280; # y coordinate of image
    screen.blit(TowerImage, ( x,y,50,75)) # paint to screen
    pygame.display.flip() # paint screen one time
    record=False
    LastChangeTime=time.time()
    while record == False:
        record=MouseCheck(record,LastChangeTime)
    # Get the next file number and update.
    # A next file number ensures all files have a unique identifier.
    fo = open("Setup/NextFileNumber.csv", "r")
    Last_File_Number=fo.readline()
    fo.close()
    # Open NextFileNumber to write
    fo = open("Setup/NextFileNumber.csv", "w")
    Next_File_Number = int(Last_File_Number )+ 1
    file_string=str(Next_File_Number)
    fo.write( file_string);
    fo.close()
    # Open final data file
    FileName="Data/BellPullRaw"+str(Next_File_Number)+".csv"
    fo = open(FileName, "w")

    # Transfer calibration file info
    fo1 = open("Setup/Calibration.csv", "r")
    Cal_Data=fo1.readline()
    fo1.close()
    file_string=Cal_Data
    fo.write( file_string+chr(10))
   
    text = font.render("Started and Saving as :-", True, BLACK)
    screen.blit(text, [50, 75])
    pygame.display.flip()


    text = font.render(FileName, True, BLACK)
    screen.blit(text, [70, 125])
    pygame.display.flip()
    try:
        while record==True:
            
            file_string=str(sf)+","+str(sx)+","+str(sy)+","+str(sz)
            file_string=file_string+","+str(gx)+","+str(gy)+","+str(gz)
            file_string=file_string+","+str(timer)+","+str(confidence)+","+str(Switch)
            fo.write( file_string+chr(10)) # Is 10 correct ?    
            record=MouseCheck(record,LastChangeTime)
        if record == False:
            fo.close()
            print("Data collection terminated.")
            text = font.render("Saved.", True, BLACK)
            screen.blit(text, [50, 175])
            pygame.display.flip()

            i=0
            while fo.closed == False:
                i=i+1
            #print (i)
            
            
    finally:
        print( 'End reading ')
        #sock.close()
    record=True
    text = font.render("Click again to start over.", True, RED)
    screen.blit(text, [50, 225])
    pygame.display.flip()

    while record==True:
        record=MouseCheck(record,LastChangeTime)
        
print( 'closing socket' )
sock.close()            
