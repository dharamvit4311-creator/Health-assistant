import streamlit as st
import pandas as pd
import math
from datetime import date, datetime
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a8a6b 0%, #0f5f4a 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.2rem; }
    .main-header p  { color: #c8f0e5; margin: 0.4rem 0 0; font-size: 1rem; }

    .feature-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .severity-critical { background:#fff0f0; border-left:4px solid #d32f2f; padding:1rem; border-radius:8px; }
    .severity-high     { background:#fff3e0; border-left:4px solid #f57c00; padding:1rem; border-radius:8px; }
    .severity-medium   { background:#e8f5e9; border-left:4px solid #388e3c; padding:1rem; border-radius:8px; }
    .severity-low      { background:#e3f2fd; border-left:4px solid #1976d2; padding:1rem; border-radius:8px; }

    .metric-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .metric-box .value { font-size: 1.8rem; font-weight: 700; color: #1a8a6b; }
    .metric-box .label { font-size: 0.8rem; color: #666; margin-top: 2px; }

    .diet-card {
        background: linear-gradient(135deg, #f0fff8 0%, #e8f8f2 100%);
        border: 1px solid #a8d8c8;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .diet-card h4 { color: #0f5f4a; margin: 0 0 0.3rem; }
    .diet-card p  { color: #2d6a4f; margin: 0; font-size: 0.95rem; }

    .tip-box {
        background: #fffde7;
        border: 1px solid #f9a825;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #5d4037;
    }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── Data loaders ─────────────────────────────────────────────────────────────
@st.cache_data
def load_symptoms():
    return pd.read_csv("symptoms_data.csv")

@st.cache_data
def load_diet():
    return pd.read_csv("diet_data.csv")

symptoms_df = load_symptoms()
diet_df     = load_diet()

ALL_SYMPTOMS = sorted(set(
    list(symptoms_df["symptom1"]) +
    list(symptoms_df["symptom2"]) +
    list(symptoms_df["symptom3"])
))

# ── Session state ─────────────────────────────────────────────────────────────
if "health_log" not in st.session_state:
    st.session_state.health_log = []
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "water_count" not in st.session_state:
    st.session_state.water_count = 0
if "steps" not in st.session_state:
    st.session_state.steps = 0

# ── Helper functions ──────────────────────────────────────────────────────────
def check_symptoms(selected):
    selected = [s.lower().strip() for s in selected]
    results = []
    for _, row in symptoms_df.iterrows():
        row_syms = {row["symptom1"].lower(), row["symptom2"].lower(), row["symptom3"].lower()}
        matches = len(set(selected) & row_syms)
        if matches >= 2:
            results.append({
                "condition": row["condition"],
                "advice":    row["advice"],
                "severity":  row["severity"],
                "matches":   matches,
            })
    results.sort(key=lambda x: x["matches"], reverse=True)
    return results[:3]

def calculate_bmi(weight_kg, height_cm):
    h = height_cm / 100
    bmi = weight_kg / (h * h)
    if bmi < 18.5:   cat = "underweight"
    elif bmi < 25:   cat = "normal"
    elif bmi < 30:   cat = "overweight"
    else:            cat = "overweight"
    return round(bmi, 1), cat

def get_diet_plan(goal, age, bmi_cat):
    df = diet_df[
        (diet_df["goal"] == goal) &
        (diet_df["age_min"] <= age) &
        (diet_df["age_max"] >= age) &
        (diet_df["bmi_category"] == bmi_cat)
    ]
    if df.empty:
        df = diet_df[
            (diet_df["goal"] == goal) &
            (diet_df["bmi_category"] == bmi_cat)
        ]
    if df.empty:
        df = diet_df[diet_df["goal"] == goal]
    return df.iloc[0] if not df.empty else None

def severity_color(sev):
    return {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(sev, "⚪")

HEALTH_TIPS = [
    "💧 Drink at least 8 glasses of water every day.",
    "🚶 Walk for 30 minutes daily to boost your heart health.",
    "🛌 Aim for 7–8 hours of sleep every night.",
    "🥗 Eat 5 servings of fruits and vegetables daily.",
    "🧘 Practice 10 minutes of deep breathing or meditation.",
    "🚫 Avoid smoking and limit alcohol consumption.",
    "🩺 Get a full body check-up at least once a year.",
    "📵 Reduce screen time 1 hour before bedtime.",
    "🌞 Get 15–20 minutes of sunlight daily for Vitamin D.",
    "😁 Wash your hands for 20 seconds to prevent infections.",
]

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h1>🏥 AI Health Assistant</h1>
    <p>Your personal AI-powered guide for symptoms, diet, and daily wellness</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    user_name   = st.text_input("Your name", placeholder="Enter your name")
    user_age    = st.number_input("Age (years)", min_value=5, max_value=100, value=17)
    user_weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=60)
    user_height = st.number_input("Height (cm)", min_value=100, max_value=220, value=165)

    if user_weight and user_height:
        bmi_val, bmi_cat = calculate_bmi(user_weight, user_height)
        bmi_color = {"underweight": "#2196f3", "normal": "#4caf50", "overweight": "#ff9800"}.get(bmi_cat, "#666")
        st.markdown(f"""
        <div style="background:#f0fff8;border:1px solid #a8d8c8;border-radius:8px;padding:0.8rem;margin-top:0.5rem;text-align:center">
            <div style="font-size:1.6rem;font-weight:700;color:{bmi_color}">{bmi_val}</div>
            <div style="font-size:0.75rem;color:#666">BMI — <strong>{bmi_cat.capitalize()}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💡 Daily Health Tip")
    tip_idx = date.today().toordinal() % len(HEALTH_TIPS)
    st.info(HEALTH_TIPS[tip_idx])

    st.markdown("---")
    st.markdown("### 📊 Today's Tracker")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💧 +1 Glass"):
            st.session_state.water_count += 1
    with col2:
        if st.button("🚶 +500 Steps"):
            st.session_state.steps += 500

    st.markdown(f"""
    <div style="display:flex;gap:8px;margin-top:6px">
        <div class="metric-box" style="flex:1">
            <div class="value">{st.session_state.water_count}</div>
            <div class="label">Glasses of water</div>
        </div>
        <div class="metric-box" style="flex:1">
            <div class="value">{st.session_state.steps:,}</div>
            <div class="label">Steps today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Symptom Checker",
    "🥗 Diet Advisor",
    "⏰ Health Reminders",
    "📋 Health Dashboard",
])

# ─── TAB 1: SYMPTOM CHECKER ───────────────────────────────────────────────────
with tab1:
    st.markdown("## 🩺 Symptom Checker")
    st.markdown("Select **2 or more symptoms** you are experiencing. The AI will identify possible conditions and advise you.")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        selected_symptoms = st.multiselect(
            "Choose your symptoms:",
            options=ALL_SYMPTOMS,
            placeholder="Type or select symptoms...",
        )
        custom_symptom = st.text_input("Can't find your symptom? Type it below:", placeholder="e.g. blurred vision")

    with col_b:
        st.markdown("#### ℹ️ How it works")
        st.markdown("""
        1. Select symptoms from the list
        2. Click **Analyse**
        3. Get possible conditions & advice
        4. ⚠️ Always consult a real doctor for diagnosis
        """)

    if st.button("🔍 Analyse Symptoms", type="primary", use_container_width=True):
        all_selected = selected_symptoms[:]
        if custom_symptom.strip():
            all_selected.append(custom_symptom.strip().lower())

        if len(all_selected) < 2:
            st.warning("⚠️ Please select at least 2 symptoms for a meaningful analysis.")
        else:
            results = check_symptoms(all_selected)
            st.markdown("---")
            if not results:
                st.info("ℹ️ No strong match found for the selected combination. Please consult a doctor for a proper diagnosis.")
            else:
                st.markdown(f"### 🔎 Results for: `{', '.join(all_selected)}`")
                for i, r in enumerate(results):
                    sev_class = f"severity-{r['severity'].lower()}"
                    icon = severity_color(r["severity"])
                    st.markdown(f"""
                    <div class="{sev_class}" style="margin-bottom:1rem">
                        <h4 style="margin:0 0 0.4rem">{icon} {r['condition']}</h4>
                        <p style="margin:0 0 0.3rem"><strong>Severity:</strong> {r['severity']}</p>
                        <p style="margin:0"><strong>Advice:</strong> {r['advice']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.session_state.health_log.append({
                    "date":      datetime.now().strftime("%d %b %Y, %H:%M"),
                    "type":      "Symptom Check",
                    "detail":    f"Symptoms: {', '.join(all_selected)} → {results[0]['condition']}",
                })

                st.markdown("""
                <div class="tip-box">
                ⚠️ <strong>Disclaimer:</strong> This tool provides general health information only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified doctor.
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 All Symptoms in Database")
    with st.expander("View all symptoms this assistant can analyse"):
        cols = st.columns(4)
        for i, sym in enumerate(ALL_SYMPTOMS):
            cols[i % 4].markdown(f"• {sym.capitalize()}")

# ─── TAB 2: DIET ADVISOR ─────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🥗 Personalised Diet Advisor")
    st.markdown("Enter your details to receive a customised daily meal plan.")

    col1, col2, col3 = st.columns(3)
    with col1:
        d_age    = st.number_input("Age", min_value=5, max_value=80, value=int(user_age), key="d_age")
    with col2:
        d_weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=int(user_weight), key="d_wt")
    with col3:
        d_height = st.number_input("Height (cm)", min_value=100, max_value=220, value=int(user_height), key="d_ht")

    d_goal = st.radio(
        "Health Goal:",
        options=["weight_loss", "weight_gain", "maintenance"],
        format_func=lambda x: {"weight_loss": "⬇️ Lose Weight", "weight_gain": "⬆️ Gain Weight", "maintenance": "✅ Maintain Weight"}[x],
        horizontal=True,
    )

    if st.button("🥦 Get My Diet Plan", type="primary", use_container_width=True):
        bmi_v, bmi_c = calculate_bmi(d_weight, d_height)
        plan = get_diet_plan(d_goal, d_age, bmi_c)

        st.markdown("---")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Your BMI", bmi_v)
        col_m2.metric("BMI Category", bmi_c.capitalize())
        col_m3.metric("Daily Calorie Target", f"{plan['calories']} kcal" if plan is not None else "N/A")

        if plan is not None:
            st.markdown("### 🍽️ Your Daily Meal Plan")

            meals = [
                ("🌅 Breakfast", plan["breakfast"]),
                ("☀️ Lunch",     plan["lunch"]),
                ("🌙 Dinner",    plan["dinner"]),
                ("🍎 Snacks",    plan["snack"]),
            ]
            for meal_name, meal_desc in meals:
                st.markdown(f"""
                <div class="diet-card">
                    <h4>{meal_name}</h4>
                    <p>{meal_desc}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="tip-box">
            🚫 <strong>Foods to avoid:</strong> {plan['avoid']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 💧 Hydration & Exercise Tips")
            tips_col1, tips_col2 = st.columns(2)
            with tips_col1:
                st.success("💧 Drink 8–10 glasses of water daily")
                st.success("🚶 Walk 30 minutes every day")
            with tips_col2:
                st.success("🛌 Sleep 7–8 hours every night")
                st.success("🧘 Avoid stress — try yoga or meditation")

            st.session_state.health_log.append({
                "date":   datetime.now().strftime("%d %b %Y, %H:%M"),
                "type":   "Diet Plan",
                "detail": f"Goal: {d_goal}, BMI: {bmi_v} ({bmi_c}), Calories: {plan['calories']}",
            })
        else:
            st.warning("No diet plan found for this combination. Try adjusting your inputs.")

# ─── TAB 3: HEALTH REMINDERS ─────────────────────────────────────────────────
with tab3:
    st.markdown("## ⏰ Health Reminders")
    st.markdown("Set reminders for your daily health habits. These will appear in your dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        reminder_type = st.selectbox(
            "Reminder type:",
            ["💧 Drink Water", "💊 Take Medication", "🏃 Exercise", "🛌 Sleep Time", "🍎 Eat Healthy Snack", "🧘 Meditation / Breathing", "📏 Check Weight", "Custom"]
        )
        if reminder_type == "Custom":
            reminder_type = st.text_input("Enter custom reminder:")
    with col2:
        reminder_time  = st.time_input("Reminder time:")
        reminder_notes = st.text_input("Notes (optional):", placeholder="e.g. 2 tablets after food")

    if st.button("➕ Add Reminder", type="primary"):
        if reminder_type:
            st.session_state.reminders.append({
                "type":  reminder_type,
                "time":  reminder_time.strftime("%I:%M %p"),
                "notes": reminder_notes,
                "done":  False,
            })
            st.success(f"✅ Reminder added: **{reminder_type}** at **{reminder_time.strftime('%I:%M %p')}**")

    st.markdown("---")
    st.markdown("### 📋 Your Reminders")

    if not st.session_state.reminders:
        st.info("No reminders set yet. Add one above!")
    else:
        for i, r in enumerate(st.session_state.reminders):
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                status = "✅" if r["done"] else "🔔"
                st.markdown(f"**{status} {r['type']}** — _{r['time']}_")
                if r["notes"]:
                    st.caption(f"📝 {r['notes']}")
            with col_b:
                if st.button("Done", key=f"done_{i}"):
                    st.session_state.reminders[i]["done"] = True
                    st.rerun()
            with col_c:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.reminders.pop(i)
                    st.rerun()

    st.markdown("---")
    st.markdown("### 🌟 Suggested Daily Routine")
    routine = [
        ("6:00 AM",  "🌅 Wake up & drink 1 glass warm water"),
        ("7:00 AM",  "🧘 10 min yoga / stretching"),
        ("8:00 AM",  "🍳 Nutritious breakfast"),
        ("10:00 AM", "💧 Drink water"),
        ("1:00 PM",  "🥗 Healthy lunch"),
        ("4:00 PM",  "🍎 Light snack + water"),
        ("6:00 PM",  "🚶 30 min walk / exercise"),
        ("8:00 PM",  "🍽️ Light dinner"),
        ("10:00 PM", "📵 No screens — prepare for sleep"),
        ("10:30 PM", "🛌 Sleep (7–8 hours)"),
    ]
    for time_str, activity in routine:
        st.markdown(f"**`{time_str}`** — {activity}")

# ─── TAB 4: DASHBOARD ────────────────────────────────────────────────────────
with tab4:
    st.markdown("## 📋 Health Dashboard")
    name_display = user_name if user_name else "User"
    st.markdown(f"### Welcome, {name_display}! Here's your health summary.")

    bmi_v2, bmi_c2 = calculate_bmi(user_weight, user_height)
    water_goal = 8
    water_pct  = min(int((st.session_state.water_count / water_goal) * 100), 100)
    steps_goal = 6000
    steps_pct  = min(int((st.session_state.steps / steps_goal) * 100), 100)

    st.markdown("### 📊 Today's Stats")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BMI", bmi_v2, bmi_c2.capitalize())
    m2.metric("Water", f"{st.session_state.water_count}/{water_goal} glasses", f"{water_pct}% of goal")
    m3.metric("Steps", f"{st.session_state.steps:,}", f"{steps_pct}% of {steps_goal:,} goal")
    m4.metric("Reminders set", len(st.session_state.reminders), f"{sum(1 for r in st.session_state.reminders if r['done'])} done")

    st.markdown("---")
    st.markdown("### 🎯 Goal Progress")
    st.markdown(f"**💧 Water intake:** {st.session_state.water_count}/{water_goal} glasses")
    st.progress(water_pct / 100)
    st.markdown(f"**🚶 Steps:** {st.session_state.steps:,}/{steps_goal:,}")
    st.progress(steps_pct / 100)

    st.markdown("---")
    st.markdown("### 📝 Activity Log")
    if not st.session_state.health_log:
        st.info("No activity yet. Use the Symptom Checker or Diet Advisor to start logging.")
    else:
        log_df = pd.DataFrame(st.session_state.health_log)
        st.dataframe(log_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🧠 AI in Healthcare — About This Project")
    with st.expander("Read the project explanation"):
        st.markdown("""
        #### What is AI in Healthcare?
        Artificial Intelligence in healthcare uses machine learning, natural language processing,
        and data analysis to assist in medical decision-making, patient care, and health management.

        #### AI Techniques Used in This Project
        | Feature | AI Technique |
        |---|---|
        | Symptom checker | NLP keyword matching + Rule-based logic |
        | Diet advisor | Rule-based AI + BMI calculation |
        | Health reminders | Scheduling logic |
        | Dashboard | Data analysis + visualisation |

        #### Benefits
        - Available 24/7 — no waiting time
        - Reduces unnecessary hospital visits
        - Promotes healthy lifestyle habits
        - Personalised advice for each user

        #### Limitations
        - Cannot replace a real doctor
        - Limited to the symptoms in its dataset
        - No physical examination possible
        - Risk of misdiagnosis for rare conditions

        #### Ethical Considerations
        - User health data must be kept private
        - AI must clearly state it is not a medical professional
        - Outputs should always recommend consulting a doctor
        """)

    st.markdown("---")
    st.caption("⚠️ Disclaimer: This AI Health Assistant is a student capstone project for educational purposes only. It is not a medical device and should not be used for actual medical diagnosis or treatment.")
