# 🏏 IPL Analytics & Performance Insights Dashboard (2008-2025)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.22%2B-FF4B4B.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scipy-sklearn-orange.svg)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.0%2B-darkgreen.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An interactive, data-driven Streamlit dashboard that provides deep tactical insights, player dynamics, and strategic benchmarks of the Indian Premier League (IPL) from 2008 to 2025. It also includes a live chasing win probability predictor using machine learning.

---

## 🌟 Dashboard Features

1. **🏆 Summary & Scoring**: Interactive visualizations of season-wise scoring trends and toss impact.
2. **🥇 Cap Winners**: Deep dives into historic Orange Cap (highest runs) and Purple Cap (highest wickets) winners.
3. **⚔️ Team Performance**: Compare season-by-season win rates and performance of multiple IPL franchises.
4. **🏟️ Venue Intelligence**: Average runs and performance benchmarks for different stadiums.
5. **🤖 Live Win Predictor**: A Logistic Regression model predicting the ball-by-ball win probability of chasing teams in the second innings based on live match context.
6. **🎛️ Interactive Filters**: Dynamically filter data across the dashboard by season ranges and specific teams.
7. **🌗 Professional UI**: Clean, responsive layout with built-in Dark/Light mode support.

---

## 🛠️ Tech Stack

- **Frontend/Web Framework**: `Streamlit`
- **Data Processing**: `Pandas`, `NumPy`
- **Machine Learning**: `Scikit-Learn` (Logistic Regression for win prediction)
- **Visualization**: `Plotly` (interactive charts and gauges)

---

## 🚀 How to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/IPL-Analytics-Dashboard.git
   cd IPL-Analytics-Dashboard
   ```

2. **Set Up a Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Provide the Dataset**:
   Download the ball-by-ball dataset (e.g., from Kaggle). Ensure `IPL.csv` is placed in the `data/` folder, or in the same directory as `app.py`. *(Note: The app has a fallback mechanism to generate simulated data for demonstration if the file is not found).*

4. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment Instructions for Streamlit Cloud

To share your dashboard with the world, you can easily deploy it for free using **Streamlit Community Cloud**:

1. **Push your code to GitHub**:
   - Ensure your repository contains `app.py`, `requirements.txt`, and this `README.md`.
   - Ensure you push your `IPL.csv` data file to your repository (or adjust `app.py` to fetch it from a remote source/bucket, or rely on the app's simulated data fallback).

2. **Log in to Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.

3. **Deploy the App**:
   - Click the **"New app"** button in the top right.
   - Connect your GitHub account and select your repository.
   - Choose your branch (e.g., `main`).
   - Set the Main file path to `app.py`.
   - (Optional) Customize your app URL in the advanced settings.
   - Click **"Deploy!"**

4. **Manage your App**:
   - Streamlit will automatically install the dependencies from `requirements.txt` and launch your dashboard.
   - Any future `git push` to your linked branch will trigger an automatic re-deployment and update your live app!
