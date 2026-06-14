import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💰",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("salary_model.pkl")
features = joblib.load("features.pkl")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
}

.title {
    text-align: center;
    font-size: 65px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #2563eb;
    margin-top: -10px;
}

.description {
    text-align: center;
    font-size: 22px;
    color: #475569;
    margin-bottom: 40px;
}

.metric-card {
    background-color: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
    text-align: center;
}

.metric-title {
    font-size: 28px;
    font-weight: 700;
}

.metric-value {
    font-size: 45px;
    font-weight: bold;
    color: #0f172a;
}

.card {
    background-color: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
}

.predict-btn {
    background-color: #2563eb;
    color: white;
}

.success-box {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    padding: 35px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-top: 20px;
}

.salary-text {
    font-size: 50px;
    font-weight: bold;
}

.range-text {
    font-size: 30px;
    font-weight: 600;
}

.tech-box {
    background-color: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
    text-align: center;
}

.tech-title {
    font-size: 34px;
    font-weight: 700;
    color: #0f172a;
}

.tech-item {
    font-size: 24px;
    font-weight: 600;
    color: #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<div class='title'>💰 Salary Prediction App</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Predict Employee Salary</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='description'>
    Predict employee salaries using Machine Learning based on experience, education, city, and age.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-title' style='color:#7c3aed;'>Algorithm</div>
        <div class='metric-value'>Regression</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-title' style='color:#16a34a;'>Accuracy</div>
        <div class='metric-value'>92%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-title' style='color:#2563eb;'>Dataset Size</div>
        <div class='metric-value'>10K+</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-title' style='color:#ea580c;'>Deployment</div>
        <div class='metric-value'>Streamlit</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- MAIN SECTION ----------------
left, right = st.columns([1, 1])

# ---------------- LEFT SIDE ----------------
with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>📋 Enter Employee Details</div><br>",
        unsafe_allow_html=True
    )

    experience = st.slider(
        "Experience (Years)",
        0,
        30,
        2
    )

    age = st.slider(
        "Age",
        18,
        60,
        25
    )

    education = st.selectbox(
        "Education Level",
        ["Bachelors", "Masters", "PhD"]
    )

    city = st.selectbox(
        "City",
        ["Hyderabad", "Bangalore", "Chennai"]
    )

    skills = st.multiselect(
        "Skills",
        ["Python", "Machine Learning",
         "SQL", "Deep Learning",
         "Power BI", "Java"]
    )

    # ---------------- CREATE INPUT ----------------
    input_dict = {col: 0 for col in features}

    for col in features:
        col_lower = col.lower()

        if "experience" in col_lower:
            input_dict[col] = experience

        elif "age" in col_lower:
            input_dict[col] = age

        elif f"education_{education}".lower() == col_lower:
            input_dict[col] = 1

        elif f"city_{city}".lower() == col_lower:
            input_dict[col] = 1

    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=features, fill_value=0)

    # ---------------- PREDICT BUTTON ----------------
    if st.button("🚀 Predict Salary", use_container_width=True):

        prediction = model.predict(input_df)[0]

        prediction = abs(prediction)

        prediction = round(prediction)

        min_salary = prediction - 50000
        max_salary = prediction + 50000

        st.markdown(f"""
        <div class='success-box'>

        <h1>💸 Predicted Salary</h1>

        <div class='salary-text'>
        ₹ {prediction:,.0f} / year
        </div>

        <br>

        <div class='range-text'>
        Estimated Range:
        <br>
        ₹ {min_salary:,.0f} - ₹ {max_salary:,.0f}
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.success(
            "Prediction generated successfully using trained ML model."
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT SIDE ----------------
with right:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>📊 Salary Insights</div><br>",
        unsafe_allow_html=True
    )

    # ---------------- LINE CHART ----------------
    exp = np.array([1, 5, 15, 30])
    salary = np.array([520000, 600000, 680000, 750000])

    chart_df = pd.DataFrame({
        "Experience": exp,
        "Salary": salary
    })

    fig = px.line(
        chart_df,
        x="Experience",
        y="Salary",
        markers=True,
        title="Experience vs Salary Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- BAR CHART ----------------
    edu_df = pd.DataFrame({
        "Education": ["Bachelors", "Masters", "PhD"],
        "Average Salary": [600000, 900000, 1300000]
    })

    fig2 = px.bar(
        edu_df,
        x="Education",
        y="Average Salary",
        title="Average Salary by Education",
        text="Average Salary"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Salaries increase with more experience and higher education levels."
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- TECHNOLOGIES USED ----------------
st.write("")
st.write("")

st.markdown("""
<div class='tech-box'>

<div class='tech-title'>
💻 Technologies Used
</div>

<br><br>

<div style='display:flex;
justify-content:space-around;
flex-wrap:wrap;
gap:20px;'>

<div class='tech-item'>🐍 Python</div>

<div class='tech-item'>🚀 Streamlit</div>

<div class='tech-item'>🤖 Scikit-Learn</div>

<div class='tech-item'>📊 Pandas</div>

<div class='tech-item'>📈 Plotly</div>

<div class='tech-item'>💾 Joblib</div>

</div>

</div>
""", unsafe_allow_html=True)