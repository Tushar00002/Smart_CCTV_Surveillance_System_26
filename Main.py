import tkinter
from tkinter import *
import customtkinter as ctk
from PIL import ImageTk ,Image
import cv2
from faceDetection import face, faceCounter
from fireDetection import fire
from motionAlert import motionDetector
from weaponDetection import weapon
from accidentDetection import accident
from faceRecognition import recognize
import flags

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("green")

app1 = ctk.CTk()  #creating cutstom tkinter window
app1.geometry("600x440")
app1.title('Login')

def main_page():
    name = entry1.get()      # Get the email and password entered by the user
    email = entry2.get()
    flags.name = name       # Update the email and password variables in flags.py
    flags.email = email

    app1.destroy()            # destroy current window and creating new one 
    window = ctk.CTk()
    window.geometry("1280x720")
    window.title("Smart CCTV")
    app = Frame(window)
    app.grid()
    lmain = Label(app)
    lmain.grid()
    info_label = Label(window, text="Activity", font=("Georgia", 15), bg="#262626", fg="white")
    info_label.place(relx=1, rely=0.1, anchor="ne", width=300)

    def update_info_label():
        text = "Welcome\n\n"  
        if flags.prohibited_email:
            text += "Some one is in prohibited area!\n\n"
        if flags.restricted_email:
            text += "Security Breach!!\n\n"
        if flags.fire_email:
            text += "Fire Alert\n\n"
        if flags.accident_email:
            text += "Accident Alert\n\n"
        
        info_label.configure(text=text)
        info_label.after(100, update_info_label)

    def reset_flags():
        flags.prohibited_email = False
        flags.restricted_email = False
        flags.fire_email = False
        flags.accident_email = False
        flags.started = False

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
                if switch_var_4.get() == "on":
                    faceCounter(frame)
                if switch_var_5.get() == "on":
                    motionDetector(frame)
                if switch_var_6.get() == "on":
                    weapon(frame)
                if switch_var_7.get() == "on":
                    accident(frame)
                if switch_var_8.get() == "on":
                    recognize(frame)
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
    switch_var_4 = ctk.StringVar(value="off")
    switch_var_5 = ctk.StringVar(value="off")
    switch_var_6 = ctk.StringVar(value="off")
    switch_var_7 = ctk.StringVar(value="off")
    switch_var_8 = ctk.StringVar(value="off")

    ctk.CTkLabel(animated_panel, text="Select Features").pack(padx=20,pady=20)
    switch_1 = ctk.CTkSwitch(animated_panel, text="Prohibited Mode      ",font=("arial",14), variable=switch_var_1,onvalue="on",offvalue="off")
    switch_1.pack(padx=20,pady=10)
    switch_2 = ctk.CTkSwitch(animated_panel, text="Fire and Smoke      \nDetection",font=("arial",13), variable=switch_var_2,onvalue="on",offvalue="off")
    switch_2.pack(padx=20,pady=10)
    switch_4 = ctk.CTkSwitch(animated_panel, text="Restricted Mode     ",font=("arial",13), variable=switch_var_4,onvalue="on",offvalue="off")
    switch_4.pack(padx=20,pady=10)
    switch_5 = ctk.CTkSwitch(animated_panel, text="Motion Alert           ",font=("arial",13), variable=switch_var_5,onvalue="on",offvalue="off")
    switch_5.pack(padx=20,pady=10)
    switch_6 = ctk.CTkSwitch(animated_panel, text="Weapon Detection   ",font=("arial",13), variable=switch_var_6,onvalue="on",offvalue="off")
    switch_6.pack(padx=20,pady=10)
    switch_7 = ctk.CTkSwitch(animated_panel, text="Car Crash Detection",font=("arial",13), variable=switch_var_7,onvalue="on",offvalue="off")
    switch_7.pack(padx=20,pady=10)
    switch_8 = ctk.CTkSwitch(animated_panel, text="Face Recognition   ",font=("arial",13), variable=switch_var_8,onvalue="on",offvalue="off")
    switch_8.pack(padx=20,pady=10)

    ctk.CTkButton(animated_panel, text="Refresh", command=reset_flags).pack(padx=20,pady=20)

    button_1 = ctk.CTkButton(window, text="Features Tab", width=170,height=33,corner_radius=25,font=("cosmic sans ms",15),fg_color="#2d71bf",hover_color="#48abab",command=animated_panel.animate)
    button_1.place(relx=0.7,rely=0.87,anchor="n")
    btn_start = ctk.CTkButton(window, text="START", width=100,height=33,corner_radius=25,font=("cosmic sans ms",14),fg_color="#2d71bf",hover_color="#48abab", command=streamer.start)
    btn_start.place(relx=0.15,rely=0.87,anchor="n")
    btn_stop = ctk.CTkButton(window, text="STOP", width=100,height=33,corner_radius=25,font=("cosmic sans ms",14),fg_color="#2d71bf",hover_color="#48abab", command=streamer.stop)
    btn_stop.place(relx=0.23,rely=0.87,anchor="n")
    gen_button = ctk.CTkButton(window, text="Generate Report", width=130,height=33,corner_radius=25,font=("cosmic sans ms",14),fg_color="#2d71bf",hover_color="#48abab", command=flags.gen_report)
    gen_button.place(relx=0.42,rely=0.87,anchor="n")

    update_info_label()
    window.mainloop()
    

img1=ImageTk.PhotoImage(Image.open("assets/bg_img/pattern.png"))
img2=ctk.CTkImage(Image.open("./assets/bg_img/Google_Logo.webp").resize((20,20), Image.LANCZOS))
img3=ctk.CTkImage(Image.open("./assets/bg_img/FB_Logo.png").resize((20,20), Image.LANCZOS))

l1=ctk.CTkLabel(master=app1,image=img1)
l1.pack()

frame=ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2=ctk.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
l2.place(x=50, y=45)
l3=ctk.CTkLabel(master=frame, text="Forget password?",font=('Century Gothic',12))
l3.place(x=155,y=195)

entry1=ctk.CTkEntry(master=frame, width=220, placeholder_text='Enter your Name')
entry1.place(x=50, y=110)
entry2=ctk.CTkEntry(master=frame, width=220, placeholder_text='Email')
entry2.place(x=50, y=165)

button1 = ctk.CTkButton(master=frame, width=220, text="Login", command=main_page, corner_radius=6)
button1.place(x=50, y=240)
button2= ctk.CTkButton(master=frame, image=img2, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
button2.place(x=50, y=290)
button3= ctk.CTkButton(master=frame, image=img3, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF')
button3.place(x=170, y=290)

app1.mainloop()
