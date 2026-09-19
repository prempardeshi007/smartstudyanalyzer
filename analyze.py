import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3

# Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load CSV data
try:
    data = pd.read_csv("study_data.csv")
except:
    print("Error: study_data.csv not found. Run main.py first.")
    exit()

# Plot graph
plt.figure()
plt.plot(data["Time(s)"], data["Blink Rate"])
plt.xlabel("Time (seconds)")
plt.ylabel("Blink Rate (per minute)")
plt.title("Focus Analysis")
plt.grid()

# Calculate average blink rate
avg_blink_rate = data["Blink Rate"].mean()

print(f"\nAverage Blink Rate: {int(avg_blink_rate)} blinks/min")

# Focus score logic
if 15 <= avg_blink_rate <= 20:
    focus_score = 90
    message = "Excellent focus"
elif 10 <= avg_blink_rate < 15:
    focus_score = 75
    message = "Good focus"
elif avg_blink_rate < 10:
    focus_score = 60
    message = "Low focus, you may be tired"
else:
    focus_score = 70
    message = "Over blinking, possible distraction"

# Output
print(f"Focus Score: {focus_score}/100")
print(f"Analysis: {message}")

# Voice output
speak(f"Your focus score is {focus_score}. {message}")

# Show graph at END
plt.show()