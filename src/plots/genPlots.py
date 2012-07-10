'''
Created on 09.07.2012

@author: gschoenb
'''
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

import perfTest as pT

def stdyStVerPlt(toPlot):
    '''
    Generate a steady state verification plot.
    @param toPlot A SsdTest object.
    '''
    x = np.array(toPlot.getStdyRnds())
    av = []
    avT = []
    avB = []
    av.append(toPlot.getStdyAvg())
    avTop = toPlot.getStdyAvg() * 1.10
    avBot = toPlot.getStdyAvg() * 0.9
    avT.append(avTop)
    avB.append(avBot)
    av = av * len(x)
    avT = avT * len(x)
    avB = avB * len(x)
    
    plt.clf()#clear
    plt.plot(x,toPlot.getStdyValues(),'o', label='IOPS', markersize=10)
    plt.plot(x, toPlot.getStdySlope()[0]*x + toPlot.getStdySlope()[1], 'r', label='Slope')
    plt.plot(x, av, '-', color='black',label='Average')
    plt.plot(x, avT, '--', color='black',label='Top')
    plt.plot(x, avB, '--', color='black',label='Bottom')
    
    plt.ylim(min(toPlot.getStdyValues())*0.75,max(toPlot.getStdyValues())*1.25)
    plt.xticks(x)
    plt.title("Steady State Verification Plot")
    plt.xlabel("Round")
    plt.ylabel("IOPS")
    plt.legend()
    plt.savefig(toPlot.getTestname()+'-stdyStVerPlt.png',dpi=300)
    
def stdyStConvPlt(toPlot):
    '''
    Generate a steady state convergence plot.
    @param toPlot A SsdTest object.
    '''
    rnds = toPlot.getRnds()
    matrices = toPlot.getRndMatrices()
    bsLens = len(matrices[0][-1])#fetch the number of bs of the first matrix
    
    #initialize matrix for plotting
    lines = []
    for i in range(bsLens):
        lines.append([])

    for rndMat in matrices:
        row = rndMat[-1]#last row is random write
        for i in range(len(row)):
            lines[i].append(row[i])#switch from row to column wise ordering of values
    
    plt.clf()#clear
    x = range(rnds + 1)#fetch number of rounds, we want to include all rounds
    for i in range(len(lines)):
        plt.plot(x,lines[i],'o-',label='bs='+pT.SsdTest.SsdTest.bsLabels[i])
    
    plt.xticks(x)
    plt.title("Steady State Convergence Plot")
    plt.xlabel("Round")
    plt.ylabel("IOPS")
    plt.legend()
    plt.savefig(toPlot.getTestname()+'-stdyStConvPlt.png',dpi=300)
    
def mes2DPlt(toPlot):

    mixWLds = []
    #each row will be a workload percentage
    for i in range(len(pT.SsdTest.SsdTest.mixWlds)):
        mixWLds.append([])
        #in each row will be the different block sizes
        for bs in range(len(pT.SsdTest.SsdTest.bsLabels)):
            mixWLds[i].append(0)
    matrices = toPlot.getRndMatrices()    
    for rndMat in matrices:
        #each row is a percentage of a workload
        for i,row in enumerate(rndMat):
            #in each row are the different block sizes
            for bs in range(len(row)):
                #calculate average
                if mixWLds[i][bs] != 0:
                    mixWLds[i][bs] += row[bs]
                    mixWLds[i][bs] = (mixWLds[i][bs]) / 2
                else:
                    mixWLds[i][bs] = row[bs]
    plt.clf()#clear plot
    x = [8,4,0.5]
    for i in range(len(mixWLds)):
        #the gonna be r/w percentage of mixed workload
        plt.plot(x,mixWLds[i],'o-',
                  label=str(pT.SsdTest.SsdTest.mixWlds[i])+'/'+str(100-pT.SsdTest.SsdTest.mixWlds[i]))
        
         
    plt.xticks(x)
    plt.title("IOPS test")
    plt.xlabel("Block Size (KB)")
    plt.ylabel("IOPS")
    plt.legend()
    plt.savefig(toPlot.getTestname()+'-mes2DPlt.png',dpi=300)
    
                
                
    
    
    
    
    
    
    
    
    
    
    