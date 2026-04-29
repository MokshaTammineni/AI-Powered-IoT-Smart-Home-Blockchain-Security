import cv2
import time
from datetime import datetime

class IoTCameraSensor:
    """
    Module 1: IoT Simulation (Vision-based Sensor)
    
    This class simulates an IoT sensor using the laptop's webcam.
    Instead of a simple PIR sensor, we use Computer Vision to detect motion.
    
    IoT Principle: "Edge Computing"
    - The processing happens locally (on the laptop) rather than sending raw video to the cloud.
    - Only "events" (motion) are flagged.
    """
    
    def __init__(self, camera_index=0, frame_width=640, frame_height=480):
        self.camera_index = camera_index
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cap = None
        self.motion_detected = False
        
    def start_sensing(self):
        """
        Starts the webcam and continuous monitoring loop.
        Press 'q' to quit.
        """
        print("[INFO] Starting IoT Camera Sensor...")
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Set resolution (Lower resolution = faster processing for IoT simulation)
        self.cap.set(3, self.frame_width)
        self.cap.set(4, self.frame_height)
        
        if not self.cap.isOpened():
            print("[ERROR] Could not access web camera.")
            return

        # Read the first frame for baseline reference
        ret, frame1 = self.cap.read()
        ret, frame2 = self.cap.read()
        
        print("[INFO] Sensor Active. Press 'q' to stop.")

        while self.cap.isOpened():
            # 1. IoT Sensing: Detect difference between frames
            diff = cv2.absdiff(frame1, frame2)
            
            # 2. Conversion: RGB to Grayscale (Reduces data complexity)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # 3. Filtering: Blur to remove noise
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 4. Thresholding: Convert to binary (Motion vs No Motion)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            
            # 5. Contour Detection: Find moving objects
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            motion_status = "No Motion"
            
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                
                # Sensitivity threshold: Ignore small movements (like wind/noise)
                if cv2.contourArea(contour) < 900:
                    continue
                
                # Motion confirmed
                motion_status = "Motion Detected!"
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Display Status on Screen (Simulation UI)
            cv2.putText(frame1, f"Status: {motion_status}", (10, 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv2.imshow("Module 1: IoT Camera Sensor Simulation", frame1)
            
            # Update frames
            frame1 = frame2
            ret, frame2 = self.cap.read()
            
            if cv2.waitKey(10) == ord('q'):
                break
                
        self.stop_sensing()

    def stop_sensing(self):
        print("[INFO] Stopping Sensor...")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

# Run the module independently for testing
if __name__ == "__main__":
    sensor = IoTCameraSensor()
    sensor.start_sensing()
