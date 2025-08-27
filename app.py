import streamlit as st
import pandas as pd
import pickle
from datetime import date

# -------------------------
# Load Model
# -------------------------
model = pickle.load(open('D:\Guvi projects\YoutubeAdRevProject\Models\poly_LR_model.pkl', 'rb'))

# ----------------------------------------------------
# Streamlit Page Config
# ----------------------------------------------------
st.set_page_config(
    page_title="YouTube Revenue Prediction",
    page_icon="📊",
    layout="centered"
)

# ----------------------------------------------------
# Custom CSS for Background + Effects
# ----------------------------------------------------
youtube_logo_path = "D:\Guvi projects\YoutubeAdRevProject\youtube-logo-png-photo-0.png"
page_bg = """
<style>
/* Background */
.stApp {
    background-image: linear-gradient(to right, #141E30, #243B55);
    background-size: cover;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Titles */
h1, h2, h3, h4 {
    color: #FFD700 !important;
    text-shadow: 1px 1px 4px black;
}

/* Input fields */
div[data-baseweb="input"] input {
    background-color: #f8f9fa;
    color: black;
    border-radius: 10px;
    padding: 8px;
}

/* Labels */
.stNumberInput label,
.stSelectbox label,
.stDateInput label {
    color: #FFD700 !important;   /* Change this color */
    font-weight: bold;
    font-size: 16px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(45deg, #ff4b2b, #ff416c);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    transition: all 0.3s ease;
    border: none;
}
.stButton button:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #ff6a00, #ee0979);
}

/* Result Box */
div[data-testid="stSuccess"] {
    background: rgba(0, 255, 127, 0.15);
    border: 2px solid #00FF7F;
    border-radius: 12px;
    padding: 15px;
    color: #00FF7F !important;
    font-weight: bold;
    text-align: center;
    font-size: 20px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------------------------------------
# Title
# ----------------------------------------------------
col1, col2 = st.columns([2, 10])  # adjust ratio for spacing

with col1:
    st.image(youtube_logo_path, width=100)  # logo on left

with col2:
    st.title("YouTube Ad Revenue Prediction")  # title on right
    st.write("Enter your video details to estimate the ad revenue.")

# ----------------------------------------------------
# User Inputs
# ----------------------------------------------------
st.subheader("🎥 Video Information")

# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    views = st.number_input("Views", min_value=0, step=100, format="%d")
with col2:
    likes = st.number_input("Likes", min_value=0, step=10, format="%d")
with col3:
    comments = st.number_input("Comments", min_value=0, step=5, format="%d")

# Row 2
col4, col5, col6 = st.columns(3)
with col4:
    watch_time_minutes = st.number_input("Watch Time (minutes)", min_value=0.0, step=10.0, format="%.1f")
with col5:
    subscribers = st.number_input("Subscribers", min_value=0, step=10, format="%d")
with col6:
    upload_date = st.date_input("Video Upload Date", min_value=date(2005, 1, 1), max_value=date.today())

# Row 3
col7, col8, col9 = st.columns(3)
with col7:
    category = st.selectbox("Category", ["Education", "Music", "Tech", "Entertainment", "Gaming", "Lifestyle"])
with col8:
    device = st.selectbox("Device", ["TV", "Mobile", "Desktop", "Tablet"])
with col9:
    country = st.selectbox("Country", ["CA", "DE", "IN", "AU", "UK", "US"])

# ----------------------------------------------------
# Feature Engineering
# ----------------------------------------------------
watch_time_days = watch_time_minutes / 1440 
day_name = upload_date.strftime("%A")

engagement_rate = (likes + comments) / views if views > 0 else 0
sub_engagement = (likes + comments) / subscribers if subscribers > 0 else 0

input_data = pd.DataFrame({
    "watch_time_days": [watch_time_days],
    "engagement_rate": [engagement_rate],
    "sub_engagement": [sub_engagement],
    "category": [category],
    "device": [device],
    "country": [country],
    "day_name": [day_name]
})

# ----------------------------------------------------
# Prediction
# ----------------------------------------------------
if st.button("🚀 Predict Revenue"):
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Estimated Revenue: **${prediction:.2f}**")

# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.markdown("---")
st.caption("✨ Created by Sai Sudharsan | Powered with Streamlit")
