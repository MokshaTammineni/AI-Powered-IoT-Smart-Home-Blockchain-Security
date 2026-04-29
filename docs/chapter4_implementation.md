# CHAPTER 4: IMPLEMENTATION

This chapter details the practical realization of the **AI-Powered IoT Smart Home with Blockchain Security**. It covers the platform requirements and the step-by-step development of each module.

---

## 4.1 Software Requirements

The project is built entirely using open-source technologies to ensure accessibility and reproducibility.

| Component | Specification | Purpose |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11 (64-bit) | Primary development and execution environment. |
| **Programming Language** | Python 3.9+ | Core language for AI, Backend, and Logic. |
| **IDE** | VS Code / PyCharm | Code editing and debugging. |
| **Computer Vision Lib** | OpenCV (`opencv-contrib-python`) | Image processing and LBPH Face Recognition. |
| **Web Framework** | Flask | Serving the Dashboard and API endpoints. |
| **Data Handling** | NumPy, JSON | Matrix operations and data serialization. |
| **Blockchain Logic** | Python (Hashlib) | Implementing SHA-256 hashing and chain validation. |
| **Frontend** | HTML5, CSS3, Bootstrap | Designing the responsive user interface. |

---

## 4.2 Hardware Requirements

The system is designed to run on "Edge" architecture, meaning it processes data locally without needing heavy cloud resources.

| Hardware | Recommendation | Minimum Requirement |
| :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i5 (8th Gen) or AMD Ryzen 5 | Intel Core i3 / Raspberry Pi 4 |
| **RAM** | 8 GB DDR4 | 4 GB |
| **Storage** | 256 GB SSD (for fast I/O) | 128 GB HDD |
| **Camera** | HD Webcam (720p) | Built-in Laptop Webcam (480p) |
| **Connectivity** | Wi-Fi / Ethernet | Localhost (Offline Mode supported) |

---

## 4.3 Module-wise Implementation

The implementation is divided into five distinct modules, executed sequentially to build the complete system.

### Module 1: IoT Simulation (The "Eyes")
**Goal**: To simulate an "Always-On" smart security camera using a standard laptop webcam.

*   **Logic**:
    *   The system initializes the webcam using `cv2.VideoCapture(0)`.
    *   It captures a reference frame (background) and compares subsequent frames against it using **Frame Differencing**.
    *   It calculates the absolute difference between pixel intensities: $\Delta = |Current - Reference|$.
    *   If $\Delta > Threshold$, it contours the area and flags it as "Motion Detected".
*   **Significance**: This reduces computational load by ensuring the heavy AI model only runs when someone is actually present, extending the theoretical battery life of the IoT device.

### Module 2: AI Security Layer (The "Brain")
**Goal**: To identify the person triggering the motion sensor.

*   **Step 1: Data Collection**:
    *   A script captures 30-50 grayscale images of the authorized user's face.
    *   These images are stored in a dataset folder `src/known_faces/`.
*   **Step 2: Training**:
    *   The **LBPH (Local Binary Patterns Histograms)** recognizer reads these images.
    *   It extracts texture features (LBP codes) and maps them to a specific ID (e.g., User ID: 1).
    *   The trained model creates a histogram database of all known faces.
*   **Step 3: Recognition**:
    *   When a face is detected in the live feed, the system generates a histogram for it.
    *   It compares this histogram with the trained database using Chi-Square distance.
    *   **result**: If `confidence < 60`, the person is "Authorized". Else, they are "Unknown".

### Module 3: Decision & Alert System (The "Reflex")
**Goal**: To automate security responses based on AI analysis.

*   **Implementation**:
    *   A Python control loop monitors the output of Module 2.
    *   **Condition A (Authorized)**:
        *   Triggers function `unlock_door()`.
        *   Updates UI Text to Green.
        *   Prepares a log entry: `{"event": "ENTRY", "user": "Name"}`.
    *   **Condition B (Intruder)**:
        *   Triggers function `lock_door()` (Simulated).
        *   Activates "Red Alert" mode in the application.
        *   Prepares a log entry: `{"event": "INTRUSION", "user": "Unknown"}`.

### Module 4: Blockchain Logging (The "Vault")
**Goal**: To create a tamper-proof audit trail of all security events.

*   **Class Structure**: `Blockchain` class in Python.
*   **Block Definition**: Each event creates a `Block` object containing:
    *   `Index`: Sequence number (0, 1, 2...).
    *   `Timestamp`: Exact time of the event.
    *   `Data`: The security log (e.g., "Intrusion detected").
    *   `Previous Hash`: The digital fingerprint of the *last* block.
    *   `Hash`: The fingerprint of *this* block (calculated using SHA-256).
*   **Security Mechanism**:
    *   The `calculate_hash()` function combines all block data into a string and hashes it.
    *   Because `Previous Hash` is part of the input, changing an old block changes its hash, which changes the *next* block's `Previous Hash`, and so on. This "avalanche effect" makes the chain immutable.

### Module 5: Web Dashboard (The "Face")
**Goal**: To envision the system as a consumer-ready product.

*   **Backend**: A Flask app (`app.py`) serves the HTML pages.
*   **Video Streaming**: Uses a generator function to yield video frames as a multipart HTTP response (`mjpeg`), allowing live streaming in the browser.
*   **Real-Time Ops**:
    *   The dashboard auto-refreshes the "Blockchain Ledger" section to show new blocks as they are mined.
    *   It provides a visual confirmation of the system's status (Secure vs. Alert).
