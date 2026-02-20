import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Blood Pressure Load Simulator", page_icon="🩺", layout="centered")

st.title("🩺 What Moves Blood Pressure?")
st.caption("Adjust the habits below to see how they can influence **blood pressure strain** on the body.")

with st.expander("Important note (read this)", expanded=False):
    st.write(
        "**Educational tool only.** This shows relative impact (trend), not a diagnosis or a prediction of your actual blood pressure. "
        "People respond differently based on baseline health, medications, and genetics."
    )

# --- Inputs ---
st.subheader("Adjust the levers")

col1, col2 = st.columns(2)

with col1:
    exercise_days = st.slider("Exercise days per week", 0, 7, 2)
    sleep_hours = st.slider("Sleep (hours/night)", 4.0, 9.5, 7.0, 0.5)
    stress = st.slider("Stress level (0–10)", 0, 10, 5)

with col2:
    nicotine = st.toggle("Smoking / Nicotine use", value=False)
    processed = st.selectbox("Highly processed foods", ["Rarely", "Some days", "Most days"], index=1)

# --- Scoring model (educational/illustrative) ---
# Higher score = more "BP load"/strain
def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))

# Exercise points: more exercise reduces load
if exercise_days == 0:
    ex_pts = 10
elif exercise_days == 1:
    ex_pts = 7
elif exercise_days == 2:
    ex_pts = 5
elif exercise_days == 3:
    ex_pts = 3
elif exercise_days in (4, 5):
    ex_pts = 1
else:  # 6-7
    ex_pts = 0

# Sleep points: below 7 increases load; 7–8 neutral; >8 slightly beneficial
if sleep_hours < 7:
    sl_pts = (7 - sleep_hours) * 4  # up to ~12
elif sleep_hours <= 8:
    sl_pts = 0
else:
    sl_pts = -1

# Nicotine points
nic_pts = 12 if nicotine else 0

# Processed food points
pf_pts = {"Most days": 8, "Some days": 4, "Rarely": 0}[processed]

# Stress points
st_pts = round(stress * 1.6)  # up to ~16

load = clamp(20 + ex_pts + sl_pts + nic_pts + pf_pts + st_pts)

# --- Categorization ---
if load <= 33:
    zone = "Lower strain"
    color = "#2E7D32"
    insight = "Nice work—this mix of habits generally supports healthier blood pressure and blood vessels."
elif load <= 66:
    zone = "Moderate strain"
    color = "#F9A825"
    insight = "You’ve got some protective habits in place. One small change could meaningfully improve the trend."
else:
    zone = "Higher strain"
    color = "#C62828"
    insight = "This combination can increase strain on blood vessels. The good news: changing just one lever can shift the odds."

# --- Biggest opportunity (simple priority logic) ---
if nicotine:
    opportunity = "Biggest opportunity: reducing nicotine use (benefits can happen quickly)."
elif sleep_hours < 7:
    opportunity = "Biggest opportunity: improving sleep by +30–60 minutes consistently."
elif exercise_days < 3:
    opportunity = "Biggest opportunity: add movement—10-minute walks count."
elif processed == "Most days":
    opportunity = "Biggest opportunity: swap one processed food per day for a whole-food option."
elif stress >= 7:
    opportunity = "Biggest opportunity: stress recovery—try 2 minutes of slow exhale breathing."
else:
    opportunity = "You’re doing several things that support healthier blood pressure—keep building on what’s working."

# --- Gauge ---
st.subheader("Blood Pressure Load Gauge")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=load,
        number={"suffix": " / 100"},
        title={"text": f"<b>{zone}</b>"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 33], "color": "#E8F5E9"},
                {"range": [33, 66], "color": "#FFF8E1"},
                {"range": [66, 100], "color": "#FFEBEE"},
            ],
            "threshold": {"line": {"color": "#444", "width": 3}, "thickness": 0.75, "value": load},
        },
    )
)
fig.update_layout(margin=dict(l=20, r=20, t=60, b=10), height=320)
st.plotly_chart(fig, use_container_width=True)

# --- Text outputs ---
st.markdown(f"**Insight:** {insight}")
st.markdown(f"**{opportunity}**")

st.divider()
st.caption("Educational tool only. Not intended to diagnose, treat, or replace medical care.")
