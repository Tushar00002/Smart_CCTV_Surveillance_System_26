import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email = "bepositiveadi0099@gmail.com"):
    sender_email = "abdulbasit63920@gmail.com"  
    sender_password = "yqvmxuaaoruawspi"
    subject = "Fire Alert"
    message = "Fire Breakdown alert!!!"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    msg.attach(MIMEText(message, 'plain'))
    
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")