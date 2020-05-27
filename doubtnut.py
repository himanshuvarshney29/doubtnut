from threading import Thread, Event
import time
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="doubtnut"
)
mycursor = mydb.cursor()

stop_event = Event()
def do_actions():
    i = 0
    while True:
        i += 1
        time.sleep(1)
        # Here we make the check if the other thread sent a signal to stop execution.
        if stop_event.is_set():
            break
 
 
if __name__ == '__main__':
    action_thread = Thread(target=do_actions)
 
    action_thread.start()
    action_thread.join(timeout=60)

    stop_event.set()
 
    send_mail(data)

def send_mail(data):
    # get all users in 5th to 6 th minute
    mycursor.execute("SELECT * FROM user_asked_question where created+(5*60) < Now() adn created+(5*60) > NOW()-60")
    myresult = mycursor.fetchall()

    for x in myresult:
        generatePdfAndSendMail(x)

def generatePdfAndSendMail(data):
    c = canvas.Canvas('doubtnut.pdf')
    c.drawString(100,750,"Welcome to doubtnut!")
    c.showPage()
    c.save()
    sendEmail(data)

def sendEmail():
    try:
        mail_content = ''' Hello Welcome to doubtnut
        '''
        # The mail addresses and password
        sender_address = 'sender123@gmail.com'
        sender_pass = 'xxxxxxxx'
        receiver_address = 'receiver567@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'doubtnut.pdf'
        attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
