import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading

class NotificationManager:
    """
    Module: Real-World Integration (Email Alerts)
    
    This class handles sending email alerts when an intruder is detected.
    It uses Python's built-in `smtplib` to connect to Gmail's SMTP server.
    
    SECURITY NOTE: 
    - Requires a Gmail "App Password" (not regular password).
    - Hardcoding credentials is bad practice for production, but okay for this student demo.
    """
    
    def __init__(self):
        # TODO: USER MUST FILL THESE IN
        self.sender_email = "alaparthyvana@gmail.com"  # Replace with your email
        self.app_password = "pfaplgoziwvcoaej"     # Replace with your App Password
        
        # User defined alert receiver (can be same as sender)
        self.receiver_email = self.sender_email 
        
        self.last_sent_time = None
        self.cooldown_seconds = 300 # 5 Minutes cooldown to avoid spam

    def send_alert(self, intruder_name="Unknown Person"):
        """
        Sends an email alert if cooldown has passed.
        """
        current_time = datetime.now()
        
        # Check cooldown
        if self.last_sent_time:
            time_diff = (current_time - self.last_sent_time).total_seconds()
            if time_diff < self.cooldown_seconds:
                print(f"[INFO] Alert suppressed (Cooldown active: {int(self.cooldown_seconds - time_diff)}s remaining)")
                return

        # Run email sending in a background thread to prevent freezing the video
        email_thread = threading.Thread(target=self._send_email_thread, args=(intruder_name, current_time))
        email_thread.start()
        
    def _send_email_thread(self, intruder_name, current_time):
        """
        Actual email sending logic (Private method).
        """
        print(f"[ALERT] Sending email to {self.receiver_email}...")
        
        try:
            # Create Message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = f"🚨 SECURITY ALERT: Intruder Detected ({intruder_name})!"

            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #e74c3c;">⚠️ Security Intrusion Detected</h2>
                <p><strong>Time:</strong> {current_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Identified As:</strong> {intruder_name}</p>
                <p>Please check your security dashboard immediately.</p>
                <hr>
                <p style="font-size: 0.8rem; color: #666;">Sent from your AI Smart Home System</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html'))

            # Connect to Gmail SMTP Server
            # 587 is the default port for TLS
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.receiver_email, text)
            server.quit()
            
            print("[SUCCESS] Email Alert Sent!")
            self.last_sent_time = current_time
            
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            print("[TIP] Did you enable 'App Passwords' in your Google Account?")

# Test
if __name__ == "__main__":
    nm = NotificationManager()
    # nm.send_alert("Test Intruder") # Uncomment to test
