# AI-Powered E-Commerce Customer Intelligence System

A data science hackathon project that turns raw e-commerce data into business insights, churn predictions, and review sentiment analysis, all wrapped in an interactive Streamlit app.

Built according to the supplied **Data Science Final Hackathon** brief, using the provided SQLite database.

## What's inside

- **SQL business analysis**: five required queries covering revenue, orders, and customer behaviour
- **Data cleaning and EDA**: documented handling of messy real-world data
- **Customer churn prediction**: Logistic Regression, Random Forest, and a small neural network
- **Review sentiment analysis**: TF-IDF with Logistic Regression
- **Streamlit app**: an interactive dashboard to explore results and run predictions

## App features

| Section | What it does |
|---|---|
| Dashboard | Net revenue, total orders, total customers, monthly revenue trend, and revenue by category |
| Churn Prediction | Enter a customer's profile and buying history to get a churn probability |
| Sentiment Analysis | Paste a customer review to classify its sentiment |

## Getting started

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the notebook**

This performs the analysis and saves the trained models to `models/`.

```bash
jupyter notebook notebooks/hackathon_solution.ipynb
```

**3. Launch the app**

```bash
streamlit run app/streamlit_app.py
```

> Run the app from the project root so the custom theme in `.streamlit/config.toml` is applied.

## Project structure

```
.
├── .streamlit/
│   └── config.toml              # App theme
├── app/
│   └── streamlit_app.py         # Streamlit application
├── data/
│   └── ecommerce_hackathon.db   # Supplied SQLite database
├── models/                      # Saved churn and sentiment models
├── notebooks/
│   └── hackathon_solution.ipynb # Complete analysis and modeling
├── sql_queries.sql              # Five required SQL queries
└── requirements.txt             # Dependencies
```

## Key modeling decision: avoiding data leakage

Churn is defined using a strict time split:

- **Features** are built only from orders placed **on or before 31 May 2026**.
- **Target**: a customer is labelled as churned (`1`) if they placed **no orders between 1 June and 31 August 2026**.

This ensures the model never sees purchases from the prediction window, so its performance reflects how it would behave on genuinely future data.

## Data cleaning

The notebook documents and resolves the following issues:

- Missing values
- Invalid dates
- Inconsistent category labels
- Invalid order quantities and prices
- Missing delivery and payment values
- Invalid review ratings

Each cleaning decision is kept simple and explained alongside the code.

## Results

### Churn prediction

| Model | Accuracy | F1 | ROC-AUC |
|---|---|---|---|
| Logistic Regression | 0.715 | **0.743** | **0.787** |
| Random Forest | 0.688 | 0.702 | 0.759 |
| Neural Network | 0.714 | 0.732 | 0.785 |

Logistic Regression performed best overall, with the neural network close behind.

### Sentiment analysis

| Model | Accuracy | Weighted F1 |
|---|---|---|
| TF-IDF + Logistic Regression | 1.000 | 1.000 |

Scores are on the held-out test set.

> **Note:** These results are specific to the supplied database and should be interpreted in that context, not treated as universal performance.

## Tech stack

Python · pandas · NumPy · scikit-learn · SQLite · Jupyter · Streamlit · Altair
