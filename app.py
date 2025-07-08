import streamlit as st
import base64
import streamlit.components.v1 as components

from utils.calculations import calculate_corpus, simulate_savings_growth
from utils.ai_agent import generate_advice
from utils.visualizations import plot_projection, plot_savings_vs_corpus
from utils.auth import login, signup  # add signup
import sqlite3

# App config
st.set_page_config(page_title="AI Retirement Planner", layout="centered")

# SQLite database setup
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (username TEXT, authenticated INTEGER)''')
conn.commit()

#--- session state ----
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def set_bg(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .center-box {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 10px;
            width: 350px;
            margin: auto;
            text-align: center;
            margin-top: 100px;
        }}
        </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
set_bg("image/background.jpg")


# --- Handle logout ---
if st.query_params.get("logout") == "true":
    st.session_state.authenticated = False
    st.session_state.page = "login"
    st.session_state.page = "welcome"
    st.success("Logged out successfully.")
    st.rerun()    



if st.session_state.page == "welcome":

    st.title("Welcome to AI Retirement Planner")
    st.write("Plan your future with smart simulations and AI advice.")
    col1, col2, col3, col4 = st.columns([4,2,2,4])
    with col2:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
            st.rerun()
    with col3:
        if st.button("🆕 Register"):
            st.session_state.page = "signup"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# --- Login Page ---
if st.session_state.page == "login" and not st.session_state.authenticated:
    st.markdown("<div class='center-container'><div class='login-box'>", unsafe_allow_html=True)
    if login(cursor, conn):
        st.session_state.authenticated = True
        st.session_state.page = "profile"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- Signup Page ---
if st.session_state.page == "signup"and not st.session_state.authenticated:
    st.markdown("<div class='center-container'><div class='login-box'>", unsafe_allow_html=True)
    signup(cursor, conn)
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

if st.session_state.get("authenticated"):
    col1, col2, col3 = st.columns([6, 2, 2])
    with col3:
        if st.button("🔒 Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "welcome"
            if st.session_state.get("username"):
                cursor.execute("DELETE FROM sessions WHERE username = ?", (st.session_state["username"],))
                conn.commit()
            st.success("Logged out successfully.")
            st.rerun()



st.title("🧠 AI Retirement Planner - User Profile")
age = st.number_input("Enter your current age", 18, 100)
retirement_age = st.slider("Target retirement age", 45, 75, 60)
income = st.number_input("Monthly income (₹)", min_value=0)
monthly_expense = st.number_input("Monthly expenses (₹)", min_value=0)
monthly_saving = st.number_input("Monthly savings (₹)", min_value=0)
current_savings = st.number_input("Current savings (₹)", min_value=0)
life_expectancy = st.slider("Expected life span", 70, 100, 85)
inflation_rate = st.slider("Expected inflation rate (%)", 1, 10, 6)/100
risk = st.selectbox("Risk Preference", ["Low", "Medium", "High"])


if st.button("Calculate Retirement Plan"):
    corpus = calculate_corpus(age, retirement_age, current_savings, monthly_expense, monthly_saving,inflation_rate)
    st.success(f"Estimated Retirement Corpus Needed: ₹{corpus:,.2f}")
    st.subheader("AI Financial Advice")
    st.write(generate_advice(age, retirement_age, risk, corpus))
    st.subheader("Savings Projection")
    plot_projection(age, retirement_age, current_savings, monthly_saving, corpus)

# Scenario Modeling
st.markdown("Scenario Modeling")
scenario = st.selectbox(
    "Select a scenario to simulate",
    ["None", "Having a child", "Marriage", "Job loss", "Healthcare cost", "Inflation spike"]
)
# --- Apply Scenario Impact ---
if scenario == "Job Loss":
    income *= 0.75  # reduce income by 25%
elif scenario == "Marriage":
    monthly_expense *= 1.3  # 30% increase
elif scenario == "Having a child":
    monthly_expense *= 1.5  # 50% increase
    income *= 0.9    # Less work hours
elif scenario == "Healthcare cost":
    monthly_saving -= 200000  # Large cut from savings
elif scenario == "Inflation spike":
    inflation_rate += 0.03

if st.button("Run Scenario Analysis"):
    years_post_retirement = life_expectancy - retirement_age
    years_to_retire = retirement_age - age

    scenario_corpus = calculate_corpus(
        age, retirement_age, monthly_expense,
        current_savings, monthly_saving,
        inflation=inflation_rate)
    st.session_state["scenario_corpus"] = scenario_corpus  #store in session
    st.info(f"Scenario Corpus Needed: ₹{scenario_corpus:,.2f}")
    st.caption("This reflects adjusted retirement needs based on your selected scenario.")

    # Plot updated graph
    projection = simulate_savings_growth(
        current_savings=current_savings, monthly_saving=monthly_saving,
        years=years_to_retire)
    
    fig = plot_savings_vs_corpus(projection, scenario_corpus)
    st.pyplot(fig)

# --- Gemini-Based Strategy Suggestion ---
if st.button("Get AI Scenario Insights"):
    if "scenario_corpus" not in st.session_state:
        st.warning("Please run scenario Analysis first.")
    else:
        scenario_corpus = st.session_state["scenario_corpus"]
    prompt = (
        f"User age: {age}, income: ₹{income}, expenses: ₹{monthly_expense}, savings: ₹{monthly_saving}. "
        f"Retirement goal: age {retirement_age}, life expectancy: {life_expectancy}. "
        f"Scenario selected: {scenario}, inflation rate: {inflation_rate * 100:.2f}%. "
        f"Risk profile: {risk}. Estimated retirement corpus needed: ₹{scenario_corpus:,.2f}.\n\n"
        "Suggest a retirement strategy, investment plan, or savings adjustments "
        "based on this scenario."
    )
    ai_response = generate_advice(age, retirement_age, risk, scenario_corpus)
    st.subheader("AI-Generated Scenario Strategy")
    st.write(ai_response)



