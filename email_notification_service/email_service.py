import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, sender_email=None, application_key=None, receiver_email=None, message=None, subject=None):
        self.sender_email = sender_email
        self.sender_password = application_key
        self.receiver_email = receiver_email
        self.message = message
        self.subject = subject

    def __create_header(self):
        header = MIMEMultipart()
        header['Subject'] = self.subject
        header['From'] = self.sender_email
        header['To'] = self.receiver_email
        body = MIMEText(self.message)
        header.attach(body)
        return header

    def send_email(self):
        try:
            print("Creating connection with email service")
            email = smtplib.SMTP_SSL('smtp.gmail.com')
            email.login(self.sender_email, self.sender_password)
            print("Login Successful")
            header = self.__create_header()
            email.sendmail(self.sender_email, self.receiver_email, header.as_string())
            email.quit()
            print("Email sent")
        except Exception as e:
            raise e
    @classmethod
    def default(self):
        pass


