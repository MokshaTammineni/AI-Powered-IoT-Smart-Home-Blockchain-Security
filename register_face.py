import cv2
import os

def register_face():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Register Face")
    
    print("[INFO] Press 'SPACE' to capture your face.")
    print("[INFO] Press 'q' to quit without saving.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            break
            
        cv2.imshow("Register Face", frame)
        
        k = cv2.waitKey(1)
        if k % 256 == 32: # SPACE pressed
            # Ask for name
            print("Capture successful!")
            name = input("Enter the name of the person: ").strip()
            
            if name:
                # Save image
                save_path = f"src/known_faces/{name}.jpg"
                if not os.path.exists("src/known_faces"):
                    os.makedirs("src/known_faces")
                    
                cv2.imwrite(save_path, frame)
                print(f"[SUCCESS] Saved {save_path}")
                break
            else:
                print("[ERROR] Name cannot be empty.")
                
        elif k % 256 == ord('q'):
            print("Escape hit, closing/not saving...")
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_face()
 