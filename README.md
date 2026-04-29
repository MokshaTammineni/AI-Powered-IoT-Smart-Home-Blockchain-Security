🏠 AI Powered IoT Smart Home with Blockchain Secured Security Features

🚀 Overview

This project is an advanced smart home security system that combines Artificial Intelligence (AI), IoT concepts, and Blockchain technology to provide secure and intelligent home automation.
It includes face recognition with liveness detection, real-time monitoring, and secure logging to ensure safety and prevent unauthorized access.

🎯 Features

* 🔐 Face Recognition Authentication
* 🧠 Liveness Detection (Anti-spoofing)
* 📷 Real-time Camera Monitoring
* 🔔 Notification System
* 🔗 Blockchain-based Secure Logging
* 🌐 Web Dashboard Interface

🛠️ Tech Stack

* Python
* OpenCV
* Face Recognition
* Flask (Backend)
* HTML/CSS (Frontend)
* Blockchain Concepts

📂 Project Structure

AI-Powered-IoT-Smart-Home-Blockchain-Security/
├── src/                # Core logic
│    ├── app.py
│    ├── face_auth.py
│    ├── face_liveness.py
│    ├── camera_sensor.py
│    ├── notification_manager.py
│    ├── register_face.py
│    ├── secure_logger.py
│
├── templates/          # Frontend UI
│    └── index.html
│
├── known_faces/        # Stored face images
│
├── requirements.txt
├── README.md
└── .gitignore


 ▶️ How to Run

 1️⃣ Install dependencies

pip install -r requirements.txt

2️⃣ Run the application

python src/app.py


 🏗️ System Architecture

User → Camera → Face Detection → Liveness Check → Face Recognition
↓
If Verified
↓
Grant Access + Send Notification
↓
Store Logs using Blockchain

 🔐 Security Highlights
* Liveness detection prevents spoofing attacks (photo/video)
* Blockchain ensures tamper-proof data storage
* Secure authentication system

🌟 Future Improvements

* Mobile app integration
* Cloud deployment (AWS/GCP)
* IoT hardware integration
* Advanced AI anomaly detection

👩‍💻 Author

Moksha Sree
AI & ML Undergraduate
