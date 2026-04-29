import cv2
import time

class FaceLiveness:
    """
    Module: Advanced AI (Liveness Detection)
    
    Goal: Prevent Photo Spoofing.
    Logic: Requires the user to BLINK to prove they are real.
    """
    
    def __init__(self):
        # Load Eye Cascade
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # State Tracking
        self.eyes_visible_start = 0
        self.blink_timestamp = 0
        self.is_live = False
        self.last_state = "SEARCHING" # SEARCHING, EYES_FOUND, BLINK_DETECTED

    def check_liveness(self, face_roi):
        """
        Analyzes a face ROI to detect blinking.
        Returns: (is_live, status_text)
        """
        if face_roi is None or face_roi.size == 0:
            return False, "NO FACE"

        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))
        
        current_time = time.time()
        eyes_detected = len(eyes) >= 1 # At least one eye needed

        # Liveness Logic: True -> False (Blink) -> True
        
        if self.is_live:
            # Reset after 5 seconds to force re-verification (optional, good for security)
            if current_time - self.blink_timestamp > 5:
                self.is_live = False
                self.last_state = "SEARCHING"
            return True, "LIVENESS CONFIRMED"

        if eyes_detected:
            if self.last_state == "BLINKING":
                # Eyes reappeared after blink!
                self.is_live = True
                self.blink_timestamp = current_time
                return True, "REAL PERSON"
            else:
                self.last_state = "EYES_OPEN"
                return False, "PLEASE BLINK"
        
        else:
            # No eyes detected
            if self.last_state == "EYES_OPEN":
                # Eyes were open, now closed -> POTENTIAL BLINK
                self.last_state = "BLINKING"
                return False, "BLINKING..."
            else:
                self.last_state = "SEARCHING"
                return False, "LOOK AT CAMERA"

    def reset(self):
        self.is_live = False
