import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ctypes, sys
import configparser

config_file = os.environ['LOCALAPPDATA'] + '\\photoshop.ini'

config = configparser.ConfigParser()
if (os.path.isfile(config_file)):
    config.read(config_file)
    default_path = config['DEFAULT']['default_path']
else:
    # lets create that config file for next time...
    cfgfile = open(config_file,'w')
    config['DEFAULT']['default_path'] = os.environ["PROGRAMW6432"] + "\\Adobe\\Adobe Photoshop CC 2018"
    config.write(cfgfile)
    cfgfile.close()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def askPath():
    MsgBox = tk.messagebox.askyesno('Default path changed','The default installation path could not be found \nWould you like to search the "Adobe Photoshop CC 2018" folder yourself?',icon = 'error')
    if MsgBox:
        rootk.path = filedialog.askdirectory()
        return rootk.path
    else:
        root.destroy()
        exit()

if is_admin():
    # Check if default path exists else ask user to specify it
    if os.path.isdir(default_path):
        path = default_path
    else:
        rootk = tk.Tk()
        rootk.withdraw()
        path = askPath()

    # Path to application.xml
    file = path + "\\AMT\\application.xml"

    # Check if path is correct and file exists
    if not (os.path.isfile(file)):
        tk.messagebox.showerror('Error!','Folder is not correct or file does not exist! \nPlease make sure inside the selected folder is a folder called "AMT"')
        exit()
    else:
        cfgfile = open(config_file,'w')
        config['DEFAULT']['default_path'] = path
        config.write(cfgfile)
        cfgfile.close()

    # Open original file
    tree = ET.parse(file)
    root = tree.getroot()

    elem = root.findall(".//*[@key='TrialSerialNumber']")
    TrialSerialNumber = elem[0].text
    elem[0].text = str(int(TrialSerialNumber) + 10)

    # Write back to file
    tree.write(file)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
