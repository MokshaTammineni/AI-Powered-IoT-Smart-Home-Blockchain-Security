import cv2
import time
from datetime import datetime
from face_auth import FaceAuthSystem
from secure_logger import BlockchainLogger

class SmartHomeSecurity:
    """
    Module 3: Decision & Alert System
    
    This is the "Brain" of the project.
    It integrates:
    - Module 2 (AI Face Auth)
    
    And implements Logic:
    1. If Name == "Intruder" -> TRIGGER ALERT (Red)
    2. If Name == Known User -> GRANT ACCESS (Green)
    """
    def __init__(self):
        print("[INIT] Initializing Security System...")
        self.auth = FaceAuthSystem()
        self.auth.train_model()
        
        # Initialize Blockchain for Immutable Logging
        self.blockchain = BlockchainLogger()
        
        # Spam Prevention: Cooldown for alerts (seconds)
        self.last_alert_time = 0
        self.alert_cooldown = 5 
        
    def start_monitoring(self):
        print("[INFO] Security Monitoring Started...")
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            # Step 1: Detect & Identify
            frame, names = self.auth.recognize_faces(frame)
            
            # Step 2: Decision Logic
            system_status = "MONITORING"
            color = (255, 255, 0) # Cyan
            
            if names:
                # Priority: Check for intruders first
                if "Intruder" in names:
                    system_status = "CRITICAL: INTRUDER DETECTED!"
                    color = (0, 0, 255) # Red
                    
                    # ALERT ACTION: In a real IoT system, this would ring a buzzer
                    print(f"[{datetime.now()}] !!! ALARM: Unknown Person detected !!!")
                    
                    # BLOCKCHAIN LOGGING (With Spam Prevention)
                    current_time = time.time()
                    if current_time - self.last_alert_time > self.alert_cooldown:
                        self.blockchain.add_log("INTRUSION", "Unknown", "Unauthorized Face Detected")
                        self.last_alert_time = current_time
                    else:
                        print(f"[INFO] Alert cooldown active. Skipping blockchain log.")
                    
                else:
                    # If we only see known people
                    authorized_person = names[0]
                    system_status = f"ACCESS GRANTED: {authorized_person}"
                    color = (0, 255, 0) # Green
                    print(f"[{datetime.now()}] LOG: Entry authorized for {authorized_person}")

            # Step 3: Feedback Loop (UI)
            # Add a classic "Security Cam" timestamp
            cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (10, frame.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Show System Status at top
            cv2.putText(frame, system_status, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            cv2.imshow("Module 3: Main Security Dashboard", frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    security_system = SmartHomeSecurity()
    security_system.start_monitoring()
