# CHAPTER 3: SYSTEM DESIGN

## 3.1 System Architecture

The system architecture is designed as a modular pipeline that integrates Internet of Things (IoT) principles, Artificial Intelligence (AI), and Blockchain technology to create a cohesive smart home security ecosystem. The interaction between these modules is linear and event-driven.

The architecture consists of five primary layers:

1.  **Sensing Layer (IoT)**: This layer is responsible for perceiving the environment. It utilizes a visual sensor (webcam) to capture a continuous video stream. Motion detection algorithms process this stream in real-time to identify potential activity, filtering out static frames to conserve processing power.

2.  **Processing Layer (AI)**: Upon triggering by the sensing layer, the video frames are passed to the AI engine. This layer performs complex computer vision tasks including Face Detection (locating faces), Liveness Detection (distinguishing real humans from photos), and Face Recognition (identifying the person).

3.  **Decision Layer (Control Logic)**: This layer acts as the system's brain. It receives the classification result from the AI layer (e.g., "Authorized User", "Unknown", or "Spoof Attempt") and executes pre-defined security protocols. These protocols include unlocking/locking doors, triggering visual alarms, and preparing data for logging.

4.  **Logging Layer (Blockchain)**: To ensure accountability and data integrity, every significant event handled by the Decision Layer is recorded here. A custom private blockchain construct ensures that each log entry is cryptographically linked to the previous one, rendering the history immutable and tamper-proof.

5.  **Application Layer (Dashboard)**: The final layer provides a user interface. A local web server (Flask) renders a dashboard that displays the live camera feed with augmented reality overlays (bounding boxes, names) and a real-time view of the blockchain ledger.

---

## 3.2 Dataset Description

A custom dataset is utilized for this project, specifically tailored to the deployment environment (e.g., the user’s home). Unlike large-scale public datasets (like LFW or CelebA) which are used for generalized training, this system uses a **One-Shot Learning** or **Few-Shot Learning** approach typical for personalized security systems.

*   **Structure**: The dataset is organized in a directory structure `src/known_faces/`.
*   **Content**: It contains images of authorized individuals (e.g., family members). Each image is labeled with the person's name (e.g., `user_name.jpg`).
*   **Format**: Images are stored in standard formats (JPG/PNG) and are converted into grayscale matrices for processing.
*   **Dynamic Expansion**: The system is designed to allow easy addition of new authorized users by simply adding their photograph to the dataset folder.

---

## 3.3 Data Preprocessing

Before feeding images into the recognition model, raw visual data undergoes several preprocessing steps to ensure consistency and improve accuracy.

1.  **Grayscale Conversion**: Color information is often redundant for texture-based face recognition. All input frames are converted from RGB to Grayscale to reduce dimensionality and processing time.
    *   Formula: $Y = 0.299R + 0.587G + 0.114B$

2.  **Face Localization & Cropping**: The system uses **Haar Cascade Classifiers** to scan the image for facial features. Once a face is detected, the region of interest (ROI) is cropped, discarding the background noise.

3.  **Normalization/Resizing**: The cropped face images are resized to a fixed dimension to ensure all input vectors to the model are of equal length. Histogram Equalization may be applied to improve contrast, making the model more robust to varying lighting conditions.

4.  **Label Encoding**: The string names of the files (e.g., "John") are mapped to unique integer IDs (e.g., 1) required by the LBPH algorithm during training.

---

## 3.4 Model Design

The core recognition engine employs the **Local Binary Patterns Histograms (LBPH)** algorithm. This algorithm was selected over Deep Learning methods (like CNNs) due to its computational efficiency on edge devices and its ability to learn from a small number of images.

### 3.4.1 Mechanics of LBPH
The model works by characterizing the local structure of the face image:
1.  **LBP Operation**: A sliding window (3x3 pixels) moves across the image. The center pixel is compared with its 8 neighbors.
2.  **Binary Thresholding**: If a neighbor's intensity is greater than or equal to the center, it is assigned a '1'; otherwise '0'.
3.  **Decimal Conversion**: The resulting 8-bit binary code is converted to a decimal value, representing the local texture pattern (e.g., edge, corner, spot).
4.  **Histogram Extraction**: The image is divided into a grid (e.g., 8x8). A histogram of LBP values is calculated for each grid cell.
5.  **Concatenation**: All histograms are concatenated to form a single feature vector that uniquely represents the face.

---

## 3.5 Training Procedure

The training process in this system is fast and occurs typically upon system initialization.

1.  **Initialization**: The `cv2.face.LBPHFaceRecognizer_create()` object is instantiated.
2.  **Loading Data**: The system iterates through the `src/known_faces/` directory.
    *   For each image: Read -> Grayscale -> Detect Face -> Crop.
    *   Extract Label from filename.
3.  **Training**: The `train(faces, labels)` method is called. The algorithm computes the LBP histograms for all training images and stores them in memory.
4.  **Serialization (Optional)**: The trained model state can be saved to a `.yml` file (e.g., `trainer.yml`) to avoid retraining on every restart, though for small datasets, real-time training is instantaneous.

---

## 3.6 Evaluation Metrics

The system uses specific metrics to determine the reliability of a prediction.

### 3.6.1 Confidence Score (Distance)
Unlike probability-based models (which output 0-100%), LBPH outputs a **Confidence Score** based on distance (e.g., Chi-Square or Euclidean distance) between the live face's histogram and the stored model's histogram.
*   **Lower Score** = Closer Match.
*   **0**: Perfect match.
*   **< 50**: High confidence match (Authorized).
*   **> 80**: Low confidence match (Unknown/Intruder).

### 3.6.2 Thresholding
A critical hyperparameter is the **Decision Threshold**.
*   **Acceptance Threshold**: Set to roughly **70**.
    *   If $Score < Threshold$: Identify as User.
    *   If $Score > Threshold$: Identify as Unknown.
This threshold is tuned physically by testing the system under different lighting conditions to minimize False Positives and False Negatives.

---

## 3.7 System Workflow Algorithm

The operational logic follows a strict algorithmic sequence:

1.  **START**
2.  **Initialize**: Load Haar Cascades, Train LBPH Model, Connect to Blockchain.
3.  **LOOP**:
    4.  **Capture Frame** from Camera.
    5.  **Detect Motion**: Is there movement?
        *   NO: Go to Step 4.
        *   YES: Proceed.
    6.  **Detect Face**: Is there a face?
        *   NO: Go to Step 4.
        *   YES: Extract Face Region.
    7.  **Liveness Check**: Is the face 3D/Real?
        *   NO (Spoof): Trigger "Spoof Alert" -> Log to Blockchain -> Go to Step 4.
        *   YES: Proceed.
    8.  **Recognize Identity**: Compare Face with Model.
    9.  **Decision**:
        *   If **Match Found**: 
            *   Set Status: "Authorized".
            *   Action: Unlock Door (Simulated).
            *   Log: "Entry Detected" to Blockchain.
        *   If **No Match**:
            *   Set Status: "Intruder".
            *   Action: Lock Door, Sound Alarm.
            *   Log: "Intrusion Alert" to Blockchain.
    10. **Update Dashboard**: Display Video + Logs.
    11. **Go to Step 4**.
12. **END**
