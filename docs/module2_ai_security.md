# Module 2: AI Security (Face Recognition)

## 1. Overview
This module implements the core intelligence of the Smart Home project. We use the **LBPH (Local Binary Patterns Histograms)** Face Recognizer provided by OpenCV.

## 2. Why LBPH? (Important for Viva)
We chose LBPH over Deep Learning (dlib/ResNet) for this project:
1.  **Efficiency**: It runs smoothly on a standard laptop CPU without needing a GPU.
2.  **No Compilation**: It does not require complex C++ build tools (CMake/Visual Studio) which often fail on Windows.
3.  **Local Texture Analysis**: It is excellent for verifying identities in controlled environments like a smart home usage scenario.

## 3. Algorithm Steps
1.  **Face Detection**: Uses `Haar Cascade` to find the face coordinates $(x, y, w, h)$.
2.  **Feature Extraction**: The face is divided into a grid. For each pixel, we compare it to its neighbors to create a binary pattern (LBP).
3.  **Histogram Creation**: Histograms of these patterns are created for each region and concatenated.
4.  **Comparison**: The live face's histogram is compared to the stored model using Chi-square distance. 
    - Lower Distance = Better Match.

## 4. How to Setup
1.  **Install dependencies**:
    ```bash
    pip uninstall opencv-python
    pip install opencv-contrib-python
    ```
    *(Note: `opencv-contrib-python` contains the main modules + the `face` module needed for LBPH)*.

2.  **Add User Photo**:
    - Put your selfie in `src/known_faces/`.
    - Name it `YourName.jpg`.

3.  **Train & Run**:
    - `python src/face_auth.py`
    - The script automatically trains on images in the folder every time it starts.
