import cv2
import os
import numpy as np

class FaceAuthSystem:
    """
    Module 2: AI Security (Face Recognition via OpenCV LBPH)
    
    Why LBPH (Local Binary Patterns Histograms)?
    - It is lightweight and creates a local texture model of the face.
    - Unlike Deep Learning (dlib), it does NOT require a GPU or C++ compilers.
    - Perfect for laptop-based IoT simulations.
    """
    
    def __init__(self, data_path='src/known_faces'):
        self.data_path = data_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize LBPH Face Recognizer
        # NOTE: Requires 'opencv-contrib-python'
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        except AttributeError:
            print("[ERROR] OpenCV Face module not found. Run: pip install opencv-contrib-python")
            exit()
            
        self.is_trained = False
        self.names = {}  # Map ID to Name
        
        # Initialize Liveness Detector
        from face_liveness import FaceLiveness
        self.liveness = FaceLiveness()

    def train_model(self):
        """
        Reads images from src/known_faces, detects faces, and trains the recognizer.
        """
        print("[INFO] Training Face Recognition Model...")
        
        faces = []
        ids = []
        current_id = 0
        
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            print(f"[WARNING] Created {self.data_path}. Please put images there.")
            return

        image_paths = [os.path.join(self.data_path, f) for f in os.listdir(self.data_path) 
                       if f.endswith('.jpg') or f.endswith('.png')]
        
        if not image_paths:
            print("[WARNING] No known faces found to train on!")
            return

        for path in image_paths:
            # Get the name from the filename (e.g., "Rahul.jpg" -> "Rahul")
            filename = os.path.basename(path)
            name = os.path.splitext(filename)[0]
            
            # Helper: Assign a numeric ID to each name
            if name not in self.names.values():
                self.names[current_id] = name
                label = current_id
                current_id += 1
            else:
                # Find existing ID for this name
                for k, v in self.names.items():
                    if v == name:
                        label = k
                        break

            # Load image and convert to Gray
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect face in the training image
            faces_rects = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            for (x, y, w, h) in faces_rects:
                faces.append(gray[y:y+h, x:x+w])
                ids.append(label)

        if faces:
            self.recognizer.train(faces, np.array(ids))
            self.is_trained = True
            print(f"[INFO] Training Complete. Learned {len(self.names)} people.")
            print(f"[INFO] Known People: {list(self.names.values())}")
        else:
            print("[ERROR] Could not detect faces in training images. Use clearer photos.")

    def recognize_faces(self, frame):
        """
        Detects faces in frame and predicts identity.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        names_found = []
        
        for (x, y, w, h) in faces:
            name = "Unknown"
            color = (0, 0, 255) # Red for Intruder
            
            if self.is_trained:
                # Predict
                id_, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                
                # Confidence: 0 = Perfect Match, 100+ = No Match
                # Usually < 50 is a good match for LBPH. 
                # Adjusted to 60 for better stability (was 70).
                if confidence < 60: 
                    name = self.names.get(id_, "Unknown")
                    if name != "Unknown":
                        color = (0, 255, 0) # Green for Authorized
                else:
                    name = "Intruder"

            # ------------------------------------------------
            # NEW: Liveness Check Integration
            # ------------------------------------------------
            face_roi = frame[y:y+h, x:x+w]
            is_real, liveness_status = self.liveness.check_liveness(face_roi)
            
            if not is_real and name != "Unknown":
                # If identifying a user, but liveness fails -> Block Access
                name = "VERIFYING..."
                color = (0, 255, 255) # Yellow
                cv2.putText(frame, liveness_status, (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            elif is_real:
                # Liveness Passed
                 cv2.putText(frame, "REAL", (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # ------------------------------------------------

            names_found.append(name)

            # Draw UI
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
        return frame, names_found

# Independent Testing
if __name__ == "__main__":
    system = FaceAuthSystem()
    system.train_model()
    
    if not system.is_trained:
        print("[EXIT] System not trained. Add images to src/known_faces/ and run again.")
        exit()

    print("[INFO] Starting Security Camera...")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame, names = system.recognize_faces(frame)
        cv2.imshow("Module 2: Face Security (LBPH)", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
