import tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from loopit import LoopIT
import os

def on_closing():
    global running
    running = False

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # setup canvas
        self.canvas = tk.Canvas(self, bg="#4f966d", height=800, width=800, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # window
        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.resizable(False, False)
        self.title("LoopIT Interface")
        self.geometry("800x800+500+100")
        
        # logo
        self.img = Image.open(os.path.join(os.path.dirname(__file__), "logo.jpg"))
        self.resized_image = self.img.resize((150,51), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)
        self.logo_button = tk.Button(self, image=self.new_image, borderwidth=0, highlightthickness=0,
                        command=self.easter_egg)

        # parameter inputs
        self.amplitude_switch = tk.Scale(from_=0, to=30, orient=tk.HORIZONTAL, length=200, width=30, activebackground="#C25993", 
                        bg="#C25993", highlightcolor="#C25993", highlightbackground="#C25993", fg="white", troughcolor="white")
        self.pw_text = tk.Text(self, height = 1, width = 5, font=("Roboto", 16))
        self.ipi_text = tk.Text(self, height = 1, width = 5, font=("Roboto", 16))

        # buttons
        self.send = tk.Button(text="Send to LoopIT", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=3, width=15, command=self.send_to_loopit_callback)
        self.start = tk.Button(text="START", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=5, width=20, command=self.start_stimulation_callback)
        self.stop = tk.Button(text="STOP", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=5, width=20, command=self.stop_stimulation_callback)
        # initialize stop as disabled
        self.stop["state"] = "disabled"
        self.quit = tk.Button(self, text="Exit", font=("Roboto-Bold", 14), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=2, width=5, command=self.destroy)
        self.quit.place(x=720, y=6)

        # placement
        # logo and titles
        self.logo_button.place(relx=0.1, rely=0.04, anchor=tk.CENTER)
        self.header = self.canvas.create_text(400.0, 50.0, text="LoopIT", fill="white", font=("Roboto-Bold", 30))
        self.connection = self.canvas.create_text(400.0, 85.0, text="", fill="white", font=("Roboto-Bold", 14))
        self.info = self.canvas.create_text(400.0, 650, text="Stimulation Status", fill="white", font=("Roboto-Medium", 20))

        # parameter labels
        self.ipi_label = self.canvas.create_text(295, 375, text="Frequency (Hz)", fill="white", font=("Roboto-Bold", 16))
        self.pw_label = self.canvas.create_text(235, 275, text="Pulse width (microseconds)", fill="white", font=("Roboto-Bold", 16))
        self.amplitude_label = self.canvas.create_text(270, 175, text="Amplitude (0-30 mA)", fill="white", font=("Roboto-Bold", 16))

        # parameter inputs
        self.amplitude_switch.place(x=500, y=175, anchor=tk.CENTER)
        self.pw_text.place(x=425, y=275, anchor=tk.CENTER)
        self.ipi_text.place(x=425, y=375, anchor=tk.CENTER)
        self.send.place(x=400, y=500, anchor=tk.CENTER)

        # stim controls
        self.start.place(x=218, y=675, width=172, height=58)
        self.stop.place(x=418, y=675, width=172, height=58)

        # attempt connection to a LoopIT
        self.connect_to_loopit()
        
    def connect_to_loopit(self):
        # try to connect or warn the user to restart
        try:
            self.loopit = LoopIT(host='127.0.0.1', port=1219)
            self.loopit.set_mode(module_name = "fes",
                        module_index = "0",
                        mode_name = "current_mode")
        except:
            self.loopit = None
            self.canvas.itemconfig(self.connection, text="Device not found, please connect and restart application", fill="maroon", font=("Roboto-Bold", 18))


    def easter_egg(self):
        self.title("Be kind, lend a Helping Hand")

    def check_connection_status(self):
        # check for the device
        try:
            self.loopit.query()
            self.canvas.itemconfig(self.connection, text="Device connected", fill="#005208", font=("Roboto-Bold", 24))
            return True
        except:
            self.canvas.itemconfig(self.connection, text="Device not connected", fill="maroon", font=("Roboto-Bold", 24))
            return False

    def send_to_loopit_callback(self):
        result = self.check_connection_status()
        if result:
            # read the text boxes
            try:
                amp = float(self.amplitude_switch.get())
                pw = float(self.pw_text.get("1.0", tk.END))
                ipi = float(self.ipi_text.get("1.0", tk.END))
                
                # convert amplitude from milliamps to 0.0000010 A
                converted_amp = amp * 30000000
                # convert pulse width from microseconds to nanoseconds
                converted_pw = pw * 1000
                # convert inter pulse interval from Hz to nanoseconds
                converted_ipi = 1/ipi * 10**9 # formaula for Hz to nanosecond period is 1/Hz * 10**9
                
                # set loopit variables
                self.loopit.amplitude_A = str(converted_amp)
                self.loopit.amplitude_B = str(-converted_amp)
                self.loopit.pulsewidth_A = str(converted_pw)
                self.loopit.pulsewidth_B = str(converted_pw)
                self.loopit.inter_pulse_interval = str(converted_ipi)

                # flash a status message
                self.send.configure(fg="green", activeforeground="green", text="Parameters sent!")
                self.send.after(2000, lambda: self.send.config(fg="black", activeforeground="black", text="Send to LoopIT"))
            except: # warn the user
                self.send.configure(fg="red", activeforeground="red", text="Please set parameters")
            
    def start_stimulation_callback(self):
        result = self.check_connection_status()
        if result:
            self.status_stimulation("on")
            self.loopit.start_stimulation()

    def stop_stimulation_callback(self):
        result = self.check_connection_status()
        if result:    
            self.status_stimulation("off")
            self.loopit.stop_stimulation()
        
    def status_stimulation(self, msg):
        global status
        status = msg
        if status == "off":
            self.start["state"] = "normal"
            self.stop["state"] = "disabled"
            self.canvas.itemconfig(self.info, text="STIM OFF", fill="white")
            
        elif status == "on":
            self.stop["state"] = "normal"
            self.start["state"] = "disabled"
            self.canvas.itemconfig(self.info, text="STIM ON", fill="red", font=('Roboto-Bold', -50))


def main():
    app = MainApplication()
    app.mainloop()

