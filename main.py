from tkinter import *
from tkinter import ttk
import serial.tools.list_ports as port_list
import subprocess
import random
import sys
import time
import ctypes
import os
import signal
import psutil


root = Tk()
root.title("Custom simracing driver")

ports = list(port_list.comports())
portsNames = ports
cnames = StringVar(value=portsNames)

games = { 'project_car_2':'Project car 2', 'dirt_rally':'Dirt Rally'}
drivers = {'project_car_2':'driver_pc2.py', 'dirt_rally':'driver_dirt_rally.py'}

# State variables
game = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def showComPorts(*args):
    ports = list(port_list.comports())
    portsNames = ports
    cnames = StringVar(value=portsNames)
    lbox.config(listvariable = cnames)
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        name = portsNames[idx]
        statusmsg.set("Port sélectionné : %s" % (name))
    sentmsg.set('')


statusDriver = 0
def startDriver(*args):
    global statusDriver
    global process
    if statusDriver == 0:
        if (str(portsNames[lbox.curselection()[0]]).find('Arduino') != -1): 
            print("Arduino ok, driver : ", drivers[game.get()])
            
            statusDriver = 1
            lbox.config(state = DISABLED)
            process = subprocess.Popen("python3 "+str(drivers[game.get()]), shell=True)

            for radio_button in radio_buttons:
                radio_button.configure(state = DISABLED)
            send.config(text="Arrêter le driver")
        else:
            Mbox('Erreur', 'Le port COM choisi ne correspond pas à un adaptateur arduino "Custom Simracing", veuillez choisir un autre port COM.', 0)
    else:
        statusDriver = 0
        pobj = psutil.Process(process.pid)
        for c in pobj.children(recursive=True):
            c.kill()
        pobj.kill()
        lbox.config(state = NORMAL)
        for radio_button in radio_buttons:
            radio_button.configure(state = NORMAL)
        send.config(text="Lancer le driver")

c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

lbox = Listbox(c, listvariable=cnames, height=5, width=70)

lbl = ttk.Label(c, text="Profil de jeu :")
g1 = ttk.Radiobutton(c, text=games['project_car_2'], variable=game, value='project_car_2')
g2 = ttk.Radiobutton(c, text=games['dirt_rally'], variable=game, value='dirt_rally')
radio_buttons = [g1,g2]
send = ttk.Button(c, text='Lancer le driver', command=startDriver, default='active')

sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
send.grid(column=2, row=4, sticky=E)
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=6, columnspan=2, sticky=(W,E))
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)


lbox.bind('<<ListboxSelect>>', showComPorts)
lbox.bind('<Double-1>', startDriver)
root.bind('<Return>', startDriver)

for i in range(0,len(portsNames),2):
    lbox.itemconfigure(i, background='#f0f0ff')

game.set('project_car_2')
sentmsg.set('')

statusmsg.set('')
lbox.selection_set(0)
showComPorts()

def on_closing():
    pobj = psutil.Process(process.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# root.mainloop()
while(1):
    root.update_idletasks()
    root.update()
    showComPorts()
    time.sleep(0.05)
    