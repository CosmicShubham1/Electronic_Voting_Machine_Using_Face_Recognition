# 🗳️ Smart EVM: Electronic Voting Machine with Face Recognition

![Project Status](https://img.shields.io/badge/Status-Prototype_Complete-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Tech-Arduino_%7C_Python_%7C_OpenCV-blue?style=for-the-badge)

A secure, dual-authentication voting system designed to eliminate identity fraud and duplicate voting. This project integrates **Biometric Verification (Face Recognition)** with hardware-based voting controls to ensure a transparent and tamper-proof election process in offline environments.

---

## 📸 Project Preview

![EVM Setup](evm_preview.jpg)
*(Note: Upload your project image to the repository and name it 'evm_preview.jpg')*

---

## 🚀 Key Features

* **👤 Biometric Authentication:** Utilizes OpenCV (Haar Cascade & LBPH) to verify voter identity against a pre-registered database.
* **🔒 Dual-Layer Security:** Requires both a unique **Voter ID** and a successful **Face Match** (Confidence Threshold: 50-70) to unlock the voting interface.
* **🚫 Anti-Duplicate Voting:** Automatically locks the Voter ID immediately after a vote is cast, physically preventing repeated attempts.
* **🔌 Hardware-Software Bridge:** Seamless serial communication between the Python backend (Authentication) and Arduino (Control Logic).
* **📝 Secure Audit Trail:** Logs every vote (Voter ID + Candidate + Timestamp) into immutable local text files for post-election auditing.
* **💡 Real-Time Feedback:** Visual LED confirmation ensures the voter knows their vote was successfully recorded.

---

## 🛠️ Tech Stack & Hardware

### **Software**
* **Language:** Python 3.x, C++ (Arduino)
* **Libraries:** `OpenCV` (Computer Vision), `PySerial` (Communication), `Tkinter` (GUI - Optional)
* **Algorithm:** LBPH (Local Binary Patterns Histograms) Face Recognizer

### **Hardware Components**
| Component | Function |
| :--- | :--- |
| **Arduino Uno** | Central microcontroller (ATmega328P) for logic control. |
| **Webcam** | Captures real-time facial data for authentication. |
| **Push Buttons (x3)** | Physical interface for selecting Candidates A, B, or C. |
| **Red LED** | Provides visual confirmation of a successful vote. |
| **Laptop/PC** | Runs the Python recognition script and stores the database. |

---

## 🔌 Circuit Diagram & Pinout

The hardware is connected to the Arduino Uno as follows:

| Component | Arduino Pin | Description |
| :--- | :---: | :--- |
| **LED Indicator** | `D6` | Connected via 220Ω resistor (Anode). |
| **Candidate 1 Button** | `D8` | Input for Candidate A (Internal Pull-up). |
| **Candidate 2 Button** | `D9` | Input for Candidate B (Internal Pull-up). |
| **Candidate 3 Button** | `D10` | Input for Candidate C (Internal Pull-up). |
| **Serial Comms** | `TX/RX` | USB communication with the host laptop. |

> **Note:** All buttons connect one terminal to the Digital Pin and the other to **GND**.

---

## ⚙️ Installation & Setup

### 1. Hardware Setup
1.  Assemble the circuit according to the pinout table above.
2.  Connect the Arduino Uno to your PC via USB.

### 2. Arduino Firmware
1.  Open `EVM_Firmware.ino` in the Arduino IDE.
2.  Select the correct **Board** (Arduino Uno) and **Port**.
3.  Upload the code.

### 3. Python Environment
1.  Install the required dependencies:
    ```bash
    pip install opencv-contrib-python pyserial numpy
    ```
2.  **Register Voters:** Run `create_dataset.py` to capture face samples for new IDs.
3.  **Train Model:** Run `train_model.py` to generate the `trainer.yml` file.

### 4. Run the System
Execute the main script to start the voting machine:
```bash
python main_evm.py
🗳️ Workflow
Initialization: System loads the database and trains the recognizer.

Login: Voter enters their unique Voter ID.

Scan: Webcam activates to verify the face.

Match Found: Access Granted → Arduino unlocks buttons.

Mismatch: Access Denied.

Vote: User presses a physical button (Candidate 1, 2, or 3).

Confirmation: LED blinks, and the vote is logged with a timestamp.

Lock: The system locks the user ID to prevent re-voting.

🔮 Future Scope
Cloud Sync: Real-time data backup to a secure cloud server (e.g., Firebase/AWS).

Multi-Factor Auth: Adding Fingerprint verification for higher security.

Touch Interface: Replacing physical buttons with a touchscreen UI.

👨‍💻 Developer
Shubham Kumar

<p align="center">Made with ❤️ for Secure Democracy</p>
