# Module 4: Blockchain-Secured Logging

## 1. Overview
In standard systems, logs are text files that can be edited. A hacker could delete their "Intruder" entry.
In this project, we implement a **Private Blockchain**. Every security event (Entry/Intrusion) is a "Block" cryptographically linked to the previous one.

## 2. Core Concepts (Viva)
-   **Immutable**: Once written, data cannot be changed.
-   **SHA-256**: The hashing algorithm used.
-   **Genesis Block**: The first block in the chain (Index 0).
-   **Tamper Evidence**: If anyone modifies a past block, all subsequent hashes change, breaking the chain.

## 3. Data Structure
Each Block contains:
```json
{
    "index": 1,
    "timestamp": 1734567890.0,
    "data": {"event": "INTRUSION", "person": "Unknown"},
    "previous_hash": "a1b2c3d4...",
    "hash": "e5f6g7h8..."
}
```

## 4. How to Test
1.  Run `python src/secure_logger.py`
2.  It will create a chain and add 2 valid blocks.
3.  It will then simulate a **"Hacking Attack"** by manually modifying data in memory.
4.  The system will output `[ALERT] Data tampering detected!` and `Is chain valid? False`.
    **This proves the security feature.**
