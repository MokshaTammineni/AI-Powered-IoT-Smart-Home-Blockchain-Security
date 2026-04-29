from flask import Flask, render_template, Response
import cv2
import time
from datetime import datetime
from face_auth import FaceAuthSystem
from secure_logger import BlockchainLogger
from notification_manager import NotificationManager

# Initialize Flask App
app = Flask(__name__)

# Initialize Core Modules
print("[INIT] Loading AI Models and Blockchain...")
face_system = FaceAuthSystem()
face_system.train_model()

blockchain = BlockchainLogger()
blockchain.add_log("SYSTEM", "Admin", "Server Started")

# Initialize Notification Manager
notifier = NotificationManager()

# Global Video Capture
camera = cv2.VideoCapture(0)

# Cooldown Tracker (To prevent spamming the blockchain)
last_logged_time = {}

def generate_frames():
    """
    Video streaming generator function.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # 1. Run AI Logic
        frame, names = face_system.recognize_faces(frame)
        
        # 2. Blockchain Logic (Active Integration)
        # Check if we should log this event (Debouncing to avoid log spam)
        current_time = time.time()
        
        for name in names:
            event_type = "INTRUSION" if name == "Intruder" or name == "Unknown" else "ENTRY"
            
            # Key Logic: Only log if we haven't seen this person in the last 10 seconds
            if name not in last_logged_time or (current_time - last_logged_time[name] > 10):
                blockchain.add_log(event_type, name, "Detected by Camera Sensor")
                last_logged_time[name] = current_time
                print(f"[BLOCKCHAIN] Auto-logged event for {name}")

                # TRIGGER EMAIL ALERT for Intruders
                if event_type == "INTRUSION":
                    # Run in a non-blocking way (simple check for now)
                    notifier.send_alert(name)
                
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Dashboard Home"""
    # Simply pass the blockchain data to the frontend
    return render_template('index.html', chain=blockchain.chain)

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Simulate adding a log via URL (for demo purposes)
@app.route('/simulate/<event>/<name>')
def add_log(event, name):
    blockchain.add_log(event, name, "Event triggered via Web")
    return "Log Added"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
