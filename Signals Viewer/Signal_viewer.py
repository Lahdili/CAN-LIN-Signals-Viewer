"""
Version 1.3

Version 1.1 : CAN support,
Version 1.2 : LIN support,
Version 1.3 : Bugfix,

"""

import matplotlib.pyplot as plt
import csv
import sys

# global variables

Start = False
Signal = []
byte_mask = 0x0
multi_plot = []
i = 0

Line_type = ('|','-', 'o','--',':','.',',','o', 'v', '^', '<','>','1','2', '3', '4', 's','p', '*', 'h', 'H','+','x','D','d','_','-')

def mask(hight, low):
    global byte_mask
    if hight.split(".")[0] == low.split(".")[0]:
        high_data = int(hight.split(".")[1])
        low_data = int(low.split(".")[1])
        for k in range(low_data,high_data+1):
             byte_mask = byte_mask + pow(2,k)
        #print "mask ", byte_mask
    else:
         print "Mask for more than one bayte not yet implemented"
         
def extract_data():
   global multi_plot, Start, Signal,byte_mask,input_file
   x = []
   y = []
   for i in range(len(Signal)):
       byte_mask = 0
       mask(Signal[i][2],Signal[i][3])

       with open(input_file,'r') as Trace:
          plots = csv.reader(Trace, delimiter=' ')
          for row in plots:

            if row == []:
                continue
            if row[0] != "Begin" and Start == False :
               continue
            else:
                if Start == False:
                    Start = True
                    continue
                row2=[]
                for n in range(len(row)):
                   if row[n]!="":
                      row2.append(row[n])
                row = row2
                if row[0] == "End" or row[1] ==  "log":
                    #if x != [] and y !=[]:
                    multi_plot.append((x,y))
                    Start = False
                    x = []
                    y = []
                    continue
                #print row[0]
                if row[1] == "L1"  and (row[2] == "RcvError" or row[2] == "SyncError") :
                    if row[2] == Signal[i][0]:
                         print "LIN error for frame ",Signal[i][0] ," at: ",row[0] #, " error code: ", row[3]
                    continue
                if row[1] == "L1"  and (row[4] == "0" or row[3] != "Rx") :
                    if row[2] == Signal[i][0]:
                         print "LIN error for frame ",Signal[i][0] ," at: ",row[0] #, " error code: ", row[3]
                    continue
                if row[2] == '':
                    print "error"
                    continue
                if row[2] == Signal[i][0] and row[1] == Signal[i][4]:
                    x.append(float(row[0]))
                    if row[1] == "L1":
                        Data=(int(row[4+int(Signal[i][2].split(".")[0])], 16) & byte_mask) >> int(Signal[i][3].split(".")[1])
                    else:
                        Data=(int(row[5+int(Signal[i][2].split(".")[0])], 16) & byte_mask) >> int(Signal[i][3].split(".")[1])
                    #print Signal," ", Data
                    y.append(Data)
                    #for j in range (int(row[5])):
                    #    print row[21+j],"\t"
                    #print "\n"    
                       
                #i = i+1    
                #print i ,row[6], "\t",row[14], "\t",row[18], "\t"
                #print i ,row

    
def display():
    global multi_plot, Signal

    for i in range(len(multi_plot)):
        plt.plot(multi_plot[i][0],multi_plot[i][1],Line_type[i], label=Signal[i][1])
    plt.xlabel('Time (s)')
    plt.ylabel('Signal(s)')
    plt.title('Signals Graphe')
    
    max_value = 1 
    for i in range (len(Signal)):
        if int(Signal[i][2].split(".")[1]) > max_value:
            max_value = int(Signal[i][2].split(".")[1])
    plt.ylim([-1,max_value+1])
    plt.legend()
    plt.show()

def interpolation():
    global multi_plot
    x = []
    y = []
    plot_data = []
    for i in range(len(multi_plot)):
        x = []
        y = []
        for j in range (len(multi_plot[i][0])-1):
            if multi_plot[i][1][j]!= multi_plot[i][1][j+1]:
                x.append(multi_plot[i][0][j])
                y.append(multi_plot[i][1][j])
                #interpolated value
                x.append(multi_plot[i][0][j+1])
                y.append(multi_plot[i][1][j])
            else:
                x.append(multi_plot[i][0][j])
                y.append(multi_plot[i][1][j])
        if multi_plot[i][0] == [] or multi_plot[i][0] ==[]:
            print "error: no data available for the signal ", Signal[i][1], " in frame ", Signal[i][0]
            x = []
            y = []
        else:
            x.append(multi_plot[i][0][j+1])
            y.append(multi_plot[i][1][j+1])
        plot_data.append((x,y)) 
    multi_plot = plot_data
# Main

# Define frames: maximal 25 signals

Frame1 = ("20","Signal_1","2.4","2.3","1")
Frame2 = ("20","Signal_2","1.1","1.0","1")
Frame3 = ("56","Signal_3","2.0","2.0","1")
Frame4 = ("56","Signal_4","4.0","4.0","1")


# Add signal to be ploted

Signal.append(Frame1)
Signal.append(Frame2)
Signal.append(Frame3)
Signal.append(Frame4)

#Set Input file
input_file = 'Test.asc'

extract_data()
interpolation()
display()

