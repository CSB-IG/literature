## "pycxsimulator.py"
## Realtime Simulation GUI for PyCX
##
## Developed by:
## Chun Wong
## email@chunwong.net
##
## Revised by:
## Hiroki Sayama
## sayama@binghamton.edu
##
## Copyright 2012 Chun Wong & Hiroki Sayama

## The following two lines should be placed at the beginning of your simulator code:
##
## import matplotlib
## matplotlib.use('TkAgg')

from Tkinter import *
import pylab as PL

class GUI:

    ## GUI variables
    titleText = 'PyCX Simulator'  # window title
    timeInterval = 0              # refresh time in milliseconds
    running = False
    modelFigure = None
    
    def __init__(self,title='PyCX Simulator',interval=0):
        self.titleText = title
        self.timeInterval = interval
        self.initGUI()

    def initGUI(self):
        #create root window
        self.rootWindow = Tk()
        self.rootWindow.wm_title(self.titleText)
        self.rootWindow.protocol('WM_DELETE_WINDOW',self.quitGUI)
        self.rootWindow.geometry('+30+30')
                      
        #buttons
        self.frameButton = Frame(self.rootWindow)
        self.frameButton.grid(row=1,column=0,padx=5,pady=5)
        self.runPauseString = StringVar()
        self.runPauseString.set("Run")
        self.buttonRun = Button(self.frameButton,width=11,height=1,textvariable=self.runPauseString,command=self.runEvent)
        self.buttonRun.pack(side='left')
        self.buttonRun = Button(self.frameButton,width=11,height=1,text='Step Once',command=self.stepOnce)
        self.buttonRun.pack(side='left')
        self.buttonRun = Button(self.frameButton,width=11,height=1,text='Reset',command=self.resetModel)
        self.buttonRun.pack(side='left')

    #model control functions
    def runEvent(self):
        self.running = not self.running
        if self.running:
            self.rootWindow.after(self.timeInterval,self.stepModel)
            self.runPauseString.set("Pause")
        else:
            self.runPauseString.set("Run")

    def stepModel(self):
        if self.running:
            self.modelStepFunc()
            self.drawModel()
            self.rootWindow.after(self.timeInterval,self.stepModel)

    def stepOnce(self):
        self.running = False
        self.runPauseString.set("Run")
        self.modelStepFunc()
        self.drawModel()

    def resetModel(self):
        self.running = False
        self.runPauseString.set("Run")
        self.modelInitFunc()
        self.drawModel()
  
    def drawModel(self):
        if self.modelFigure == None or self.modelFigure.canvas.manager.window == None:
            self.modelFigure = PL.figure()
            PL.ion()
        self.modelDrawFunc()
        self.modelFigure.canvas.manager.window.update()        
    
    def start(self,func=[]):
        if len(func)==3:
            self.modelInitFunc = func[0]
            self.modelDrawFunc = func[1]
            self.modelStepFunc = func[2]
            self.modelInitFunc()
            self.drawModel()
        self.rootWindow.mainloop()
    
    def quitGUI(self):
        PL.close('all')
        self.rootWindow.quit()
        self.rootWindow.destroy()
