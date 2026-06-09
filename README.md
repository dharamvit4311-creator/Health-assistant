# 🏥 AI-Powered Health Assistant
### AI Capstone Project | Class 10–12 | Subject: Artificial Intelligence

---

## 📌 Project Overview

An AI-powered health assistant that helps users:
- **Check symptoms** and get possible conditions with severity levels
- **Get a personalised diet plan** based on age, BMI, and health goal
- **Set health reminders** for water, medication, exercise, and sleep
- **Track daily health stats** on a live dashboard

---

## 🤖 AI Domain Used

| Feature | AI Technique |
|---|---|
| Symptom Checker | NLP keyword matching + Rule-based logic |
| Diet Advisor | Rule-based AI + BMI calculation algorithm |
| Health Reminders | Scheduling logic |
| Dashboard | Data analysis + visualisation |

---

## 🛠️ Technologies Used

- **Language:** Python 3.x
- **Framework:** Streamlit (web UI)
- **Libraries:** Pandas (data handling)
- **Data:** Custom CSV datasets (symptoms + diet)

---

## 📁 Project Structure

```
health_assistant/
│
├── app.py               ← Main Streamlit application
├── symptoms_data.csv    ← 20 symptom-disease records
├── diet_data.csv        ← 8 diet plan rules
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## ▶️ How to Run

### Step 1 — Install Python
Download Python 3.10+ from https://python.org

### Step 2 — Install dependencies
Open terminal / command prompt in the project folder and run:
```bash
pip install streamlit pandas
```

### Step 3 — Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🌐 Deploy Online (Free) — Get Your Project URL

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Upload this project to a GitHub repository
4. Connect your repo in Streamlit Cloud
5. Click **Deploy** — you get a live URL!

---

## ✨ Features

### 🩺 Symptom Checker
- Select 2+ symptoms from a dropdown list
- AI matches them to 20+ known conditions
- Shows severity level (Low / Medium / High / Critical)
- Gives specific advice for each condition

### 🥗 Diet Advisor
- Calculates BMI automatically
- Recommends breakfast, lunch, dinner, and snacks
- Based on your age, weight, height, and goal
- Shows calorie target and foods to avoid

### ⏰ Health Reminders
- Add reminders for water, medicine, exercise, sleep
- Set a specific time for each reminder
- Mark reminders as done
- Includes a suggested daily routine

### 📊 Dashboard
- Live water intake tracker (click to add glasses)
- Step counter
- Activity log showing all symptom checks and diet plans
- BMI display with category

---

## 📊 Sample Output

**Symptom Check:**
> Input: fever, headache, body ache
> Result: Viral Fever (Medium severity)
> Advice: Rest and drink fluids. Take paracetamol. See doctor if fever > 103°F.

**Diet Plan:**
> Input: Age 17, 60kg, 165cm, goal: weight loss
> BMI: 22.0 (Normal) | Calories: 1600/day
> Breakfast: Oats with banana + 1 glass milk

---

## ✅ Advantages
- Available 24/7, no waiting time
- Reduces unnecessary hospital visits
- Promotes healthy daily habits
- Personalised advice for each user
- Free and easy to use

## ⚠️ Limitations
- Cannot replace a real doctor
- Limited to symptoms in its dataset
- No physical examination possible
- Risk of misdiagnosis for rare conditions
- User health data privacy must be ensured

---

## 🔒 Disclaimer
This project is built for **educational purposes only** as part of an AI capstone assignment.
It is **not** a medical device and should not be used for actual medical diagnosis or treatment.
Always consult a qualified doctor for health concerns.

---

*Built with Python + Streamlit | AI Capstone Project*
