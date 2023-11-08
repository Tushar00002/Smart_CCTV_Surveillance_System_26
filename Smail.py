import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import flags

def send_email(message,image_filename,default_email = "smartcctv453@gmail.com"):
    sender_email = "smartcctv453@gmail.com"  
    sender_password = "kdktdlxnofqnpqrx"
    subject = "Smart CCTV"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    receiver_email = flags.email if flags.email else default_email 

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    msg.attach(MIMEText(message, 'plain'))

    with open(image_filename, 'rb') as attachment:
        image_data = attachment.read()
    image = MIMEImage(image_data, name=image_filename)
    msg.attach(image)

    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
