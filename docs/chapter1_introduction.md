# CHAPTER 1: INTRODUCTION

## 1.1 Introduction

The concept of a "Smart Home" has evolved from simple automated lighting to complex ecosystems that manage energy, comfort, and security. However, as these systems become more interconnected, they also become more vulnerable to cyber-physical threats. This project, **"AI-Powered IoT Smart Home with Blockchain-Secured Security Features,"** represents a next-generation approach to home safety. It integrates the sensing capabilities of the Internet of Things (IoT), the cognitive processing of Artificial Intelligence (AI), and the immutable record-keeping of Blockchain technology to create a holistic security solution.

## 1.2 Background of the Problem

Traditional home security systems have relied on hardware-centric approaches.
1.  **Passive Sensors**: Devices like PIR (Passive Infrared) motion detectors trigger alarms based on heat signatures. They cannot distinguish between a burglar, a stray dog, or a shifting curtain, leading to frequent false alarms.
2.  **Centralized Vulnerability**: Most modern "smart" cameras store data on centralized cloud servers (e.g., AWS, Google Cloud). If these servers are hacked, or if an insider at the company acts maliciously, sensitive user data (video logs) can be deleted or manipulated without the user's knowledge.
3.  **Lack of Context**: Standard alarms report *that* motion occurred, but not *who* caused it or *why* it matters, leaving the homeowner to guess the severity of the threat.

## 1.3 Motivation behind the Project

The primary motivation is to decentralize trust and add intelligence to the "Edge" of the network.
*   **Privacy First**: We wanted to build a system where video data is processed locally (on the laptop/device) rather than being streamed 24/7 to a corporate cloud.
*   **Trust through Code**: In an era of "Deepfakes" and data breaches, we cannot simply trust a database administrator to keep our logs safe. We needed a system where the logs themselves are cryptographically sealed.
*   **Reducing Anxiety**: By using AI to filter out trivial events (like a pet moving), we aim to solve "Alarm Fatigue," ensuring that when the phone buzzes, it is a genuine security event.

## 1.4 Importance of the Chosen Topic

1.  **Convergence of Tech**: This project stands at the intersection of three major industrial trends: **Edge AI**, **IoT**, and **Web3/Blockchain**. Understanding how to integrate these distinct fields is a critical skill for future system architects.
2.  **Security Utility**: Physical security is a universal need. A system that can autonomously distinguish between a family member (granting access) and a stranger (denying access) has immediate, high-value real-world application.
3.  **Data Integrity**: As legal systems and insurance companies increasingly rely on digital evidence, having a blockchain-verified log of a break-in provides indisputable proof that an event occurred at a specific time.

## 1.5 Scope of the Project

*   **IoT Scope (Simulation)**: usage of a laptop webcam to simulate a "Smart Vision Sensor." Implementation of **Frame Differencing** algorithms to detect motion and trigger the system.
*   **AI Scope**: Implementation of **Face Detection** (Haar Cascades), **Liveness Detection** (Eye Blink Analysis to prevent photo spoofing), and **Face Recognition** (LBPH algorithm) to classify individuals.
*   **Blockchain Scope**: Development of a private, local blockchain using Python (`hashlib`) to securely store alert logs. It focuses on the data integrity and cryptographic linking of blocks.
*   **Alerting Scope**: Integration of an **Email Notification System** (SMTP) to send real-time alerts to the owner.
*   **Limitations**: The system runs on a single node (Edge Device/Laptop) and does not currently support multi-node P2P consensus or night-vision capabilities.

---

## 1.6 Problem Statement

**Ideally**, a smart home security system should be intelligent enough to recognize its owners and secure enough to prevent any tampering with its records.
**However**, current market solutions suffer from:
1.  **High False Positive Rates**: Triggering for non-human or authorized movement.
2.  **Centralized Data Risks**: Logs are mutable strings in a database that can be edited by anyone with admin access.

**Therefore**, this project aims to address the **"Intelligence Gap"** and the **"Trust Gap"** in home automation by building a system that self-verifies the identity of visitors and self-preserves the integrity of its logs.

---

## 1.7 Objectives

The specific technical goals of this project are:

1.  **To Implement Vision-Based Motion Detection**: Create a lightweight algorithm that monitors the environment and only triggers processing when activity is detected.
2.  **To Deploy Real-Time Face Authentication**: Integrate the LBPH algorithm to accurately identify "Authorized" users vs. "Unknown" intruders, including Liveness checks to reject photo attacks.
3.  **To Ensure Log Immutability**: Design a cryptographic blockchain structure where every new log entry contains the hash of the previous entry, preventing history rewriting.
4.  **To Automate Decision Making**: Develop a logic layer that instantly triggers simulated actuators (door locks) and sends **Email Alerts** upon detecting intruders.
5.  **To visualize System State**: Create a user-friendly Web Dashboard (Flask) that transparently displays both the live video feed and the blockchain ledger to the user.

---

## 1.8 Proposed Model / Methodology

The proposed solution is a **Multi-Layered Security Architecture**:

1.  **Sensing Layer (Input)**:
    *   **Methodology**: We utilize **Frame Differencing**. By comparing the current video frame $T$ with the previous frame $T-1$, we calculate the pixel delta. If $\Delta > Threshold$, the system wakes up.
    *   **Justification**: This "Event-Driven" approach saves massive amounts of CPU power compared to running deep learning models on empty hallways.

2.  **Processing Layer (Analysis)**:
    *   **Methodology**: We employ a **Cascade Classifier** for detection, **Eye Aspect Ratio** logic for Liveness detection (blinking), and **Histogram Analysis (LBPH)** for recognition.
    *   **Justification**: Unlike heavy Deep Learning models (like ResNet or VGG) that require powerful GPUs, LBPH is lightweight and works excellently for "One-Shot Learning" (learning a face from just a few photos), making it perfect for personal home devices.

3.  **Logging Layer (Storage)**:
    *   **Methodology**: We use a **SHA-256 Linked List** (Blockchain).
    *   **Novel Contribution**: Most smart homes use SQL databases. By using Blockchain, we introduce the concept of **"Forensic-Grade Logging"**—logs that can be used as verifiable evidence because their mathematical structure proves they haven't been altered.

4.  **Application Layer (Output)**:
    *   **Methodology**: A **Flask Web Server** pushes updates to the client using Server-Sent Events (SSE) or multipart streaming.
    *   **Justification**: This provides a platform-agnostic interface, allowing the user to monitor their home from a phone, tablet, or laptop without installing unmatched apps.
