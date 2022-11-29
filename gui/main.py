import datetime    
import webbrowser
import tkinter as tk
import PIL.Image
import numpy as np  #pip install numpy
import cv2 as cv    #pip install opencv-python
import pyautogui    #pip install PyAutoGUI
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from loopit import LoopIT
import time

status = ""

def on_closing():
    global running
    running = False
    
######### LoopIT
loopit = LoopIT(host='127.0.0.1', port=1219)
loopit.set_mode(module_name = "fes",
            module_index = "0",
            mode_name = "current_mode")


######### GUI
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)
root.title("LoopIT Interface")
root.geometry("800x800+500+100")
canvas = tk.Canvas(root, bg="#6AB187", height=800, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

img= (Image.open("assets/logo.jpg"))
resized_image= img.resize((150,51), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
canvas.create_image(10,10, anchor=tk.NW, image=new_image)

header = canvas.create_text(400.0, 50.0, text="LoopIT", fill="black", font=("Roboto-Bold", int(30.0)))
info = canvas.create_text(400.0, 650, text="Stimulation Status", fill="black", font=("Roboto-Medium", 20))


######## Parameter controls

amplitude_switch = tk.Scale(from_=0, to=30, orient=tk.HORIZONTAL, length=200, width=30, activebackground="#C25993"
                       , bg="#C25993", highlightcolor="#C25993", highlightbackground="#C25993", fg="white",
                       troughcolor="white")
amplitude_label = canvas.create_text(270, 175, text="Amplitude (0-30 mA)", fill="black", font=("Roboto-Bold", 16))

pw_text = tk.Text(root, height = 1, width = 5, font=("Roboto", 16))
pw_label = canvas.create_text(235, 275, text="Pulse width (microseconds)", fill="black", font=("Roboto-Bold", 16))

ipi_text = tk.Text(root, height = 1, width = 5, font=("Roboto", 16))
ipi_label = canvas.create_text(295, 375, text="Frequency (Hz)", fill="black", font=("Roboto-Bold", 16))


######## Buttons
    
def send_to_loopit_callback():
    # read the text boxes
    try:
        amp = float(amplitude_switch.get())
        pw = float(pw_text.get("1.0", tk.END))
        ipi = float(ipi_text.get("1.0", tk.END))
        
        # convert amplitude from milliamps to 0.0000010 A
        converted_amp = amp * 30000000
        # convert pulse width from microseconds to nanoseconds
        converted_pw = pw * 1000
        # convert inter pulse interval from Hz to nanoseconds
        converted_ipi = 1/ipi * 10**9 # formaula for Hz to nanosecond period is 1/Hz * 10**9
        
        # set loopit variables
        loopit.amplitude_A = str(converted_amp)
        loopit.amplitude_B = str(-converted_amp)
        loopit.pulsewidth_A = str(converted_pw)
        loopit.pulsewidth_B = str(converted_pw)
        loopit.inter_pulse_interval = str(converted_ipi)
    
        send.configure(fg="black", activeforeground="black", text="Send to LoopIT")
    except: # warn the user
        send.configure(fg="red", activeforeground="red", text="Please set parameters")
        
def start_stimulation_callback():
    status_stimulation("on")
    loopit.start_stimulation()

def stop_stimulation_callback():
    status_stimulation("off")
    loopit.stop_stimulation()
    
def status_stimulation(msg):
    global status
    status = msg
    if status == "off":
        start["state"] = "normal"
        stop["state"] = "disabled"
        canvas.itemconfig(info, text="STIM OFF", fill="white")
        
    elif status == "on":
        stop["state"] = "normal"
        start["state"] = "disabled"
        canvas.itemconfig(info, text="STIM ON", fill="red", font=('Roboto-Bold', -50))

send = tk.Button(text="Send to LoopIT", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", height=5, width=20, command=send_to_loopit_callback)
start = tk.Button(text="START", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", height=5, width=20, command=start_stimulation_callback)
stop = tk.Button(text="STOP", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", height=5, width=20, command=stop_stimulation_callback)
# initialize stop as disabled
stop["state"] = "disabled"

######## Event loop

amplitude_switch.place(x=500, y=175, anchor=tk.CENTER)
pw_text.place(x=425, y=275, anchor=tk.CENTER)
ipi_text.place(x=425, y=375, anchor=tk.CENTER)
send.place(x=400, y=500, anchor=tk.CENTER)

start.place(x=218, y=675, width=172, height=58)
stop.place(x=418, y=675, width=172, height=58)

quit = tk.Button(root, text="Exit", font=("Roboto-Bold", 14), borderwidth=3, highlightthickness=0, relief="raised", height=3, width=5, command=root.destroy)
quit.place(x=700, y=20)
root.mainloop()
# running = True
# while running:
#     root.update()