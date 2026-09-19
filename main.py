import cv2
import mediapipe as mp
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3

# 🔊 Voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# 👁️ Face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Eye landmark points
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(landmarks, eye_indices, w, h):
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
    
    A = ((points[1][1] - points[5][1])**2 + (points[1][0] - points[5][0])**2)**0.5
    B = ((points[2][1] - points[4][1])**2 + (points[2][0] - points[4][0])**2)**0.5
    C = ((points[0][1] - points[3][1])**2 + (points[0][0] - points[3][0])**2)**0.5
    
    return (A + B) / (2.0 * C)

# 🎥 Camera
cap = cv2.VideoCapture(0)

# 📊 Variables
blink_count = 0
frame_counter = 0
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 2

start_time = time.time()
last_blink_time = time.time()
session_start_time = time.time()

# 📁 CSV
file = open("study_data.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["Time(s)", "Blinks", "Blink Rate"])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    
    current_time = time.time()
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            
            # 👁️ EAR calculation
            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
            ear = (left_ear + right_ear) / 2
            
            # 👁️ Blink detection
            if ear < EAR_THRESHOLD:
                frame_counter += 1
            else:
                if frame_counter >= CONSEC_FRAMES:
                    blink_count += 1
                    last_blink_time = current_time
                frame_counter = 0
            
            # ⏱ Blink rate
            elapsed_time = current_time - start_time
            blink_rate = (blink_count / elapsed_time) * 60 if elapsed_time > 0 else 0
            
            # 📁 Save CSV
            writer.writerow([int(elapsed_time), blink_count, int(blink_rate)])
            
            # 🎯 STATUS SYSTEM
            status = "NORMAL"
            color = (0, 255, 255)  # Yellow
            
            if 15 <= blink_rate <= 20:
                status = "FOCUSED"
                color = (0, 255, 0)  # Green
            elif 10 <= blink_rate < 15:
                status = "NORMAL"
                color = (0, 255, 255)
            elif blink_rate < 10:
                status = "DISTRACTED"
                color = (0, 0, 255)  # Red
            
            # 😴 Drowsiness override
            if current_time - last_blink_time > 5:
                status = "DROWSY"
                color = (0, 0, 255)
                cv2.putText(frame, "DROWSINESS ALERT!", (100,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                speak("Wake up!")
            
            # ⏳ Study time
            study_time = current_time - session_start_time
            
            # ⚠️ Break reminder
            if study_time > 30:
                cv2.putText(frame, "TAKE A BREAK!", (100,300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)
                speak("Please take a break")
                session_start_time = current_time
            
            # 👁️ Eye strain
            if blink_rate < 10 and study_time > 10:
                cv2.putText(frame, "EYE STRAIN DETECTED!", (100,250),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
            
            # 📺 DISPLAY
            cv2.putText(frame, f"Blinks: {blink_count}", (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            
            cv2.putText(frame, f"Rate: {int(blink_rate)}", (30,90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
            
            cv2.putText(frame, f"Status: {status}", (30,130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            
            # 🎨 Box UI
            cv2.rectangle(frame, (20,20), (320,160), color, 3)

    cv2.imshow("Smart Study Analyzer", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 🛑 Cleanup
cap.release()
cv2.destroyAllWindows()
file.close()

# 🔥 AUTO ANALYSIS

data = pd.read_csv("study_data.csv")
avg_blink_rate = data["Blink Rate"].mean()

print(f"\nAverage Blink Rate: {int(avg_blink_rate)}")

if 15 <= avg_blink_rate <= 20:
    focus_score = 90
    message = "Excellent focus"
elif 10 <= avg_blink_rate < 15:
    focus_score = 75
    message = "Good focus"
elif avg_blink_rate < 10:
    focus_score = 60
    message = "Low focus, eye strain"
else:
    focus_score = 70
    message = "Distraction detected"

print(f"Focus Score: {focus_score}/100")
print(message)

speak(f"Your focus score is {focus_score}. {message}")

# 📈 Graph
plt.plot(data["Time(s)"], data["Blink Rate"])
plt.xlabel("Time (seconds)")
plt.ylabel("Blink Rate")
plt.title("Focus Analysis")
plt.grid()
plt.show()