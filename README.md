# AI_retirement_tool

A personalized, AI-powered web application that helps users plan their retirement, simulate life scenarios, and receive strategic financial advice using Gemini LLM.

## Features

-  **User Authentication** – Register and login securely with SQLite.
-  **Retirement Corpus Estimation** – Calculates how much money you’ll need post-retirement.
-  **Scenario Modeling** – Simulate life events like marriage, childbirth, job loss, and healthcare costs.
-  **AI-Generated Advice** – Uses Gemini AI to generate financial strategies.
-  **Visual Projections** – Graphs to visualize your future savings vs. retirement goals.
-  **Welcome Screen** – Custom UI with background image and login/register buttons.
-  **Deployed via Streamlit Cloud** – No local setup needed.

---

## Tech Stack

| Component       | Technology           |
|----------------|----------------------|
| Frontend       | Streamlit            |
| Backend Logic  | Python (calculations, simulations) |
| AI Model       | Gemini 1.5 Flash     |
| Database       | SQLite               |
| Visualization  | Matplotlib           |
| Deployment     | Streamlit Cloud      |
| Version Control| GitHub               |

---

##  Project Structure
 AI-Retirement-Tool/
├── app.py # Main Streamlit app
├── .env # Secret Gemini API key
├── requirements.txt # Python dependencies
├── README.md # You're here!
├── users.db # SQLite database (created on first run)
├── image/
│ └── background.jpg # Welcome screen background
└── utils/
├── auth.py # Login and register functions
├── calculations.py # Retirement corpus calculations
├── ai_agent.py # Gemini prompt and response
└── visualizations.py # Graphs for projections


---

##  How it Works

###  Corpus Calculation
Retirement corpus is calculated using:
- Monthly expenses
- Time to retirement
- Expected inflation
- Expected investment return

###  Scenario Modeling
You can simulate:
- Marriage 
- Having a child 
- Job loss 
- Healthcare costs 
- Inflation spike

Each event dynamically adjusts expenses or income.

###  AI Advice
Gemini LLM takes the user’s profile, corpus, and scenario context, and generates a personalized investment or retirement plan.

