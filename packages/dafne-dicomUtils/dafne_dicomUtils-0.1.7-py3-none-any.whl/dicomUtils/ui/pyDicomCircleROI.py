#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 12:48:00 2015

@author: francesco
"""

from .pyDicomView import ImageShow
from .pyDicomView import main as parent_main
from matplotlib.patches import Circle
from matplotlib import pyplot as plt
import math
import numpy as np
try:
    import pyperclip
except:
    print("Pyperclip is not available. Results will not be copied")

class ROIStruct:
    def __init__(self, circle, text, center, radius):
        self.circle = circle
        self.text = text
        self.center = center
        self.radius = radius
        
    def setColor(self, color):
        self.circle.set_edgecolor(color)
        self.text.set_color(color)

class CircleROIClass(ImageShow):
    def __init__(self,  *args, **kwargs):
        ImageShow.__init__(self, *args, **kwargs)
        self.rois = []
        self.colors = ['blue', 'red', 'green', 'yellow', 'magenta', 'cyan', 'indigo']
        self.currentROI = 0
        self.fig.canvas.mpl_connect('close_event', self.print_results)
        self.instructions = 'Shift+click: Draw ROI. Ctrl+click: Delete ROI'
        tb = self.fig.canvas.toolbar
        tb.addSeparator()
        tb.addAction("Copy Results", lambda: self.print_results(None))
        
    def print_results(self, event):
        outStr = 'Image,\troi,\tmean,\tstd'
        for imIndex in range(0, len(self.imList)):
            for roiIndex in range(0, len(self.rois)):
                roi = self.rois[roiIndex]
                im = self.imList[imIndex]
                mean, std = self.calcMeanStd(roi, im)
                outStr += '\n%d,\t%d,\t%.3g,\t%.3g' % (imIndex, roiIndex, mean, std)
        print(outStr)
        try:
            pyperclip.copy(outStr)
        except:
            pass
                
        
        
    # calculates mean and std of the ROI
    def calcMeanStd(self, roi = None, im = None):                
        if roi is None:
            c = self.circleCenter
            r = self.circleRadius
        else:
            c = roi.center
            r = roi.radius

        if im is None:
            im = self.image
        
        ny, nx = im.shape
        ix, iy = np.meshgrid(np.arange(nx), np.arange(ny))
        distance = np.sqrt((ix - c[0])**2 + (iy - c[1])**2)
        # Mask portions of the data array outside of the circle
        maskedImage = np.ma.masked_where(distance > r, im)
        
        return np.ma.mean(maskedImage), np.ma.std(maskedImage)
        
    # generates nice text to be displayed
    def genText(self, mean, std):
        try:
            return 'Mean: %.3g\n Std: %.3g' % (mean, std)
        except:
            return 'Mean: \nStd:'
        
    def leftPressCB(self, event):
        if event.key == 'shift':
            self.createROI(event)
        if event.key == 'control'  or event.key == 'super':
            self.deleteROI(event)
        
    def roiContains(self, roi, event):
        return ((event.xdata-roi.center[0])**2 + (event.ydata-roi.center[1])**2) < roi.radius**2
    
    def deleteROI(self,event):
        #delete all the ROIs under cursor
        for roi in self.rois[:]:
            if self.roiContains(roi, event):
                #remove the roi
                roi.circle.remove()
                roi.text.remove()
                self.rois.remove(roi)
        #update colors
        self.currentROI = len(self.rois)
        for i in range(0, self.currentROI):
            self.rois[i].setColor(self.colors[i])
            self.rois[i].circle.set_label('Roi %d' % i)
        self.axes.legend()
        plt.draw()
            
        
    def createROI(self,event):
        # process only if the event is in the axes
        if not self.imPlot.contains(event):
            return
        
        # check if more rois are allowed
        if self.currentROI >= len(self.colors):
            return    
        
        self.circleCenter = (event.xdata, event.ydata) #self.axes.transData.inverted().transform([event.x, event.y])
        #self.circleCenter = (self.circleCenter[0], self.circleCenter[1]) # convert to tuple
        self.circleRadius = 1
        
        
        self.circle = Circle(self.circleCenter, self.circleRadius, facecolor = 'none', edgecolor = self.colors[self.currentROI], linewidth = 2.0)
        self.axes.add_patch(self.circle)
        mean, std = self.calcMeanStd()
        self.text = self.axes.text(self.circleCenter[0], self.circleCenter[1], self.genText(mean, std), color = self.colors[self.currentROI], verticalalignment = 'top' )
        plt.draw() # draw the circle
        
    def leftReleaseCB(self, event):
        if event.key == 'control'  or event.key == 'super':
            return
        # check if more rois are allowed
        if self.currentROI >= len(self.colors):
            return
        # add the new ROI to the list
        roiStruct = ROIStruct(self.circle, self.text, self.circleCenter, self.circleRadius)
        roiStruct.circle.set_label('Roi %d' % self.currentROI)
        self.rois.append(roiStruct)
        self.currentROI = self.currentROI+1
        self.axes.legend()
        plt.draw()
        
    def leftMoveCB(self,event):
        if event.key != 'shift':
            return
        # check if more rois are allowed
        if self.currentROI >= len(self.colors):
            return
        currentXY = (event.xdata, event.ydata) #self.axes.transData.inverted().transform([event.x, event.y])       
        self.circleRadius = math.sqrt((currentXY[0] - self.circleCenter[0])**2 + (currentXY[1] - self.circleCenter[1])**2)
        self.circle.set_radius(self.circleRadius)
        
        mean, std = self.calcMeanStd()
        self.text.set_position(currentXY)
        self.text.set_text(self.genText(mean, std))
        
        plt.draw()
        

    def refreshCB(self):
        for roi in self.rois:
            mean, std = self.calcMeanStd(roi)
            roi.text.set_text(self.genText(mean, std))
      

# when called as a script, load all the images in the directory
def main():
    parent_main(CircleROIClass)