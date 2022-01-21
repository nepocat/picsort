banner = """
  ____  _                     _   
 |  _ \(_) ___ ___  ___  _ __| |_ 
 | |_) | |/ __/ __|/ _ \| '__| __|
 |  __/| | (__\__ \ (_) | |  | |_ 
 |_|   |_|\___|___/\___/|_|   \__|


                       for Windows
"""
"""
Date: 15.01.2022
Description:
Simple app for sorting holiday pictures the easy way.
    1. Select unsorted folder
    2. Select output folder
    3. Press 'Y'- key for selecting picture. Any other Key will skip the shown picture.
"""

import os
import sys
import glob
import argparse
import ctypes # for screensize
import tkinter as tk

from pathlib import Path
from tkinter import filedialog
from PIL import ImageTk, Image
from shutil import copy2

def select_dir():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory()
    dir_path = Path(dir_path)
    root.destroy()
    return dir_path

class Picsort:

    def __init__(self, unsorted_dir, sorted_dir):
        self.unsorted_dir = unsorted_dir
        self.sorted_dir = sorted_dir
        self.pics = []
        self.screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        self.root = tk.Tk()
        self.root.bind("<KeyPress>", self.key_press)  
        self.root.geometry("{}x{}+0+0".format(self.screensize[0], self.screensize[1]))
        self.root.resizable(width=True, height=True)
        self.selected = False
        self.resize_ratio = 0.75

    # key press event
    def key_press(self, event):
        self.event_action(event)

    def event_action(self, event):
        #print(repr(event))
        if event.char == 'y':
            self.selected = True
        event.widget.quit()

    # resize to screen
    def resize_pic_to_screen(self, picture, screen_width, screen_height, factor):
        if picture.width > screen_width or picture.height > screen_height:
            # only resize image bigger than the screen
            ratio = min(screen_width/picture.width, screen_height/picture.height) * factor
            picture = picture.resize((int(picture.width*ratio), int(picture.height*ratio)))
        return picture

    # main sorting
    def start_sort(self):
        try:
            # find all unsorted pictures
            self.pics = glob.glob(str(self.unsorted_dir) + '/**/*.jpg', recursive = True)
            for i in range(len(self.pics)):
                if(self.selected == True):
                    print("Select Picture: " + self.pics[i-1])
                    copy2(self.pics[i-1], self.sorted_dir)
                    self.selected = False
                x = self.screensize[0]
                y = self.screensize[1]
                picture = Image.open(self.pics[i])
                picture = self.resize_pic_to_screen(picture, x, y, self.resize_ratio)
                tk_picture = ImageTk.PhotoImage(picture)
                image_widget = tk.Label(self.root, image=tk_picture)
                image_widget.place(x=0, y=0, width=int(x/2), height=y)
                if(i < len(self.pics)-1):
                    picture2 = Image.open(self.pics[i+1])
                    picture2 = self.resize_pic_to_screen(picture2, x, y, self.resize_ratio)
                    tk_picture2 = ImageTk.PhotoImage(picture2)
                    image_widget2 = tk.Label(self.root, image=tk_picture2)
                    image_widget2.place(x=x/2, y=0, width=int(x/2), height=y)
                self.root.mainloop()
        except Exception as e :
            print("Exception occured: " + e)
        if self.selected == True:
            # copy last img if true
            copy2(self.pics[-1], self.sorted_dir)


if __name__ == '__main__':

    print(banner)

    parser = argparse.ArgumentParser(description='Sorting pictures from one folder to another.')
    parser.add_argument('-c','--cli_mode', nargs=2 ,help='[sorted_dir] [unsorted_dir]')
    args = parser.parse_args()

    if args.cli_mode:
        unsorted_dir = args.cli_mode[0]
        sorted_dir = args.cli_mode[1]
    else:
        unsorted_dir = select_dir()
        sorted_dir = select_dir()

    if not unsorted_dir or not sorted_dir:
        print("Please provide both directorys!")
        sys.exit(1)
    
    if not os.path.isdir(unsorted_dir) or not os.path.isdir(sorted_dir):
        print("\nError: Specify a directory for each input argument")
        sys.exit(1)
    
    print("1. Unsorted Pictures: " + str(unsorted_dir))
    print("2. Sorted Pictures: " + str(sorted_dir) + "\n\n")

    ps = Picsort(unsorted_dir, sorted_dir)
    ps.start_sort()






    



