# 📊 Smart Study Analyzer

## 📌 Overview

Smart Study Analyzer is a real-time AI-based system that monitors user attention using eye blink detection through a webcam.
It analyzes blink patterns to detect **focus, distraction, drowsiness, and eye strain**, and provides alerts and feedback.

---

## 🎯 Features

* 👁️ Real-time Blink Detection
* ⏱️ Blink Rate Calculation
* 🧠 Focus Level Classification (Focused / Normal / Distracted / Drowsy)
* 😴 Drowsiness Alert
* ⚠️ Eye Strain Detection
* ⏳ Break Reminder System
* 🔊 Voice Feedback (Text-to-Speech)
* 📁 Data Logging (CSV file)
* 📈 Automatic Graph Analysis

---

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* Pandas
* Matplotlib
* pyttsx3

---

## ▶️ How to Run (CMD Steps)

### Step 1: Open Command Prompt

Press:
Win + R → type `cmd` → Enter

---

### Step 2: Go to Project Folder

```
cd C:\Users\PREM\SmartStudyAnalyzer
```

---

### Step 3: Activate Virtual Environment

```
venv\Scripts\activate
```

---

### Step 4: Run the Program

```
python main.py
```

---

## 🧪 How it Works

1. Webcam captures live video
2. MediaPipe detects face and eye landmarks
3. Eye Aspect Ratio (EAR) is calculated
4. Blinks are detected based on EAR threshold
5. Blink rate is computed per minute
6. System classifies user into:

   * 🟢 Focused
   * 🟡 Normal
   * 🔴 Distracted / Drowsy
7. Alerts are generated for:

   * Drowsiness
   * Eye strain
   * Break reminder
8. Data is stored in `study_data.csv`
9. After stopping (ESC), system:

   * Calculates focus score
   * Gives voice feedback
   * Displays graph

---

## 📁 Output Files

* `study_data.csv` → Stores blink data
* Graph → Shows blink rate over time
* Console Output → Focus score & analysis

---

## 💡 Applications

* 📚 Student focus monitoring
* 💻 Productivity tracking
* 🚗 Driver drowsiness detection
* 👨‍💻 Eye health awareness

---

## 🚀 Future Improvements

* GUI Dashboard
* Mobile App Integration
* Advanced AI Models
* Cloud Data Storage

---

## 🧠 Conclusion

This project demonstrates how computer vision and AI can be used to monitor human attention and health in real time, improving productivity and reducing eye strain.

---

## 👨‍💻 Author

Prem Pardeshi
R.I.D.E Project
