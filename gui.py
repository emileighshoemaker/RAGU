"""
NOSEpick - currently in development stages
created by: Brandon S. Tober and Michael S. Christoffersen
date: 25JUN19
last updated: 09SEP2019
environment requirements in nose_env.yml
"""

### IMPORTS ###
# import ingester
import utils
import imPick
import basemap
from tools import *
import os, sys, scipy
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import gdal, osr
import tkinter as tk
from tkinter import Button, Frame, messagebox, Canvas, filedialog, Menu, Radiobutton


class MainGUI(tk.Tk):
    # class to setup and hold gui attributes
    def __init__(self, master, in_path, map_path):
        self.master = master
        # self.master.protocol("WM_DELETE_WINDOW", imPick.imPick.close_window)
        self.in_path = in_path
        self.map_path = map_path
        self.setup()


    def setup(self):
        # file menu
        menubar = Menu(self.master)

        # create individual menu bars
        fileMenu = Menu(menubar, tearoff=0)
        pickMenu = Menu(menubar, tearoff=0)
        viewMenu = Menu(menubar, tearoff=0)
        mapMenu = Menu(menubar, tearoff=0)
        helpMenu = Menu(menubar, tearoff=0)

        # file menu items
        fileMenu.add_command(label="Open    [Ctrl+O]", command=self.open_loc)
        fileMenu.add_command(label="Save    [Ctrl+S", command=self.save_loc)
        fileMenu.add_command(label="Next    [>]", command=self.next_loc)
        fileMenu.add_command(label="Exit    [Escape]", command=self.close_window)

        # pick menu items
        pickMenu.add_command(label="New")
        pickMenu.add_command(label="Save")
        pickMenu.add_separator()
        pickMenu.add_command(label="Optimize")

        # view menu items
        self.im_status = tk.StringVar()
        viewMenu.add_radiobutton(label="Radargram", variable=self.im_status, value="data",command=imPick.imPick.show_radar)
        viewMenu.add_radiobutton(label="Cluttergram", variable=self.im_status, value="clut",command=imPick.imPick.show_clutter)
        viewMenu.add_separator()
        viewMenu.add_command(label="Trace-View")

        # map menu items
        mapMenu.add_command(label="Open    [Ctrl+M]", command=self.map_loc)

        # help menu items
        helpMenu.add_command(label="Instructions", command=self.help)

        # add menu items to menubar
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Pick", menu=pickMenu)
        menubar.add_cascade(label="View", menu=viewMenu)
        menubar.add_cascade(label="Map", menu=mapMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)
        
        # add the menubar to the window
        self.master.config(menu=menubar)


        # build data display frame
        self.display = tk.Frame(self.master)
        self.display.pack(side="bottom", fill="both", expand=1)

        
        # add radio buttons for toggling between radargram and clutter-sim
        radarRad = Radiobutton(self.master, text="Radar", variable=self.im_status, value="data",command=imPick.imPick.show_radar).pack(side="left")
        clutterRad = Radiobutton(self.master,text="Clutter", variable=self.im_status, value="clut",command=imPick.imPick.show_clutter).pack(side="left")  
        self.im_status.set("data")


        # bind keypress events
        self.master.bind("<Key>", self.key)   

        # call the instructions
        # self.help()  

    

        # button for loading data

    #     self.openButton = Button(self.master, text = "Open", command = utils.open)
    #     self.opneButton.pack(in_=self.controls, side="left")
    #     # button for going to next data file
    #     self.nextButton = Button(self.master, text = "Next", command = utils.next_file)
    #     self.nextButton.pack(in_=self.controls, side="left")
    #     # button for saving
    #     self.saveButton = Button(text = "Save", command = utils.savePick)
    #     self.saveButton.pack(in_=self.controls, side="left")
    #     # button for basemap display
    #     self.basemapButton = Button(text = "Map", command = basemap.basemap)
    #     self.basemapButton.pack(in_=self.controls, side="left")
    #     # button for help message
    #     self.instButton = Button(self.master, text = "Help", command = utils.help)
    #     self.instButton.pack(in_=self.controls, side="left")
    #     # button for exit
    #     self.exitButton = Button(text = "Exit", fg = "red", command = self.close_window)
    #     self.exitButton.pack(in_=self.controls, side="left")
    #     # button for picking initiation
    #     self.pickButton = Button(text = "Pick", fg = "green", command = imPick.imPick.picking)
    #     self.pickButton.pack(in_=self.pickControls, side="left")
    #     # button for trace view
    #     self.traceButton = Button(text = "Trace View", command = None)
    #     self.traceButton.pack(in_=self.pickControls, side="left")
    #     # button for pick optimization
    #     self.pickOptButton = Button(text = "Pick Optimization", command = None)
    #     self.pickOptButton.pack(in_=self.pickControls, side="left")
    #     # button to toggle on radargram
    #     self.radarButton = Button(text = "radar", command = imPick.imPick.show_radar, relief="sunken")
    #     self.radarButton.pack(in_=self.switchIm, side="left")        
    #     # button to toggle on clutter
    #     self.clutterButton = Button(text = "clutter", command = imPick.imPick.show_clutter)
    #     self.clutterButton.pack(in_=self.switchIm, side="left")        
    #     # call information messageboxs
    #     # utils.help()
    #     # register click and key events

        self.f_loadName = ""
        self.f_saveName = ""
        self.map_loadName = ""
    #     self.dtype = "amp"
    #     self.var_reset()
    #     utils.open()
    
    
    # def var_reset(self):
    #     # variable declarations
    #     self.pick_state = 0
    #     self.pick_layer = 0
    #     self.basemap_state = 0
    #     self.pick_dict = {}
    #     self.pick_idx = []
    #     self.toolbar = None
    #     self.pick_loc = None
    #     self.data_cmin = None
    #     self.data_cmax = None
    #     self.clut_cmin = None
    #     self.clut_cmax = None
    #     self.map_loadName = ""
    #     self.f_saveName = ""
    #     self.data_imSwitch_flag = ""
    #     self.clut_imSwitch_flag = ""

    def key(self,event):
        # keypress event
        if event.state & 4 and event.keysym == "o":
            # ctrl+o open file
            self.open_loc()

        elif event.state & 4 and event.keysym == "s":
            # ctrl+s save picks
            self.save_loc()

        elif event.state & 4 and event.keysym == "m":
            # ctrl+m open map
            self.map_loc()

        elif event.state & 1 and event.keysym == "greater":
            # shift+. (>) next file
            self.next_loc()

        elif event.keysym == "Escape" or event.keysym == "escape":
            self.close_window()

            
    def close_window(self):
        # destroy canvas
        # first check if picks have been made and saved
        # if len(self.xln) > 0 and self.f_saveName == "":
        #     if messagebox.askokcancel("Warning", "Exit NOSEpick without saving picks?", icon = "warning") == True:
        #         self.master.destroy()
        # else:
        #     self.master.destroy()
        self.master.destroy()


    def open_loc(self):
        # open location
        # bring up dialog box for user to load data file
        self.f_loadName = filedialog.askopenfilename(initialdir = self.in_path,title = "Select file",filetypes = (("mat files","*.mat"),("all files","*.*")))
        if self.f_loadName:
            imPick.imPick(self.master, self.display, self.f_loadName)


    def save_loc(self):
        # get desired save location for pick data
        self.f_saveName = filedialog.asksaveasfilename(initialdir = self.in_path,title = "Save As",filetypes = (("comma-separated values","*.csv"),))
    
    
    def map_loc(self):
        # get desired basemap location
        if self.f_loadName:
            self.map_loadName = filedialog.askopenfilename(initialdir = self.map_path, title = "Select file", filetypes = (("GeoTIFF files","*.tif"),("all files","*.*")))
            
        if self.map_loadName:
            basemap.basemap(self.master, self.map_loadName)

    def next_loc(self):
        # get filename for next file in directory, if one exists
        if self.f_loadName:
            # get index of crurrently displayed file in directory
            file_path = self.f_loadName.rstrip(self.f_loadName.split("/")[-1])
            file_list = os.listdir(file_path)
            file_list.sort()
            for _i in range(len(file_list)):
                if file_list[_i] == self.f_loadName.split("/")[-1]:
                    file_index = _i
            # add one to index to load next file
            file_index += 1

            # check if more files exist in directory following current file
            if file_index <= (len(file_list) - 1):
                self.f_loadName = (file_path + file_list[file_index])
                # del xln[:]
                # del yln[:]
                # del xln_old[:]
                # del yln_old[:]
                
                imPick.imPick.load(self.f_loadName)

            else:
                print("Note: " + self.f_loadName.split("/")[-1] + " is the last file in " + file_path)


    def help(self):
        # help message box
        messagebox.showinfo("NOSEpick Instructions",
        """Nearly Optimal Subsurface Extractor:
        \n\n1. Load button to open radargram
        \n2. Click along reflector surface to pick
        \n\t\u2022<backspace> to remove the last
        \n\t\u2022<c> to remove all
        \n3. Radar and clutter buttons to toggle
        \n4. Next button to load next file
        \n5. Save button to export picks
        \n6. Map button to display basemap
        \n7. Exit button to close application""")
        
        # dialogbox = tk.Toplevel(self.master)
        # dialogbox.title("NOSEpick Instructions")


        # T = tk.Text(dialogbox)
        # T.image_create(tk.END, image=photo)
        # message =  """Nearly Optimal Subsurface Extractor:
        # \n\n1. Load button to open radargram
        # \n2. Click along reflector surface to pick
        # \n\t\u2022<backspace> to remove the last
        # \n\t\u2022<c> to remove all
        # \n3. Radar and clutter buttons to toggle
        # \n4. Next button to load next file
        # \n5. Save button to export picks
        # \n6. Map button to display basemap
        # \n7. Exit button to close application"""
        # T.insert(tk.END, message)
        # T.pack(expand=True, fill="both")

        # close_button = tk.Button(dialogbox,text="Ok", 
        #                         command=dialogbox.destroy)
        # close_button.pack(side="bottom")

    
