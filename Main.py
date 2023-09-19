from tkinter import *
import customtkinter as ctk
from PIL import ImageTk ,Image
import cv2
from faceDetection import face, faceCounter
from fireDetection import fire
from smokeDetection import smoke
from record import record

window = ctk.CTk()
window.geometry("1280x720")
window.title("Smart CCTV")
app = Frame(window)
app.grid()
lmain = Label(app)
lmain.grid()

class SlidePanel(ctk.CTkFrame):
    def __init__(self,parent,start_pos,end_pos):
        super().__init__(master = parent)

        self.start_pos = start_pos +0.04
        self.end_pos = end_pos -0.02
        self.width = abs(start_pos - end_pos)

        self.pos = self.start_pos
        self.in_start_pos = True
        self.place(relx=self.start_pos,rely=0.05,relwidth=self.width,relheight=0.9)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backward()
    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos,rely=0.05,relwidth=self.width,relheight=0.9)
            self.after(10,self.animate_forward)
        else:
            self.in_start_pos = False
    def animate_backward(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos,rely=0.05,relwidth=self.width,relheight=0.9)
            self.after(10,self.animate_backward)
        else:
            self.in_start_pos = True

cap = cv2.VideoCapture(0)

width, height = 1300, 620
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

class streamer:
    is_running = False

    def video_stream():
        ret, frame = cap.read()
        if is_running and ret:
            if switch_var_1.get() == "on":
                face(frame)
            if switch_var_2.get() == "on":
                fire(frame)
            if switch_var_3.get() == "on":
                smoke(frame)
            if switch_var_4.get() == "on":
                faceCounter(frame)
            if switch_var_5.get() == "on":
                 record(frame)
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            lmain.photo = photo
            lmain.configure(image=photo)
            lmain.after(10, streamer.video_stream)
    def start():
        global is_running
        is_running = True
        streamer.video_stream()
    def stop():
        global is_running
        is_running = False
        streamer.video_stream()

animated_panel = SlidePanel(window, 1.0, 0.85)
switch_var_1 = ctk.StringVar(value="off")
switch_var_2 = ctk.StringVar(value="off")
switch_var_3 = ctk.StringVar(value="off")
switch_var_4 = ctk.StringVar(value="off")
switch_var_5 = ctk.StringVar(value="off")


ctk.CTkLabel(animated_panel, text="Select Features").pack(padx=20,pady=20)
switch_1 = ctk.CTkSwitch(animated_panel, text="Face Detection", variable=switch_var_1,onvalue="on",offvalue="off")
switch_1.pack(padx=20,pady=10)
switch_2 = ctk.CTkSwitch(animated_panel, text="Fire Detection", variable=switch_var_2,onvalue="on",offvalue="off")
switch_2.pack(padx=20,pady=10)
switch_3 = ctk.CTkSwitch(animated_panel, text="Smoke Detection", variable=switch_var_3,onvalue="on",offvalue="off")
switch_3.pack(padx=20,pady=10)
switch_4 = ctk.CTkSwitch(animated_panel, text="People Counter", variable=switch_var_3,onvalue="on",offvalue="off")
switch_4.pack(padx=20,pady=10)
switch_5 = ctk.CTkSwitch(animated_panel, text="Recorder", variable=switch_var_5,onvalue="on",offvalue="off")
switch_5.pack(padx=20,pady=10)
    
ctk.CTkButton(animated_panel, text="Button").pack(expand=True,fill="both",pady=10)

button_1 = ctk.CTkButton(window, text="Features Tab",command=animated_panel.animate)
button_1.place(relx=0.6,rely=0.9,anchor="n")

btn_start = ctk.CTkButton(window, text="Start", width=10, command=streamer.start)
btn_start.place(relx=0.2,rely=0.9,anchor="n")
btn_stop = ctk.CTkButton(window, text="Stop", width=10, command=streamer.stop)
btn_stop.place(relx=0.4,rely=0.9,anchor="n")
 
window.mainloop()
