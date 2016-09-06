#! /usr/bin/env python
savetofile=True

import numpy as np
import matplotlib

if savetofile :
  matplotlib.use('PDF')

from matplotlib import pyplot as plt
import sys
import time

if savetofile :
  matplotlib.rcParams['ps.useafm'] = True
  matplotlib.rcParams['pdf.use14corefonts'] = True
  matplotlib.rcParams['text.usetex'] = True

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()
repos = np.DataSource()

def open_data_files (fname,header):
    if repos.exists(fname):
        dataset = np.genfromtxt(fname,skip_header=header)
        print 'ouverture du fichier ' + fname
        return dataset
    else:
        print 'This file : ' + fname + ' n existe pas'
        return -1

filename=[]
filename.append(("Jrl-Walkgen/tubingen_20160715_dfON_handmodif/TestNaveau2015tubingen1TestFGPIFull.dat",False))
filename.append(("Jrl-Walkgen/tubingen_20160715_dfOFF_handmodif/TestNaveau2015tubingen1TestFGPIFull.dat",False))
filename.append(("Jrl-Walkgen/tubingen_20160715_dfON_nohandmodif/TestNaveau2015tubingen1TestFGPIFull.dat",False))
filename.append(("Jrl-Walkgen/tubingen_20160715_dfOFF_nohandmodif/TestNaveau2015tubingen1TestFGPIFull.dat",False))
filename.append(("Jrl-Walkgen/tubingen_20160715_dfON_upperbodyfixed_handmodif/TestNaveau2015tubingen1TestFGPIFull.dat",False))
filename.append(("HRP2/TestNaveau2015tubingen1corr_2016_01_08_15_33-astate.log",True))
n=len(filename)
dataset=[]
figure=[]
graph=[]
x=[]

for i in range(n):
  figure.append(plt.figure(i,figsize=(15,15)))
  graph.append(figure[i].add_subplot(211))
  plt.ylabel("meter (m)")
  plt.xlabel("time (s)")
  graph.append(figure[i].add_subplot(212))
  plt.ylabel("meter (m)")
  plt.xlabel("time (s)")
  if i==0:
    minigraph = plt.axes([0.48, 0.57, .2, .15])

#str(index)
for i in range(n):
  dataset.append(open_data_files(filename[i][0],filename[i][1]))
#  graph[2*i].clear()
#  plt.ylabel("meter (m)")
#  plt.xlabel("time (s)")
#  graph[2*i+1].clear()
#  plt.ylabel("meter (m)")
#  plt.xlabel("time (s)")
  x.append(dataset[i][1:,0])

# plots
#graph1.plot(x , dataset[:,[1]], label='zmp x')
#graph1.legend(bbox_to_anchor=(0.95, 0.95), loc=2, borderaxespad=0.)
graph[0].plot(x[0] , dataset[0][1:,[13]], "b"   , label='CoP x',linewidth=2)
graph[0].plot(x[1] , dataset[1][1:,[44]], "g--" , label='CoPmb x',linewidth=3)
graph[0].plot(x[0] , dataset[0][1:,[44]], "r"   , label='CoPmb fil x', dashes=[8, 4, 2, 4, 2, 4],linewidth=3)#1628
graph[0].plot(x[4] , dataset[4][1:,[44]], "m" , label='CoPmb fil lb x', dashes=[8, 2, 2, 4, 2, 4],linewidth=3)
graph[0].legend(bbox_to_anchor=(0.75, 0.50), loc=2, borderaxespad=0., prop={'size':20})
plt.ylabel("meter (m)")
plt.xlabel("time (s)")

graph[1].plot(x[0] , dataset[0][1:,[14]], "b"   , label='CoP y',linewidth=2)
graph[1].plot(x[1] , dataset[1][1:,[45]], "g--" , label='CoPmb y',linewidth=3)
graph[1].plot(x[0] , dataset[0][1:,[45]], "r"   , label='CoPmb fil y', dashes=[8, 4, 2, 4, 2, 4],linewidth=3)
graph[1].plot(x[4] , dataset[4][1:,[45]], "m" , label='CoPmb fil lb y', dashes=[8, 2, 2, 4, 2, 4],linewidth=3)
graph[1].legend(bbox_to_anchor=(0.75, 0.96), loc=2, borderaxespad=0., prop={'size':20})
plt.ylabel("meter (m)")
plt.xlabel("time (s)")

# this is another inset axes over the main axes
minigraph.plot(x[0] , dataset[0][1:,[13]], "b"   , label='CoP x',linewidth=2)
minigraph.plot(x[1] , dataset[1][1:,[44]], "g--" , label='CoPmb x',linewidth=3)
minigraph.plot(x[0] , dataset[0][1:,[44]], "r"   , label='CoPmb fil x', dashes=[8, 4, 2, 4, 2, 4],linewidth=3)#1628
minigraph.plot(x[4] , dataset[4][1:,[44]], "m" , label='CoPmb fil lb x', dashes=[8, 2, 2, 4, 2, 4],linewidth=3)
minigraph.set_xlim(6, 10)
minigraph.set_ylim(0.51, 0.62)

for item in (graph[0].get_xticklabels() + graph[0].get_yticklabels()):
  item.set_fontsize(24)
graph[0].xaxis.label.set_fontsize(24)
graph[0].yaxis.label.set_fontsize(24)

for item in (graph[1].get_xticklabels() + graph[1].get_yticklabels()):
  item.set_fontsize(24)
graph[1].xaxis.label.set_fontsize(24)
graph[1].yaxis.label.set_fontsize(24)

for item in (minigraph.get_xticklabels() + minigraph.get_yticklabels()):
  item.set_fontsize(24)
minigraph.xaxis.label.set_fontsize(24)
minigraph.yaxis.label.set_fontsize(24)

#plt.xticks([])
#plt.yticks([])

figure[0].canvas.draw()

figure[1].clear()
graph[2] = figure[1].add_subplot(111)
ti = 10/0.005
x[5]=np.array(range(len(dataset[5][ti:,[122]])))*0.005

graph[2].plot(x[5] , dataset[5][ti:,[122]], "b"   , label='Force RF Z',linewidth=3)
graph[2].plot(x[5] , dataset[5][ti:,[128]], "g--" , label='Force LF Z',linewidth=3)
for item in (graph[2].get_xticklabels() + graph[2].get_yticklabels()):
  item.set_fontsize(24)

graph[2].xaxis.label.set_fontsize(24)
graph[2].yaxis.label.set_fontsize(24)

graph[2].set_ylabel("Force (N)")
graph[2].set_xlabel("time (s)")
graph[2].legend(bbox_to_anchor=(0.75, 0.96), loc=2, borderaxespad=0., prop={'size':20})
figure[1].canvas.draw()

zmprefx = np.array(dataset[0][1:,[13]])
zmpmbx = np.array(dataset[1][1:,[44]])
zmpmbcorrx = np.array(dataset[0][1:,[44]])

zmprefy = np.array(dataset[0][1:,[14]])
zmpmby = np.array(dataset[1][1:,[45]])
zmpmbcorry = np.array(dataset[0][1:,[45]])

meanzmpmbcorr = np.mean(np.sqrt((zmpmbcorrx-zmprefx)*(zmpmbcorrx-zmprefx)+(zmpmbcorry-zmprefy)*(zmpmbcorry-zmprefy)),dtype=np.float64)
meanzmpmb     = np.mean(np.sqrt((zmpmbx-zmprefx)*(zmpmbx-zmprefx)+(zmpmby-zmprefy)*(zmpmby-zmprefy)),dtype=np.float64)

maxzmpmbcorr = np.max(np.sqrt((zmpmbcorrx-zmprefx)*(zmpmbcorrx-zmprefx)+(zmpmbcorry-zmprefy)*(zmpmbcorry-zmprefy)))
maxzmpmb     = np.max(np.sqrt((zmpmbx-zmprefx)*(zmpmbx-zmprefx)+(zmpmby-zmprefy)*(zmpmby-zmprefy)))

print "mean zmpmb     - zmpref = ",meanzmpmb
print "mean zmpmbcorr - zmpref = ",meanzmpmbcorr
print "max zmpmb     - zmpref = ",maxzmpmb
print "max zmpmbcorr - zmpref = ",maxzmpmbcorr

if savetofile :
  figure[0].savefig('./copmb.pdf',bbox_inches='tight',format="pdf", dpi=900)
  figure[1].savefig('./forcez.pdf',bbox_inches='tight',format="pdf", dpi=900)
  #plt.annotate('' , '' , fontsize='xx-small' )
#graph[2].plot(x[2] , dataset[2][1:,[13,14,44,45]])
#graph[2].plot(x[3] , dataset[3][1:,[44,45]])

#graph[4].plot(x[0] , dataset[0][1:,[44,45]])
#graph[4].plot(x[1] , dataset[1][1:,[44,45]])
#graph[4].plot(x[2] , dataset[2][1:,[44,45]])
#graph[4].plot(x[3] , dataset[3][1:,[44,45]])

print "End of program"

