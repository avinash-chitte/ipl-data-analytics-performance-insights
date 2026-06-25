# 🏏 IPL Intelligence Hub: Analytics & Match Prediction Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75.svg?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2%2B-F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e.svg?style=flat-square)](LICENSE)

A production-grade, modular sports analytics application and decision-support system (DSS) built with Streamlit, Plotly, and scikit-learn. The platform processes over 17 seasons of ball-by-ball Indian Premier League data (2008–2025) to deliver deep tactical insights, venue diagnostics, player evaluation, and **live win probability predictions** using machine learning.

Designed with clean architecture, premium UI/UX, and production fallback logic, this project serves as a showcase of end-to-end Python data engineering, visualization, and ML deployment.

---

## 📋 Table of Contents

- [Project Overview & Business Value](#-project-overview--business-value)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Machine Learning & Prediction Pipeline](#-machine-learning--prediction-pipeline)
- [Technology Stack](#-technology-stack)
- [Interactive UI & Screenshots](#-interactive-ui--screenshots)
- [Installation Guide](#-installation-guide)
- [Deployment](#-deployment)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 🎯 Project Overview & Business Value

In modern sports, franchises, broadcasters, and coaches require real-time, data-driven tools to optimize tactical strategies. This project simulates an enterprise-level sports analytics dashboard answering critical questions:

* **Squad Optimization:** How do players perform across match phases (Powerplay, Middle, and Death overs) to align with team matchups?
* **Venue Intelligence:** Which venues favor chasing vs. defending, and what is the spin-to-pace wicket ratio?
* **Live In-Game Predictions:** What is the real-time probability of winning a chase given balls remaining, wickets lost, and run rates?
* **Auction Strategy:** Identify high-value players and MVP candidates based on historical performance indices.

---

## 🏗️ System Architecture

The project is designed with a modular separation of concerns. Raw data operations, preprocessing, machine learning algorithms, styling templates, and page views are isolated to maintain clean code and testability.

```
projectIPL/
├── app.py                      # Main entry point (Routing, Global Sidebar Filters)
├── requirements.txt            # Python pip dependencies
├── LICENSE                     # MIT License
├── README.md                   # Project Documentation
├── .streamlit/
│   └── config.toml             # Custom theme colors and settings
├── data/
│   └── README.md               # Dataset source and download details
├── src/
│   ├── __init__.py
│   ├── constants.py            # Central configurations & official team colors
│   ├── styles.py               # Custom CSS templates & Plotly layout helper utilities
│   ├── data_loader.py          # Data ingestion engine & simulated dataset fallback
│   ├── preprocessing.py        # Feature engineering & aggregations
│   └── ml_model.py             # Classifier model, split logic, & evaluation metrics
├── views/
│   ├── __init__.py
│   ├── overview.py             # Tournament summaries & season scoring trends
│   ├── team_performance.py     # Team head-to-head profiles & consistency metrics
│   ├── player_explorer.py      # Batter & bowler profiles with phase breakdowns
│   ├── venue_intelligence.py   # Ground-level pace/spin splits & chasing trends
│   ├── powerplay_death.py      # Run-rate evolutions and specialists lists
│   ├── match_predictor.py      # ML live run-chase win predictor & metrics tabs
│   └── key_insights.py         # Curated tactical & business insights
└── notebooks/
    └── *.ipynb                 # Exploratory data analysis notebooks
```

---

## ✨ Key Features

### 1. 📊 Tournament Overview
* High-level KPI metric cards showing matches played, total runs, wickets, highest team score, and most successful franchise.
* Interactive dual-axis line chart depicting historical scoring averages and runs-per-over (RPO) trends.
* Toss impact assessment and boundary evolution bars (Fours vs. Sixes per season).

### 2. ⚔️ Team Performance & Head-to-Head
* Team comparison metrics including win-percentage evolution over time.
* Direct Head-to-Head (H2H) simulator for any two franchises showing wins share, recent encounters, and match results.
* Consistency indices based on score deviations and orange/purple cap winners.

### 3. 🧑‍💻 Player Performance Explorer
* Interactive profile search for any batter or bowler.
* Phase-wise performance splits (Powerplay, Middle, Death overs) comparing strike rates, averages, boundaries, and economy rates.
* Season-over-season career trajectory plots.

### 4. 🏟️ Venue Intelligence
* Comparison of scores and chase success rates between venues.
* Ground character profiles based on boundary percentages, run-rates, and pace vs. spin wickets splits.

### 5. 🤖 Live ML Match Predictor
* Dynamic input forms for in-progress second-innings run chases (Target, Current Score, Wickets, Overs).
* Gauge visualization displaying win probability and model confidence indicators.
* Model evaluation suite showing the ROC-AUC curve, Confusion Matrix, and Feature Importance coefficients.

---

## 🧠 Machine Learning & Prediction Pipeline

The **Live Match Predictor** utilizes a classification model optimized for second-innings runs chases:

1. **Target Variable:** Binary outcome (`match_won` - 1 if the chasing team successfully hits the target, 0 otherwise).
2. **Feature Engineering:**
   * `runs_needed`: Target runs minus current runs.
   * `balls_remaining`: Balls available (120 minus balls bowled).
   * `wickets_lost`: Active wickets lost by chasing team.
   * `required_run_rate`: `(runs_needed * 6) / balls_remaining`.
   * `current_run_rate`: `(current_runs * 6) / balls_bowled`.
3. **Data Splitting & Training:**
   * Chronological Train/Test split: Pre-2023 data is used for training (~7,700 match situations), 2023–2025 is held back for testing (~1,270 situations).
   * **Logistic Regression** classifier trained with `class_weight='balanced'` to offset class imbalance.
4. **Performance Metrics:**
   * **ROC-AUC:** Demonstrates strong discriminative capability.
   * Features coefficients ranking reveals `wickets_lost` and `required_run_rate` as the most critical predictors of second-innings chases.

---

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Dashboard App:** Streamlit 1.28+ (Modular Views layout)
* **Visualizations:** Plotly 5.15+ (Gauges, Scatter, Bar, Donut, Line, and Heatmaps)
* **Data Processing:** Pandas 2.0+, NumPy 1.24+
* **Machine Learning:** scikit-learn 1.2+
* **Styling System:** CSS Custom Variables (Injected Google Fonts: Inter, responsive styles, custom KPI frames)

---

## 📸 Interactive UI & Screenshots

The platform features a custom UI design with interactive elements and transitions:

* **Custom Sidebar Navigation:**
  ![Sidebar](https://img.shields.io/badge/Sidebar-Custom_CSS-111114.svg)
* **Dynamic Dark-Mode Theme:** Clean layout featuring custom borders (`#1e1e24`) and typography (`Inter`).
* **KPI Metrics Layout:**
  ![KPI Cards](https://img.shields.io/badge/Metrics-Glassmorphism-2563eb.svg)

---

## 🚀 Installation Guide

Follow these steps to run the application locally on your machine.

### 1. Clone the Project
```bash
git clone https://github.com/your-username/IPL-Intelligence-Hub.git
cd IPL-Intelligence-Hub
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Fetch the Data
Download the [Kaggle IPL Dataset 2008-2025](https://www.kaggle.com/datasets/saurabhbadole/ipl-dataset-2008-2025) and place the `IPL.csv` file inside the `data/` directory.

> **💡 Recruiter Tip:** If `IPL.csv` is missing, the application automatically initiates an intelligent simulated data generator. This lets you run, navigate, and test all ML predictor widgets immediately!

### 5. Start the Streamlit App
```bash
python -m streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## ☁️ Deployment

The application is fully compatible with **Streamlit Community Cloud**:

1. Fork/Push this repository to your GitHub profile.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository and set the main entry file to `app.py`.
4. Click **Deploy** — the platform automatically handles installation using `requirements.txt`.

---

## 🔮 Future Roadmap

- [ ] **Batter vs Bowler Matchups:** Interactive head-to-head match-up grid detailing historic strike rates and wicket events.
- [ ] **Auction Value Predictor:** K-Means player clustering coupled with regression models to estimate auction bid valuation.
- [ ] **Live API Integration:** Hook up match scoring APIs to enable live prediction on running matches.
- [ ] **Advanced ML Models:** Train and evaluate XGBoost or Random Forest classifiers alongside the baseline Logistic Regression.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">
  <b>Built with Python, Streamlit, and Plotly</b>
</div>
