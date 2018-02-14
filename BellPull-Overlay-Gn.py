#!/usr/bin/env python2

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

from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import tkMessageBox
import socket
import sys
import time
import random
import math
import os

record=False
StartTime=time.time()
DrawRecord=[]
class App:
    def __init__(self, master):
        step=1
        frame = Frame(master)
        frame.pack()
        bottomframe = Frame(master)
        bottomframe.pack( side = BOTTOM )
        midframe=Frame(master)
        midframe.pack(side=BOTTOM)
        #  Single plot half step size
        self.button = Button(frame, text="Half x",fg='blue', command=self.half_step)
        self.button.pack(side=LEFT)        
        #  Single plot back
        self.button = Button(frame, text="-x WP",fg='orange', command=self.back_single)
        self.button.pack(side=LEFT)        
        #  Single plot setup
        self.button = Button(frame, text="Single Plot", command=self.single_plot)
        self.button.pack(side=LEFT)
        #  Single plot forward
        self.button = Button(frame, text="+x WP",fg='orange', command=self.next_single)
        self.button.pack(side=LEFT)
        #  Single plot double step size
        self.button = Button(frame, text="Double x",fg='blue', command=self.double_step)
        self.button.pack(side=LEFT)                         
        #  Single plot type
        self.button = Button(frame, text="Time/Position     ",fg='magenta', command=self.time_position)
        self.button.pack(side=LEFT) 
        #  TextBox7
        self.text7 = Text(frame,height=1,width=15,selectborderwidth=500)
        self.text7.pack(side=LEFT)
        # Get Data button
        self.get = Button(frame, text="File to process ?", command=self.get_data)
        self.get.pack(side=LEFT)
        # Load file buttons
        self.loadfile=Button(midframe,text="1st File to Overlay Plot ?",command=self.lh_open_file)
        self.loadfile.pack(side=LEFT)
        self.text6 = Text(midframe,height=1,width=20,selectborderwidth=500)
        self.text6.pack(side=LEFT)
        self.loadfile=Button(midframe,text="2nd File to Overlay Plot ?",command=self.rh_open_file)
        self.loadfile.pack(side=LEFT)
        # Text box
        self.text = Text(frame,height=1,width=33,selectborderwidth=500)
        self.text.pack(side=LEFT)
        # Quit button
        self.button = Button(frame, text="Exit", fg="red", command=self.shutdown)
        #self.button = Button(frame, text="Exit", fg="red", command=frame.quit) 
        self.button.pack(side=LEFT)
        #Calibrate button
        self.cal=Button(frame,text="Calibrate",command=self.calibrate)
        self.cal.pack(side=LEFT)
        #Calibrate button
        self.set=Button(frame,text="Setup",command=self.setup)
        self.set.pack(side=LEFT)
        # LH minus button
        self.lhless=Button(bottomframe,text="-1 WP",fg='orange',command=self.LHminus)
        self.lhless.pack(side=LEFT)
        # Text box 1
        self.text1 = Text(bottomframe,height=1,width=9,selectborderwidth=500)
        self.text1.pack(side=LEFT)
        # Text box 2
        self.text2 = Text(bottomframe,height=1,width=30,selectborderwidth=500)
        self.text2.pack(side=LEFT)
        # LH plus button
        self.lhplus=Button(bottomframe,text="+1 WP",fg='orange',command=self.LHplus)
        self.lhplus.pack(side=LEFT)
        # RH minus button
        self.rhless=Button(bottomframe,text="-1 WP",fg='orange',command=self.RHminus)
        self.rhless.pack(side=LEFT)
        # Text box 3
        self.text3 = Text(bottomframe,height=1,width=9,selectborderwidth=500)
        self.text3.pack(side=LEFT)
        # Text box 4
        self.text4 = Text(bottomframe,height=1,width=30,selectborderwidth=500)
        self.text4.pack(side=LEFT)
        # RH plus button
        self.rhplus=Button(bottomframe,text="+1 WP",fg='orange',command=self.RHplus)
        self.rhplus.pack(side=LEFT)
    def half_step(self):
            global step
            step=int(step/2)
            if step<1:step=1
    def double_step(self):
            global step
            step=int(step*2)
            if step>256:step=256                         
    def shutdown(self):
        root.destroy()
    def single_plot(self):
        global ProcFileName
        global FileName
        global DrawRecord
        global TargetRecord
        global ForceIn,PositionIn,EventIn,VelIn,TimeIn,MaxForce

        if Single_Plot==False:
            ProcFileName=""
            root.filename = tkFileDialog.askopenfilename(initialdir = "Final/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))                 
            ProcFileName=root.filename
            Name=ProcFileName.split('/')
            ShortName=Name[-1]
            self.text.delete(1.0, END)
            self.text.insert(END, ShortName)            
        SinglePlot=True
        fo=open(ProcFileName, "r")
        MaxForce=0
        ForceIn=[]
        PositionIn=[]
        EventIn=[]
        VelIn=[]
        TimeIn=[]
        # Data: Force, Position, Velocity, Acceleration, Time, Event, Sin(Theta),Time since BDC
        for line in iter(fo):
            line = line.rstrip('\n')
            list1 = line.split(",")
            force=float(list1[0])
            ForceIn.append(force)
            PositionIn.append(list1[1])
            EventIn.append(list1[5])
            VelIn.append(list1[2])
            TimeIn.append(list1[4])
            if force>MaxForce:MaxForce=force
            #print(TimeIn)
        fo.close()

        if TimePosition==True:
            self.single_time_plot()
        else:
            self.single_pos_plot()
    def single_time_plot(self):
        global DrawRecord
        global TargetRecord
        global EventIn
        global ForceIn
        global TimeIn
        ShortName=' WP '+str(TargetRecord)+' T'
        self.text7.delete(1.0, END)
        self.text7.insert(END, ShortName) 
        
        ###### Clear plotting area ################
        RecordLen=len(DrawRecord)
        if RecordLen<>0:
            for i in range(int(RecordLen)):
                w.delete(DrawRecord[i])
        DrawRecord=[]
        
        EventPointer=0
        RecordPointer=0
        while EventPointer<>TargetRecord:
            while EventIn[RecordPointer]<>'BDC-B':
                RecordPointer=RecordPointer+1
            EventPointer=EventPointer+1
            RecordPointer=RecordPointer+1
        #RecordPointer now points at the required start
        PlotTimeStart=TimeIn[RecordPointer]
        TimeTickTarget1=TimeTickInterval*4
        fill='blue'
        LineWidth=1
        LastPlotForce=0
        FillColour=["khaki1","wheat1"]
        FillColourPointer=0
        x=0
        for line in range(899):
            # First draw a background unless it is reverse
            if not "Rev" in EventIn[line+RecordPointer]:
                Drawing=w.create_line(LBorder+x,top+20,LBorder+x,top+height, fill=FillColour[FillColourPointer])
                DrawRecord.append(Drawing)
                if 'BDC' in EventIn[line+RecordPointer]:
                    FillColourPointer=FillColourPointer+1
                    if FillColourPointer==2:FillColourPointer=0
            # Now add the force graph                      
            force=float(ForceIn[line+RecordPointer])
            PForce=force/MaxForce*height
            if PForce<0:PForce=0
            Drawing=w.create_line(LBorder+x,height+top-LastPlotForce,LBorder+x,height+top-PForce, fill="black")
            DrawRecord.append(Drawing)
            LastPlotForce=PForce
            TimeNow=TimeIn[line+RecordPointer]
            x=x+1
            #  Add events
            event=False
            if "TDC+" in EventIn[line+RecordPointer]:
                colour="magenta"
                TickLength=15
                event=True
            if "Rev" in EventIn[line+RecordPointer]:
                colour="black"
                TickLength=20
                event=True
            if event:
                Drawing=w.create_line(LBorder+x,top,LBorder+x,top+TickLength,fill=colour,width=1)
                DrawRecord.append(Drawing)
                #print(LBorder+x,top,LBorder+x,top+TickLength)            
            #Manage time ticks
            TickLength=10
            x1=left
            if float(TimeNow)>TimeTickTarget1:
                Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height+top-TickLength, fill="black",width=4)
                DrawRecord.append(Drawing)
                TimeTickTarget1=float(TimeNow)+TimeTickInterval*4
                #print(TimeNow,TimeTickTarget1,TimeTickInterval)
 
            
        # Draw ticks on force axis
        scale=height/MaxForce
        FTickMeasure=0
        while FTickMeasure<height:
            Drawing=w.create_line(left,height+top-FTickMeasure,left+TickLength,height+top-FTickMeasure, fill="black",width=1)
            DrawRecord.append(Drawing) 
            FTickMeasure=FTickMeasure+int(TickInterval*scale)
        # Define axes
        Message="Vertical axis, 1 tick = "+str(TickInterval)+" "+FUnits
        Drawing=w.create_text(150, 440, text=Message)
        DrawRecord.append(Drawing)
        Message="Horizontal axis, 1 tick = "+str(TimeTickInterval*4)+" s"
        Drawing=w.create_text(850, 440, text=Message)
        DrawRecord.append(Drawing)            
    def single_pos_plot(self):
        global DrawRecord
        global TargetRecord
        global EventIn
        global ForceIn
        global PositionIn
        global VelIn
        global TickLength
        ShortName=' WP '+str(TargetRecord)+' P'
        self.text7.delete(1.0, END)
        self.text7.insert(END, ShortName)         
        ###### Clear plotting area ################
        RecordLen=len(DrawRecord)
        if RecordLen<>0:
            for i in range(int(RecordLen)):
                w.delete(DrawRecord[i])
        DrawRecord=[]
        # Draw all data
        RecordLen=len(ForceIn)
        LastPlotForce=height*.1
        LastPlotPos=450-180*2
        for i in range (RecordLen):
            PlotWidth=1
            x=int(450+float(PositionIn[i])*2)
            force=float(ForceIn[i])
            if force<-50: force=-50
            PForce=force/MaxForce*height*.8+height*.1
            colour='pale turquoise'
            if float(VelIn[i])<0:colour='pink'            
            Drawing=w.create_line(LBorder+LastPlotPos,height+top-LastPlotForce,LBorder+x,height+top-PForce, fill=colour,width=PlotWidth)
            DrawRecord.append(Drawing)
            LastPlotForce=PForce
            LastPlotPos=x
        # Now draw selcted whole pull in bold
        EventPointer=0
        RecordPointer=0
        while EventPointer<>TargetRecord:
            while EventIn[RecordPointer]<>'BDC-B':
                #  If BDC-H Keep these readings so the last ones can be used for starting the plot
                #if EventIn[RecordPointer]=='BDC-B':
                 #   LastPlotForce=float(ForceIn[RecordPointer])/MaxForce*.8+height*.1
                  #  LastPlotPos=float(PositionIn[RecordPointer])*2+450
                RecordPointer=RecordPointer+1
            EventPointer=EventPointer+1
            LastPlotForce=float(ForceIn[RecordPointer])/MaxForce*.8+height*.1
            LastPlotPos=float(PositionIn[RecordPointer])*2+450            
            RecordPointer=RecordPointer+1
            
        #RecordPointer now points at the required start
        LineWidth=2

        x=1
        while EventIn[RecordPointer+x]<>'BDC-B':
            force=float(ForceIn[x+RecordPointer])
            if force<-50: force=-50
            Pos=int(float(PositionIn[x+RecordPointer])*2)+450
            PForce=force/MaxForce*height*.8+height*.1
            #if PForce<0:PForce=0
            #if float(PForce)<height*.1:PForce=height*.1
            colour='blue'
            if float(VelIn[x+RecordPointer])<0:colour='red'
            #print(VelIn[x])
            x1=LBorder+(LastPlotPos)
            y1=height+top-(LastPlotForce)
            x2=LBorder+Pos
            y2=height+top-PForce
            Drawing=w.create_line(x1,y1,x2,y2, fill=colour,width=LineWidth)
            DrawRecord.append(Drawing)
            LastPlotForce=PForce
            LastPlotPos=Pos
            x=x+1
        # Draw ticks on force axis
        scale=height/MaxForce
        FTickMeasure=int(height*.1)
        while FTickMeasure<height:
            Drawing=w.create_line(left,height+top-FTickMeasure,left+TickLength,height+top-FTickMeasure, fill="black")
            DrawRecord.append(Drawing) 
            FTickMeasure=FTickMeasure+int(TickInterval*scale*.8)
        #Manage position ticks
        TickLength=20
        x1=left
        for position in [-180,0,180]:
            x=position*2+450
            Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height+top-TickLength, fill="black",width=3)
            DrawRecord.append(Drawing)
        #Manage minor position ticks
        TickLength=10
        x1=left
        for position in [-185,-175,-170,-165,-160,-155,-150,-145,-140,140,145,150,155,160,165,170,175,185]:
            x=position*2+450
            Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height+top-TickLength, fill="black",width=1)
            DrawRecord.append(Drawing)            
        # Define axes
        Message="Vertical axis, 1 tick = "+str(TickInterval)+" "+FUnits
        Drawing=w.create_text(150, 440, text=Message)
        DrawRecord.append(Drawing)
        Message="Horizontal axis, TDC (Hand), BDC, TDC (Back), Minor ticks at 5 degree intervals."
        Drawing=w.create_text(750, 440, text=Message)
        DrawRecord.append(Drawing)        
    def next_single(self):
        global TargetRecord,step
        TargetRecord=TargetRecord+step
        if TimePosition==True:
            self.single_time_plot()
        else:
            self.single_pos_plot()        
    def back_single(self):
        global TargetRecord,step
        TargetRecord=TargetRecord-step
        if TimePosition==True:
            self.single_time_plot()
        else:
            self.single_pos_plot()        
    def time_position(self):
        global TimePosition
        TimePosition= not TimePosition        
    def get_data(self):
        global ProcFileName
        global FileName
        ProcFileName=""
        root.filename = tkFileDialog.askopenfilename(initialdir = "Data/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))                 
        ProcFileName=root.filename
        self.text.delete(1.0, END)
        self.text.insert(END, ProcFileName)
            #================== Now process the data =======================         

            #  Develop file names here
        list2=ProcFileName.partition('Data')
        # Change Data to Inter or Final in directory
        TempFileName= list2[0]+'Inter'+list2[2]
        # Strip out BellPullRaw
        list3=TempFileName.partition('BellPullRaw')
        TempFileName=list3[0]+list3[2]
        list1=TempFileName.partition('.')    
        FileName=ProcFileName
        FileName1=list1[0]+'temp1'+list1[1]+list1[2]
        FileName2=list1[0]+'temp2'+list1[1]+list1[2]
        FileName3=list1[0]+'temp3'+list1[1]+list1[2]
        FileName4=list1[0]+'temp4'+list1[1]+list1[2]
        FileName5=list1[0]+'temp5'+list1[1]+list1[2]
        FileName6=list1[0]+'temp6'+list1[1]+list1[2]
        FileName7=list1[0]+'temp7'+list1[1]+list1[2]
        FileName8=list1[0]+'temp8'+list1[1]+list1[2]
        FileName9=list1[0]+'temp9'+list1[1]+list1[2]
        list4=FileName6.partition('Inter')
        FileName10=list4[0]+'Final/Plot-G-'+list3[2]
        def Comp_Sign(a,b):
            if math.copysign(float(a),float(b))==float(a):
                #Signs are same
                ZeroCross=False
            else:
                ZeroCross=True
            return ZeroCross
            # Pass 1 ... Remove extreme digital noise from force data
            #            Mange calibration, Dump accelerometer data
            #            and select active Gyro chanel.
        Message='1-Cleaning digital force signal.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        lastf=0
        MaxStep=300 # This may need adjusting.
        fo = open(FileName, "r")
        fout=open(FileName1, "w")
        # Now find the active channels
        # Get setup info
        fo1=open("Setup/Setup.cvs", "r")        
        Settings=fo1.readline()
        listSet=Settings.split(",") 
        fo1.close        
        AccCh=0
        for x in [1,2,3]:
            print(x,listSet[x])
            if (listSet[x])=='1':
                AccCh=x
        VelCh=0
        for x in [4,5,6]:
            if abs(int(listSet[x]))==1:
                VelCh=x
        VelSign=1
        if int(listSet[VelCh])<0:
            VelSign=-1
        #  Read in calibration info
        INFO=fo.readline()
        list1=INFO.split(",")
        a=float(list1[0])
        b=float(list1[1])      
        lineb=[0,0,0,0]
        lista=[0,0,0,0]
        list=[0,0,0,0,]
        # To find stepped digital noise compare 3 values
        # For noise the first and last must be similar with
        # the cental value offset.
        for i in [1,2,3]:
            temp=fo.readline()
            if not temp: break
            lineb[i]=temp
            lista[i]=lineb[i].split(",")
            temp=lista[i][0]
            list[i]=int(temp)        
        if abs(list[2]-list[1])>MaxStep:
            if abs(list[2]-list[3])>MaxStep:
                if abs(list[1]-list[3])<2*MaxStep:
                    mean=float((list[1])+float(list[3]))/2 
                    list[2]=mean
        # This has the force.
        # Deal with calibration
        Force= float(list[1])*float(a)+float(b)
        #Now reconstruct output and write
        outstring=str(Force)
        for k in [VelCh,7]: # Omit Acc, Non active Gyro 8, Confidence & switch
            if k==VelCh:
                lista[2][k]=str(float(lista[2][k])*int(VelSign))            
            outstring = outstring+','+lista[1][k]
        fout.write(outstring+'\n');
        while True:
            # Now rotate and read again
            list[1]=list[2]
            list[2]=list[3]
            lista[1]=lista[2]
            lista[2]=lista[3]
            temp=fo.readline()
            if not temp: break
            lineb[3]=temp
            lista[3]=lineb[3].split(",")
            temp=lista[3][0]            
            list[3]=int(temp)        
            if abs(list[2]-list[1])>MaxStep:
                if abs(list[2]-list[3])>MaxStep:
                    if abs(list[1]-list[3])<2*MaxStep:
                        mean=float((list[1])+float(list[3]))/2
                        list[2]=mean
           # This has the force.  Now reconstruct output and write
            # Deal with calibration
            Force= float(list[1])*float(a)+float(b)
            #Now reconstruct output and write
            outstring=str(Force)           
            for k in [VelCh,7]:
                if k==VelCh:
                    lista[2][k]=str(float(lista[2][k])*int(VelSign))                
                outstring = outstring+','+lista[1][k]
            fout.write(outstring+'\n');
        # This has the force.  Now reconstruct output and write
        # Deal with calibration
        Force= float(list[2])*float(a)+float(b)
        #Now reconstruct output and write
        outstring=str(Force)        
        for k in [VelCh,7]:
            if k==VelCh:
                lista[2][k]=str(float(lista[2][k])*int(VelSign))
            outstring = outstring+','+lista[2][k]
        fout.write(outstring+'\n');
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1
            #Pass 2 ... smooth data and compute GyroAcc.
        Message='2-Smoothing data.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        writelines=0
        writelines1=0
        fo = open(FileName1, "r")
        fout=open(FileName2, "w")
            #       Force       Channel 0
            #       Ang V       Channel  1
            #       time        Channel 2
            #   N.B.  GyroAcc but these times are not averaged
        Count = 0
        SampleSize=5
        Readings1=[]
        Readings2=[]
        Readings3=[]
        Readings4=[]
        Readings5=[]
        LastGyro=0
        LastTime=1
        Pointer=0
        for line in iter(fo):
            list1 = line.split(",")
                # Use  first SampleSize readings to calculate mean and then step through data.
            if Count<SampleSize:
                Readings1.append(float(list1[0]))
                Readings2.append(float(list1[1]))
                Readings3.append(float(list1[2])) 
            else:
                Readings1[Pointer]=float(list1[0])
                Readings2[Pointer]=float(list1[1])
                Readings3[Pointer]=float(list1[2]) 
                Pointer=Pointer+1
                if Pointer>(SampleSize-1):
                    Pointer=0
            if Count>=SampleSize:
                    #Calculate Average
                Sum1=0
                Sum2=0
                for i in range(0,(SampleSize),1):
                    Sum1=Sum1+Readings1[i]
                    Sum2=Sum2+Readings2[i]     
                Av1=Sum1/(SampleSize)
                Av2=Sum2/(SampleSize)*VelSign
                #  Calculate GyroAcc here using 2nd & 3rd readings
                LastGyro=Av2
                LastTime=Readings3[SampleSize-2]
                file_string=str(Av1)+","+str(Av2)+","+list1[2]
                fout.write( file_string);
                writelines=writelines+1
                Count=Count+1
            Count=Count+1
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1
            # -----------Pass 3 ------------
        Message='3-Finding Acceleration from Gyro.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
            # Open smoothed file
        fo=open(FileName2, "r")
        fout=open(FileName3, "w")
        NewCount=0
        Pointer=0
        lastgyro=0
        lasttime=0
        writelines=0
        for line in iter(fo):
            line = line.rstrip('\n')
            list1 = line.split(",")
            gyro=float(list1[1])
            time=float(list1[2])
            GyroDif=(gyro-lastgyro)
            TimeDif=(time-lasttime)
            GyroAcc=GyroDif/TimeDif
            writelines=writelines+1
            outstring=list1[0]+','+list1[1]+','+str(GyroAcc)+','+list1[2]+'\n'
            # Data is now: F, Vel, Acc, time
            fout.write( outstring);
            lastgyro=gyro
            lasttime=time
            Pointer=Pointer+1   
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1
            # --------Pass 4------------------
#  Integrate Gyro to get position
        Message='4-Integrating Gyro for position.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        # Integrate across 3 Gyro readings to get mid result.
        # Then add one result at end so that all file reading works.

############################################################################################

        # N.B.  The idea here will be to integrate angular velocity against time to give
        #   angular position.  Assume the bell is at rest against the stay at the start, so
        #   this angle must be set.
        #   Thereafter, the angle will increase until true BDC so this value can be identified
        #   and, if required corrections can be introduced.

#############################################################################################
        SetPos=-8.5
        SetPos=int(SetPos)-180
        StartPosition=SetPos
        GyroIn=[0,0,0]
        TimeIn=[0,0,0]
        OutLines=0
        fo=open(FileName3, "r")
        fout=open(FileName4, "w")
        Working =True
        #Read in first 2 values
        for i in (0,1):
            checkline=fo.readline()
            if not checkline: break
            checkline = checkline.rstrip('\n')        
            list1 = checkline.split(",")
            if i==0:
                outstring=checkline+','+str(SetPos)
                fout.write( outstring+'\n');
                OutLines=OutLines+1
            GyroIn[i]=list1[1]
            TimeIn[i]=list1[3]
            Position=SetPos
            InitialTime=list1[3] # This will end up with the 2nd value which will be the first result.
            LastLine=checkline
        # Now cycle trough data
        while Working:
            checkline=fo.readline()
            if not checkline: break
            checkline = checkline.rstrip('\n')        
            list1 = checkline.split(",")
            i=i+1
            GyroIn[2]=list1[1]
            TimeIn[2]=list1[3]
            # We now have 3 readings so compute  new position
            GyroDif=(float(GyroIn[2])-float(GyroIn[0]))
            TimeDif=float(TimeIn[2])-float(TimeIn[0])              
            #  This seems to produce double the expexted movement so use /4 rather than /2
            Position=float(Position)+(float(GyroIn[2])+float(GyroIn[0]))/4*float(TimeDif)
            outstring=LastLine+','+str(Position)
            fout.write( outstring+'\n');
            OutLines=OutLines+1
            LastLine = checkline
            # Rotate valuse
            for j in (0,1):
                GyroIn[j]=GyroIn[j+1]
                TimeIn[j]=TimeIn[j+1]
        #write final line  (repeating position)
        Position=float(Position)+float(GyroDif)/float(TimeDif)
        FinalPosition=Position
        outstring=LastLine+','+str(Position)
        FinalTime=list1[3]
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1         
        Message='Position file written.'
        self.text.delete(1.0, END)
        # Outlines has number of data points written
#=======================================================================
        Message='5 - Correcting gyro drift'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        # Calculate the drift per time period
        Drift= (float(FinalPosition)-float(StartPosition))/int(OutLines)
        Diff=float(FinalPosition)-float(StartPosition)
        TotalTime=float(FinalTime)-float(InitialTime)
        TimeDrift=float(Diff)/float(TotalTime)
        fo=open(FileName4, "r")
        fout=open(FileName5, "w")
        Count=0
        for line in iter(fo):
            line = line.rstrip('\n')
            list1 = line.split(",")
            Count=Count+1
            CorPos=float(list1[4])-float(TimeDrift)*(float(list1[3])-float(InitialTime))
            outstring=list1[0]+','+list1[1]+','+list1[2]+','+list1[3]+','+str(CorPos)+'\n'
            fout.write( outstring);
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1
        # We now have angular position, velecity and acceleration so all event points can be identified.
        # =============== Pass 6 =============================
        Message='6-Finding events'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        LastPos=0
        LastVel=0
        LastAcc=0
        fo=open(FileName5, "r")
        fout=open(FileName6, "w")
        for line in iter(fo):
            line=line.rstrip('\n')
            list1 = line.split(",")
            Event=""
            Vel=list1[1]
            Acc=list1[2]
            Pos=list1[4]
            Sine=math.sin(math.radians(float(Pos)))
            RevVel=Comp_Sign(Vel,LastVel)
            RevAcc=Comp_Sign(Acc,LastAcc)
            RevPos=Comp_Sign(Pos,LastPos)
            if abs(float(Pos))>180:
                # Over TDC
                Event=Event+'TDC+'
            if RevAcc:
                Rate=float(Acc)-float(LastAcc)
                if abs(Rate)>100:
                    # BDC found
                    Event='BDC-H'
                    if Rate>0:
                        Event='BDC-B'
            if RevVel:
                # Rope reversal found
                Rate=abs(float(Vel)-float(LastVel))
                if Rate <=30:
                    Event=Event+"Rev"
            if Event=='':
                if float(Acc) >=0:
                    if float(Vel) >=0:
                        Event='Fall from H'
                    else:
                        Event='Rise to H'
                if float(Acc) <=0:
                    if float(Vel) <=0:
                        Event='Fall from B'
                    else:
                        Event='Rise to B'
            if Event=="":
                Event="-"
            # Re-arrange output to give
            # Force, Position, Velocity, Acceleration, Time, Event, Sin(Theta)           
            outstring=list1[0]+','+list1[4]+','+list1[1]+','+list1[2]+','+list1[3]+','+Event+','+str(Sine)+'\n'
            fout.write( outstring);
            LastVel=Vel
            LastPos=Pos
            LastAcc=Acc
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1    
# =============== Pass 7 =============================
#  Manage time for BDC-B
        Message='8-Managing time per Whole Pull.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
        root.update_idletasks()
        #  Produce time values that start from zero
        #  for each stroke.
        fo=open(FileName6, "r")
        fout=open(FileName7, "w")
        BDCtime=0
        for line in iter(fo):
            line = line.rstrip('\n') 
            list1 = line.split(",")
            if 'BDC-B' in list1[5]:
                BDCtime=float(list1[4])
            BDCelapsed=float(list1[4])-float(BDCtime)
            outstring=line+','+str(BDCelapsed)
            fout.write( outstring+'\n');       
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1       
# =============== Pass 8 =============================
#Transfer to final file
        fo=open(FileName7, "r")
        fout=open(FileName10, "w")
        for line in iter(fo):
            outstring=line
            fout.write( outstring);
        fo.close()
        fout.close()
        while fout.closed == False:
            i=i+1         
        Message='Plot file written.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)
# +++++++++++++++ End of Processing ++++++++++++++++++++
    def calibrate(self):
        Message='Calibrate not implemented yet.'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)         
    def setup(self):
        ###############################################################
        #
        #   This is intended to identify active sensor channels
        #   for acceleration and velocity, and consider their
        #   signs.  (Acceleration removed 21/11/17) Information written to
        #   a setup file used for
        #   all data processing.  This file collect with the bell
        #   down and given one quick pull to start the bell swinging.
        #   Requires a short period at start with no pull.
        #
        #################################################################
        global FileName
        Message='Checking setup...'
        self.text.delete(1.0, END)
        self.text.insert(END, Message)         
        root.filename = tkFileDialog.askopenfilename(initialdir = "",title = "Select setup file",filetypes = (("csv files","*.csv"),("all files","*.*")))                 
        SetupFileName=root.filename
        fo = open(SetupFileName, "r")
        fout=open("Setup/Setup.cvs", "w")
        #  N.B.  Acc noted here is from accelerometer, not Acc computed from Gyro readings!
            # 0 - Force
            # 1 - Acc x
            # 2 - Acc y
            # 3 - Acc z
            # 4 - Vel x
            # 5 - Vel y
            # 6 - Vel z
            # The useful Vell and Acc channels will both be near zero
            # with the bell at rest but will have maximum amplitude
            # when the bell swings.
            # Use readings 10 to 50 to find low values and then
            # monitor max and min
        listMax=[0,0,0,0,0,0,0]
        listMin=[0,0,0,0,0,0,0]
        listZero=[0,0,0,0,0,0,0]    
        INFO=fo.readline()
        i=0
        j=0
        for line in iter(fo):
            list1 = line.split(",")
            if i<50 and i>10:
                for j in [4,5,6]:
                    a=float(listZero[j])
                    b=float(list1[j])
                    listZero[j]=a+b
                i=i+1
            else:
                if i==50:
                    # Set all list values to the mean zero reading
                    for j in [4,5,6]:
                        a=float(listZero[j])/40
                        listZero[j]=a
                        listMax[j]=listZero[j]
                        listMin[j]=listZero[j]
                # Now find max and min readings
                for j in [4,5,6]:
                    if float(list1[j])>float(listMax[j]):
                        listMax[j]=list1[j]
                    if float(list1[j])<float(listMin[j]):
                        listMin[j]=list1[j]
                    i=i+1
        fo.close()
        # Now determine active channels
        listActive=[1,1,0,0,0,0,0]
        MaxDif=-100
        '''
        # For Acc
        # Assume readings below +/- 200 are near zero
        for j in [1,2,3]:
            if abs(listZero[j])<200:
                listActive[j]=abs((float(listMax[j])-float(listMin[j])))
                if (float(listActive[j]))>(float(MaxDif)):
                    MaxDif=float(listActive[j])
        for j in [1,2,3]:
            if float(listActive[j])==float(MaxDif):
                listActive[j]=1
            else:
                listActive[j]=0
        '''
        # For Vel
        # Assume readings below +/- 20 are near zero
        MaxDif=-100
        for j in [4,5,6]:
            if abs(listZero[j])<20:
                listActive[j]=abs((float(listMax[j])-float(listMin[j])))
                if (float(listActive[j]))>(float(MaxDif)):
                    MaxDif=float(listActive[j])
        for j in [4,5,6]:
            if float(listActive[j])==float(MaxDif):
                listActive[j]=1
            else:
                listActive[j]=0                                  
        # If this has worked corectly there should be 3 active channels.
        #  Active channels detected but signs to be dealt with.
        #  Only the velocity needs a sign in anlysis so define a convention
        #       Handstroke direction is +ve
        #       and this is the first active velocity in this test.
        # To avoid noise look for 5 consecutive non zero readings
        for k in [4,5,6]:
            match=0
            if int(listActive[k])==1:
                match=1
            if match==1:
                for j in [k]:        
                    Sign=0
                    Count=0
                    ConsecCount=0
                    LastCount=0
                    SignFound=False
                    Trigger=abs(float(listMax[j])-float(listMin[j]))*.01
                    fo = open(SetupFileName, "r")
                    INFO=fo.readline()
                    for line in iter(fo):
                        Count=Count+1
                        if SignFound==False:
                            list1 = line.split(",")
                            TestVal=abs(float(list1[j]))-float(listZero[j])
                            if abs(TestVal)>float(Trigger):
                                if Count==LastCount+1:
                                    ConsecCount=ConsecCount+1
                                else:
                                    ConsecCount=0
                                if ConsecCount==5:
                                    SignFound=True
                                    if float(list1[j])<float(listZero[j]):
                                        Sign=1
                                    else:
                                        Sign=-1
                            LastCount=LastCount+1
                    fo.close()
                    listActive[j]=Sign
        count=0
        for j in [0,1,2,3,4,5,6]:
            count=count+abs(int(listActive[j]))
        if count==3:
            outstring=''
            for j in [0,1,2,3,4,5,6]:
                outstring=outstring+str(listActive[j])+','
            # The other data fields are time,confidence and switch
            # of which the first and last will be used so add these in.
            outstring=outstring+'1' +','+'0'+','+'1'+','+'\n'
            fout.write(outstring);
            fo.close()
            fout.close()
            Message='File written OK. '
            self.text.delete(1.0, END)
            self.text.insert(END, Message)             
            while fout.closed == False:
                i=i+1
        else:
            Message='File problem. '
            self.text.delete(1.0, END)
            self.text.insert(END, Message)            
    def LHminus(self):
        global WholePullPlot1
        global WholePulls1
        WholePullPlot1=WholePullPlot1-1
        if WholePullPlot1<1:
            WholePullPlot1=WholePulls1
        Message1=str(WholePullPlot1)+' of '+str(WholePulls1)
        self.text1.delete(1.0, END)
        self.text1.insert(END, Message1)
        check_files()        
    def LHplus(self):
        global WholePullPlot1
        global WholePulls1
        WholePullPlot1=WholePullPlot1+1
        if WholePullPlot1>WholePulls1:
            WholePullPlot1=1
        Message1=str(WholePullPlot1)+' of '+str(WholePulls1)
        self.text1.delete(1.0, END)
        self.text1.insert(END, Message1)
        check_files()
    def RHminus(self):
        global WholePullPlot2
        global WholePulls2
        WholePullPlot2=WholePullPlot2-1
        if WholePullPlot2<1:
            WholePullPlot2=WholePulls2
        Message3=str(WholePullPlot2)+' of '+str(WholePulls2)
        self.text3.delete(1.0, END)
        self.text3.insert(END, Message3)
        check_files()                          
    def RHplus(self):
        global WholePullPlot2
        global WholePulls2
        WholePullPlot2=WholePullPlot2+1
        if WholePullPlot2>WholePulls2:
            WholePullPlot2=1
        Message3=str(WholePullPlot2)+' of '+str(WholePulls2)
        self.text3.delete(1.0, END)
        self.text3.insert(END, Message3)
        check_files()        
    def lh_open_file(self):
        global LeftFileName
        LeftFileName=""
        # Open LH file for plotting      
        root.filename = tkFileDialog.askopenfilename(initialdir = "Final/",title = "Select 1st file",filetypes = (("csv files","*.csv"),("all files","*.*")))                 
        LeftFileName=root.filename
        lista=LeftFileName.rpartition('/')
        Message4=lista[2]        
        self.text2.delete(1.0, END)
        self.text2.insert(END, Message4)
        check_files()
    def rh_open_file(self):
        # Open RH file for plotting
        global RightFileName
        root.filename = tkFileDialog.askopenfilename(initialdir = "Final/",title = "Select 2nd file",filetypes = (("csv files","*.csv"),("all files","*.*")))                                                    
        RightFileName=root.filename
        lista=RightFileName.rpartition('/')
        Message4=lista[2]
        self.text4.delete(1.0, END)
        self.text4.insert(END, Message4)
        check_files()
def Key_Pause():
        time.wait(20)
def check_files():
    global scale
    global Time0
    global Time1
    global WholePulls1
    global WholePulls2
    global DrawRecord
    ThisTime=0
    LastTime=0
    NHand=[0,0]
    NBack=[0,0]
    FMaxH=[0,0]
    FMaxB=[0,0]
    Time0=[]
    Time1=[]
    FMax=0
    ####  Enable next line for Python3 ####
    #if (LeftFileName != '') and (RightFileName!=''):
    #### Comment out next line for Python3 ####
    if (LeftFileName <> '') and (RightFileName<>''):
        # Both graphs are defined so establish baseline data
        pointer=-1
        for FileName in (LeftFileName,RightFileName):
            pointer=pointer+1
            fo=open(FileName, "r")
            Hand=True
            LastRealTime=0
            for line1 in iter(fo):
                list1 = line1.split(",")
                # 0-Force, 4- Total Time, 5- Event, 7-Whole Pull Time
                ThisTime=float(list1[7])
                ThisRealTime=float(list1[4])
                ThisEvent=list1[5]
                if 'BDC' in ThisEvent:
                    # This code will produce a list of times
                    # starting with the first wait period, followed
                    # by Hand, Back, Hand, .........
                    Hand=not Hand
                    # This is the start of Hand or Back stroke
                    if Hand==True:
                        #It is a Handstroke
                        NHand[pointer]=NHand[pointer]+1
                    else:
                        NBack[pointer]=NBack[pointer]+1
                    #We can store the time of each stroke
                    ElaspedTime=ThisRealTime-LastRealTime
                    LastRealTime=ThisRealTime
                    if pointer==0:
                        Time0.extend([float(ElaspedTime)])
                    else:
                        Time1.extend([float(ElaspedTime)])
                LastTime=ThisTime          
                Force =float(list1[0])
                if Force>FMax: FMax=Force
                if Hand==True:
                    if Force>FMaxH[pointer]:
                        FMaxH[pointer]=Force
                else:
                    if Force>FMaxB[pointer]:
                        FMaxB[pointer]=Force
            fo.close()        
        WholePulls1=NHand[0]
        WholePulls2=NHand[1]
        # Ensure whole pull from stand is not used
        WholePullPlot1=2
        WholePullPlot2=2
        ###### Clear plotting area ################
        RecordLen=len(DrawRecord)
        print(RecordLen)
        if RecordLen<>0:
            for i in range(int(RecordLen)):
                w.delete(DrawRecord[i])
        DrawRecord=[]
        scale=height/FMax
        # Draw ticks on force axis
        FTickMeasure=0
        while FTickMeasure<height:
            Drawing=w.create_line(left,height+top-FTickMeasure,left+TickLength,height+top-FTickMeasure, fill="black")
            DrawRecord.append(Drawing) 
            FTickMeasure=FTickMeasure+int(TickInterval*scale)

        Plot()
def Plot():
    global scale
    global Time0
    global Time1
    Marker1=''
    Marker2=''
    FillCount=0
    FillFrequency=3
    # Now open the two files and scan to the start of the required whole pulls
    fo1=open(LeftFileName, "r")
    fo2=open(RightFileName, "r")
    count=1
    while count<>(WholePullPlot1):
        INFO1=fo1.readline()
        if 'BDC-B' in INFO1: count=count+1
    # The fo1 pointer should now be at the start of plot data
    count=1
    while count<>(WholePullPlot2):
        INFO2=fo2.readline()
        if 'BDC-B' in INFO2: count=count+1
    # The fo2 pointer should now be at the start of plot data
    # The number of pixels across is half the width
    Npixels=int(width/2)
    # Read two samples and then interpolate for pixels
    INFO1=fo1.readline()
    INFO2=fo2.readline()
    list1 = INFO1.split(",")
    list2 = INFO2.split(",")
    LastForce1=list1[0]
    LastForce2=list2[0]
    LastTime1=list1[7]
    LastTime2=list2[7]
    TimeEnd1=list1[7]
    INFO1=fo1.readline()
    INFO2=fo2.readline()
    list1 = INFO1.split(",")
    list2 = INFO2.split(",")
    NextForce1=list1[0]
    NextForce2=list2[0]
    NextTime1=list1[7]
    NextTime2=list2[7]
    TimeStep1=float(float(Time0[(WholePullPlot1*2-2)])/int(Npixels))
    TimeStep2=float(float(Time1[(WholePullPlot2*2-2)])/int(Npixels))
    MaxTime1=float(Time0[(WholePullPlot1*2-2)])+float(Time0[(WholePullPlot1*2-1)])
    MaxTime2=float(Time1[(WholePullPlot2*2-2)])+float(Time1[(WholePullPlot2*2-1)])
    TimeTickTarget1=0.25
    TimeTickTarget2=0.25
    MidTime1=0
    MidTime2=0
    LastMidTime1=0
    LastMidTime2=0
    Draw3=True
    Draw4=True    
    for x in range(width):
        LastMidTime1=MidTime1
        MidTime1=MidTime1+TimeStep1
        LastMidime2=MidTime2
        MidTime2=MidTime2+TimeStep2
        # Check that the time is in this range
        if float(NextTime1)<float(MidTime1): #We need a new 1 reading
            if MidTime1<MaxTime1:
                LastTime1=NextTime1
                LastForce1=NextForce1
                INFO1=fo1.readline()
                list1 = INFO1.split(",")
                NextForce1=list1[0]
                NextTime1=list1[7]
                Marker1=list1[5]    
        if float(NextTime2)<float(MidTime2): #We need a new 2 reading
            if MidTime2<MaxTime2:
                LastTime2=NextTime2
                LastForce2=NextForce2
                INFO2=fo2.readline()
                list2 = INFO2.split(",")
                NextForce2=list2[0]
                NextTime2=list2[7]
                Marker2=list2[5]
        # Interpolation of data 1 should now be possible
        ForceDif1=float(NextForce1)-float(LastForce1)
        TimeDif1=float(NextTime1)-float(LastTime1)
        StepTime1=float(MidTime1)-float(LastTime1)
        StepForce1=float(StepTime1)/float(TimeDif1)*float(ForceDif1)        
        PlotForce1=float(StepForce1)+float(LastForce1)
        PForce1=int(float(PlotForce1)*scale)
        if MidTime1>MaxTime1:PForce1=0
        if PForce1<0:PForce1=0
        if PForce1>height-1: PForce1=height-1
        Drawing=w.create_rectangle(LBorder+x,height+top-PForce1,LBorder+x+2,height+top-PForce1-2, fill="blue", outline="blue")
        DrawRecord.append(Drawing)
        # Interpolation of data 2 should now be possible
        ForceDif2=float(NextForce2)-float(LastForce2)
        TimeDif2=float(NextTime2)-float(LastTime2)
        StepTime2=float(MidTime2)-float(LastTime2)
        StepForce2=float(StepTime2)/float(TimeDif2)*float(ForceDif2)        
        PlotForce2=float(StepForce2)+float(LastForce2)
        PForce2=int(float(PlotForce2)*scale)
        if MidTime2>MaxTime2:PForce2=0        
        if PForce2<0:PForce2=0
        if PForce2>height-1: PForce2=height-1            
        Drawing=w.create_rectangle(LBorder+x,height+top-PForce2,LBorder+x+2,height+top-PForce2-2, fill="green", outline="green")
        DrawRecord.append(Drawing)
        #Manage fill
        FillCount=FillCount+1
        if FillCount>FillFrequency:
            LineWidth=1
            Space=abs(PForce1-PForce2)
            if Space>4:
                if PForce1>PForce2:
                    fill='yellow'
                    Ptop=PForce1-3
                    Pbottom=PForce2+3
                else:
                    fill='red'
                    Ptop=PForce2-3
                    Pbottom=PForce1+3
                Drawing=w.create_line(LBorder+x,height+top-Ptop,LBorder+x,height+top-Pbottom, fill=fill,width=LineWidth)
                DrawRecord.append(Drawing)
                FillCount=0
        #Manage Events
        # N.B. Events are identified at the sampling frequency but position can be estimated by interpolation.
        #       But do it simply for starters
        Draw=False
        Draw2=False
        LineWidth=1
        if 'TDC' in Marker1:
            fill='magenta'
            Draw=True
            length=TickLength*2        
        if 'Rev'in Marker1:
            fill='orange'
            length=TickLength*3
            Draw=True
        if Draw==True:
            Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height+top-length, fill=fill,width=LineWidth)
            DrawRecord.append(Drawing)
        if 'TDC' in Marker2:
            fill='magenta'
            Draw2=True
            length=TickLength*2   
        if 'Rev'in Marker2:
            fill='orange'
            length=TickLength*3
            Draw2=True
        if Draw2==True:
            Drawing=w.create_line(LBorder+x,top,LBorder+x,top+length, fill=fill,width=LineWidth)
            DrawRecord.append(Drawing)
        #Manage time ticks
        TickLength=10
        x1=left
        if MidTime1>TimeTickTarget1:
            Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height+top-TickLength, fill="blue",width=3)
            DrawRecord.append(Drawing)
            TimeTickTarget1=TimeTickTarget1+TimeTickInterval
        # Now time ticks for graph 2 at top
        if MidTime2>TimeTickTarget2:
            Drawing=w.create_line(LBorder+x,top,LBorder+x,top+TickLength, fill="green",width=3)
            DrawRecord.append(Drawing)
            TimeTickTarget2=TimeTickTarget2+TimeTickInterval
        #Check for change of stroke
        if 'BDC' in INFO1 and Draw3==True:
            TimeStep1=float(float(Time0[(WholePullPlot1*2-1)])/int(Npixels))
            Drawing=w.create_line(LBorder+x,height+top,LBorder+x,height/2+top, fill='blue',width=LineWidth)
            DrawRecord.append(Drawing)
            Draw3=False
        if 'BDC' in INFO2 and Draw4==True:
            TimeStep2=float(float(Time1[(WholePullPlot2*2-1)])/int(Npixels))            
            Drawing=w.create_line(LBorder+x,top,LBorder+x,height/2+top, fill='green',width=LineWidth)            
            DrawRecord.append(Drawing)
            Draw4=False
        # Define axes
        Message="Vertical axis, 1 tick = "+str(TickInterval)+" "+FUnits
        Drawing=w.create_text(150, 440, text=Message)
        DrawRecord.append(Drawing)
        Message="Horizontal axis, 1 tick = "+str(TimeTickInterval)+" s"
        Drawing=w.create_text(850, 440, text=Message)
        DrawRecord.append(Drawing) 
    fo1.close()
    fo2.close()
#=========== Setup and mainloop ===============================
RightFileName=""
LeftFileName=""
#  Define plot area variables
ScreenWidth=1000  # Width
ScreenHeight=450  # Height
LBorder = 50      # Left border
RBorder = 50      # Right border
TBorder = 150     # Top border
BBorder = 150     # Bottom border
CentreGap= 50     # Gap between plot areas
TickInterval = 50 # Gap between ticks on force axis (in force units)
FUnits='N'          # Force units
TickLength=10     # Length of ticks on force axis
MarkerLength = 0  # Lenght of event markers drawn from time axis
                  #   Set to zero for full graph height
LowestForce=0     # Cut off for display of force.
MarkerLength=10
NoForceCutOff = 200 # Used for jumping out of data capture.
NoForceTime = 250     #  Timer for jumping out of data capture
ShowMinForce=-100      #Used for simple indicator
ShowMaxForce=800    #           "
ShowRange=525       #  Height of simple indicator
TimeTickInterval=0.25 # Time between time ticks
step=1              # Number of whole pulls to step over
WholePulls1=10
WholePulls2=10
WholePullPlot1=1
WholePullPlot2=1
toggle=False
Single_Plot=False
# Define colours
LineType=['Target Hand','Target Back','Student Hand','Student Back']
LineType.extend(['TDC','Reverse','Overpull','Underpull'])
Colour=['Green','Green','Blue','Blue','Orange','Red','Red','Orange']
#Define graphs
Graph=['Target Hand','Target Back','Student Hand','Student Back']
root = Tk()
root.title("BellPull (the Oswestry Pullometer, inspired by John Harrison)")
app = App(root)
w = Canvas(root, width=ScreenWidth, height=ScreenHeight, bg = 'cyan')
w.pack()

left=50
width=900
top=25
height=400
# Capture key action
w.bind("<Key>", Key_Pause)
# Define mid markers for 2 graphs
Mid1=int(top+(height*.55))
Mid2=int(top+(height*.45))
offset=0
w.create_rectangle(left, top, left+width, top+height, fill="white")
LeftFileName=""
RightFileName=""
msg=''
TargetRecord=1
TimePosition=True
def key(event):
    if event.char == event.keysym:
        msg = 'Normal Key %r' % event.char
    elif len(event.char) == 1:
        msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
    else:
        msg = 'Special Key %r' % event.keysym

root.bind_all('<Key>', key)
root.mainloop()

#root.destroy() # optional; see description below
