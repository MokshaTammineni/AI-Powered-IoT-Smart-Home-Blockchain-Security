# Module 1: IoT Simulation (Vision-Based)

## 1. Overview
In this module, we simulate a sophisticated IoT sensor using the laptop's webcam. Instead of using a basic PIR (Passive Infrared) sensor which only detects heat, we use **Computer Vision** to detect motion. This represents "Edge Computing," where the sensor itself processes data (video frames) and only triggers when relevant changes occur.

## 2. Algorithm: Frame Differencing
We use a standard method to detect motion:
1.  **Capture Frame $t$ and Frame $t+1$**.
2.  **Calculate Difference**: $|Frame_{t+1} - Frame_t|$.
3.  **Grayscale & Blur**: Convert to black/white and blur to remove visual noise.
4.  **Threshold**: Any pixel change > 20 is considered "motion".
5.  **Contour Detection**: Draw boxes around the moving areas.

## 3. Justification for Viva
**Examiner Question**: "Where is the IoT hardware? Why just a webcam?"
**Your Defense**:
> "Sir/Ma'am, modern IoT is moving towards 'Software-Defined Sensors'. A webcam provides richer data than a simple PIR sensor. By processing the video locally (Edge AI), I am simulating a Smart Camera (like Ring or Nest) which reduces bandwidth by not sending 24/7 video to the server, but only reacting to events. This is a simulation of an Edge IoT Node."

## 4. How to Test
1.  Install OpenCV: `pip install opencv-python`
2.  Run the script: `python src/camera_sensor.py`
3.  Move your hand in front of the camera.
4.  Observe the Green Box and "Motion Detected" text.
