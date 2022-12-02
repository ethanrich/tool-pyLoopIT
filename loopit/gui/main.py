import tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from loopit import LoopIT
import os

def on_closing():
    global running
    running = False

class LoopITInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # component sizing parameters
        window_dims = (800, 500)
        logo_dims = (112,37)
        logo_loc = (0.08, 0.05)
        
        fes_module_dims = (200, 700)
        fes_module_loc = (0.45, 0.42)
        fes_module_label_loc = (0.145, 0.22)
        
        amp_switch_dims = (200, 30) # l, w
        pw_text_dims = (1, 5)
        ipi_text_dims = (1, 5)
        
        ipi_label_loc = (295, 375)
        pw_label_loc = (235, 275)
        amplitude_label_loc = (270, 175)
        
        send_dims = (3, 18)
        send_loc = (0.8, 0.4)
        
        start_dims = (3, 10)
        start_loc = (0.4, 0.85)
        
        stop_dims = (3, 10)
        stop_loc = (0.6, 0.85)
        
        quit_dims = (2, 5)
        quit_loc = (0.94, 0.06)
        
        header_loc = (0.4, 0.02)
        connect_loc = (400, 85)
        stim_status_loc = (400, 650)
        
        # colors
        self.background_color = "#145460"
        self.title_color = "#F6EBCD"
        self.connected_color = "#5D9E7E"
        self.text_color = "black"
        self.warning = "#D15252"
        self.fes_module_color = "#E8C492"

        # background
        self.configure(bg=self.background_color)

        # window
        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.resizable(False, False)
        self.title("LoopIT Interface")
        self.geometry("{0}x{1}+500+100".format(window_dims[0], window_dims[1]))
        
        # logo
        self.img = Image.open(os.path.join(os.path.dirname(__file__), "logo.jpg"))
        self.resized_image = self.img.resize(logo_dims, Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resized_image)
        self.logo_button = tk.Button(self, image=self.new_image, borderwidth=0, highlightthickness=0,
                        command=self.easter_egg)
        self.logo_button.place(relx=logo_loc[0], rely=logo_loc[1], anchor=tk.CENTER)
        
        # module section
        self.fes_module = tk.Frame(self, height=fes_module_dims[0], width=fes_module_dims[1], bg=self.fes_module_color, relief="raised", highlightthickness=5, highlightcolor="#a2c4c9")
        self.fes_module.place(relx=fes_module_loc[0], rely=fes_module_loc[1], anchor=tk.CENTER)
        
        self.fes_label = tk.Label(self, text="FES Module", bg=self.fes_module_color, fg=self.text_color, font=("Roboto-Bold", 22),
                                  relief="raised", highlightthickness=5, highlightcolor="#a2c4c9")
        self.fes_label.place(relx=fes_module_label_loc[0], rely=fes_module_label_loc[1], anchor=tk.CENTER)

        # buttons
        # send
        self.send = tk.Button(text="Send to LoopIT", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=send_dims[0], width=send_dims[1], command=self.send_to_loopit_callback)
        self.send.place(relx=send_loc[0], rely=send_loc[1], anchor=tk.CENTER)
        # start  
        self.start = tk.Button(text="START", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=start_dims[0], width=start_dims[1], command=self.start_stimulation_callback)
        self.start.place(relx=start_loc[0], rely=start_loc[1], anchor=tk.CENTER)
        # stop
        self.stop = tk.Button(text="STOP", font=("Roboto-Bold", 16), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=stop_dims[0], width=stop_dims[1], command=self.stop_stimulation_callback)
        self.stop.place(relx=stop_loc[0], rely=stop_loc[1], anchor=tk.CENTER)
        # initializ)
        self.stop["state"] = "disabled"
        
        self.quit = tk.Button(self, text="Exit", font=("Roboto-Bold", 14), borderwidth=3, highlightthickness=0, relief="raised", 
                                height=quit_dims[0], width=quit_dims[1], command=self.destroy)
        self.quit.place(relx=quit_loc[0], rely=quit_loc[1], anchor=tk.CENTER)

        # placement
        # logo and titles
        self.header = tk.Label(self, text="LoopIT", bg=self.background_color, fg=self.title_color, font=("Roboto-Bold", 30))
        self.header.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        self.connection = tk.Label(self, text="", bg=self.background_color, fg=self.text_color, font=("Roboto-Bold", 14))
        self.connection.place(relx=0.5, rely=0.13, anchor=tk.CENTER)

        self.stim_status = tk.Label(self, text="Stimulation Status", bg=self.background_color, fg=self.title_color, font=("Roboto-Medium", 20))
        self.stim_status.place(relx=0.5, rely=0.7, anchor=tk.CENTER)


        # parameter labels and inputs
        # inputs
        self.amplitude_switch = tk.Scale(from_= 0, to=30, orient=tk.HORIZONTAL, length=200, width=30, activebackground="#a2c4c9", 
                        bg="#a2c4c9", highlightcolor="#a2c4c9", highlightbackground="#a2c4c9", fg="black", troughcolor="white", font=("Roboto-Bold", 12))
        self.amplitude_switch.place(relx=0.49, rely=0.32, anchor=tk.CENTER)
        
        self.ipi_text = tk.Text(self, height = 1, width = 15, font=("Roboto", 16))
        self.ipi_text.place(relx=0.465, rely=0.45, anchor=tk.CENTER)        
        
        self.pw_text = tk.Text(self, height = 1, width = 15, font=("Roboto", 16))
        self.pw_text.place(relx=0.465, rely=0.55, anchor=tk.CENTER)
                
        # labels
        self.amplitude_label = tk.Label(self, text="Amplitude (0-30 mA)", bg=self.fes_module_color, fg=self.text_color, font=("Roboto-Bold", 16))
        self.amplitude_label.place(relx=0.15, rely=0.32, anchor=tk.CENTER)   
        
        self.ipi_label = tk.Label(self, text="Frequency (Hz)", bg=self.fes_module_color, fg=self.text_color, font=("Roboto-Bold", 16))
        self.ipi_label.place(relx=0.15, rely=0.45, anchor=tk.CENTER)
        
        self.pw_label = tk.Label(self, text="Pulse width (μs)", bg=self.fes_module_color, fg=self.text_color, font=("Roboto-Bold", 16))
        self.pw_label.place(relx=0.15, rely=0.55, anchor=tk.CENTER)

        # attempt connection to a LoopIT
        self.connect_to_loopit()
        
    def connect_to_loopit(self):
        # try to connect or warn the user to restart
        try:
            self.loopit = LoopIT(host='127.0.0.1', port=1219)
            self.loopit.set_mode(module_name = "fes",
                        module_index = "0",
                        mode_name = "current_mode")
            self.connection.config(text="Device connected", fg=self.connected_color, font=("Roboto-Bold", 24))
        except:
            self.loopit = None
            self.connection.config(text="Device not found, please connect and restart application", fg=self.warning, font=("Roboto-Bold", 18))


    def easter_egg(self):
        self.title("Be kind, lend a Helping Hand")

    def check_connection_status(self):
        # check for the device
        try:
            self.loopit.query()
            self.connection.config(text="Device connected", fg=self.connected_color, font=("Roboto-Bold", 24))
            return True
        except:
            self.connection.config(text="Device not found, please connect and restart application", fg=self.warning, font=("Roboto-Bold", 18))
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
                self.send.configure(fg=self.warning, activeforeground=self.warning, text="Set parameters")
            
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
            self.stim_status.config(text="STIM OFF", fg="white")
            
        elif status == "on":
            self.stop["state"] = "normal"
            self.start["state"] = "disabled"
            self.stim_status.config(text="STIM ON", fg=self.warning, font=('Roboto-Bold', -50))


def main():
    app = LoopITInterface()
    app.mainloop()

