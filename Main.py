import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from faceDetection import face

class SlidePanel(ctk.CTkFrame):
    def __init__(self,parent,start_pos,end_pos):
        super().__init__(master = parent)

        self.start_pos = start_pos +0.05
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
            self.pos -= 0.01
            self.place(relx=self.pos,rely=0.05,relwidth=self.width,relheight=0.9)
            self.after(10,self.animate_forward)
        else:
            self.in_start_pos = False
    
    def animate_backward(self):
        if self.pos < self.start_pos:
            self.pos += 0.01
            self.place(relx=self.pos,rely=0.05,relwidth=self.width,relheight=0.9)
            self.after(10,self.animate_backward)
        else:
            self.in_start_pos = True

vid = cv2.VideoCapture(0)

# Declare the width and height in variables
width, height = 1100, 720

# Set the width and height
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def open_camera():

	# Capture the video frame by frame
	_, frame = vid.read()
     
	# Convert image from one color space to other
	opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

	# Capture the latest frame and transform to image
	captured_image = Image.fromarray(opencv_image)

	# Convert captured image to photoimage
	photo_image = ImageTk.PhotoImage(image=captured_image)

	# Displaying photoimage in the label
	label_widget.photo_image = photo_image

	# Configure image in the label
	label_widget.configure(image=photo_image)

	# Repeat the same process after every 10 seconds
	label_widget.after(10, open_camera)


window = tk.Tk()
window.configure(bg="#2E2E2E")
label_widget = ctk.CTkLabel(window,text=None)
label_widget.pack()
window.geometry("1280x720")
window.title("Smart CCTV")


animated_panel = SlidePanel(window, 1.0, 0.7)
ctk.CTkLabel(animated_panel, text="Label 1").pack(expand=True,fill="both",padx=2,pady=10)
ctk.CTkLabel(animated_panel, text="Label 2").pack(expand=True,fill="both",padx=2,pady=10)
ctk.CTkButton(animated_panel, text="Button").pack(expand=True,fill="both",pady=10)
ctk.CTkTextbox(animated_panel).pack(expand=True,fill="both",pady=10)

button = ctk.CTkButton(window, text="Features Tab",command=animated_panel.animate)
button.place(relx=0.6,rely=0.9,anchor="n")
button = ctk.CTkButton(window, text="Start Surveillance",command=open_camera)
button.place(relx=0.35,rely=0.9,anchor="n")

window.mainloop()
