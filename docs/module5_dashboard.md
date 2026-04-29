# Module 5: Web Dashboard

## 1. Overview
The final module binds everything together. We use **Flask**, a Python web framework, to create a user interface. This allows the user to view the camera feed and the blockchain security logs from any browser.

## 2. Integration Details
-   **Frontend**: HTML/CSS (`src/templates/index.html`) using a modern card-based layout.
-   **Backend**: Flask (`src/app.py`).
-   **Streaming**: The camera frames are processed by our AI (Module 2) and then streamed to the browser using Multipart Mixed Replace (MJPEG).

## 3. How to Run THE FINAL PROJECT
1.  Navigate to the project folder.
2.  Run:
    ```powershell
    python src/app.py
    ```
3.  Open your browser (Chrome/Edge).
4.  Go to: `http://127.0.0.1:5000/`

## 4. Features to Show in Viva
1.  **Live AI Feed**: Show that the camera is accessible via browser.
2.  **Blockchain Integration**: The right side of the screen shows "Immutable Blockchain Ledger".
    -   Refresh the page to see new logs (or rely on the auto-refresh script).
3.  **Simulation**: To add a fake log for demonstration, you can visit:
    `http://127.0.0.1:5000/simulate/INTRUSION/Unknown`
    Then go back to the dashboard and see the Red Alert in the blockchain.
