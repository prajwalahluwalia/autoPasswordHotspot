import subprocess
import random
import string
import smtplib, ssl
from config import sender_email, sender_password

class GeneratePassword:
    def __init__(self, length, receiver_email, sender_email, sender_password):
        self.password = ''
        self.length = length
        self.receiver_email = receiver_email
        self.sender_email = sender_email
        self.sender_password = sender_password

    def __generateRandomPassword(self):
        letters = string.ascii_letters
        digits = string.digits
        punctuation = '@#$%&!'

        combination = letters+digits+punctuation

        self.password = ''.join(random.choice(combination) for i in range(self.length))
        return self.password

    def changePassword(self):

        status = ''
        self.password = self.__generateRandomPassword()
        output = subprocess.run('iwconfig wlp2s0', capture_output=True, shell=True)
        
        for line in str(output).split(' '):
            if line[:4]=='Mode':
                status = line[5:]
        
        if status!="Master":
            return f'Please turn on your hotspot'
        
        command = f"nmcli connection modify Hotspot 802-11-wireless-security.key-mgmt wpa-psk 802-11-wireless-security.psk {self.password}"
        
        subprocess.run(command, shell=True, capture_output=True)

        self.sendEmail()

    def sendEmail(self):
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = self.sender_email
        password = self.sender_password
        
        message = f'Subject : Password Changed \n The password is {self.password}'
        print(message)
        
        context = ssl.create_default_context()

        try:
            for email in self.receiver_email:
                print(email)
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, password)
                server.sendmail(sender_email, email, message)
                print(f'Email sent to {email}')

        except Exception as e:
            return f'e'
        
        finally:
            server.quit()


if __name__=="__main__":
    print(sender_email, sender_password)
    receiver_email = ['prajwalahluwalia3@gmail.com']
    gp = GeneratePassword(8, receiver_email, sender_password, sender_email)
    print(gp.changePassword())
