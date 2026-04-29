# Module 3: Decision & Alert System

## 1. Overview
This module acts as the central controller ("The Brain") of the smart home. It checks the output of the AI module and applies logic rules to determine if the home is safe or under threat.

## 2. Logic Flow
The system follows a simple "If-Then" architecture typical of embedded systems:

```python
IF (Seen_Face == Known):
    Status = "Access Granted"
    Action = Log Entry
ELSE IF (Seen_Face == Intruder):
    Status = "SECURITY ALERT"
    Action = Trigger Alarm (Console Beep/Log)
ELSE:
    Status = "Monitoring"
```

## 3. Real-World Relevance
In a physical execution (Raspberry Pi), the `print("ALARM")` line would be replaced by:
```python
GPIO.output(BUZZER_PIN, HIGH) # Turn on Physical Siren
requests.post("https://api.twilio.com/...", data={"sms": "Thief!"})
```
Since this is a **simulation**, we simulate the "Actuator" by printing high-priority logs to the console and changing the UI overlay to red.

## 4. How to Test
1.  Run `python src/security_system.py`
2.  **Scenario A (Owner)**: Show your face.
    -   Check Console: `LOG: Entry authorized for Vanapriya`
    -   Check Screen: Green Text "ACCESS GRANTED"
3.  **Scenario B (Intruder)**: Hide your face or show a friend's photo (phone screen).
    -   Check Console: `!!! ALARM: Unknown Person detected !!!`
    -   Check Screen: RED Text "CRITICAL: INTRUDER DETECTED!"
