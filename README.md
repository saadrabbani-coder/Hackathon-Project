# AI Powered E-Commerce Customer Intelligence System

## Hackathon project
This project follows the supplied Data Science Final Hackathon brief. It uses the provided SQLite database, SQL business analysis, cleaning, EDA, customer churn prediction, a small neural network, review sentiment analysis, and a Streamlit app.

## Run locally
```bash
pip install -r requirements.txt
jupyter notebook notebooks/hackathon_solution.ipynb
```

After running the notebook, start the app:
```bash
streamlit run app/streamlit_app.py
```

## Project structure
- `data/ecommerce_hackathon.db` - supplied SQLite database
- `notebooks/hackathon_solution.ipynb` - complete analysis and modeling
- `sql_queries.sql` - five required SQL queries
- `models/` - saved churn and sentiment models
- `app/streamlit_app.py` - Streamlit application
- `requirements.txt` - dependencies

## Important modeling decision
Churn features are built only from orders on or before 31 May 2026. Churn is 1 when a customer has no order from 1 June through 31 August 2026. This avoids using future target-window purchases as input features.

## Data cleaning
The notebook documents missing values, invalid dates, inconsistent categories, invalid order quantities/prices, missing delivery/payment values, and invalid review ratings. Cleaning decisions are simple and explained in the notebook.

## Example model results from the provided data
- Logistic Regression: Accuracy 0.715, F1 0.743, ROC-AUC 0.787
- Random Forest: Accuracy 0.688, F1 0.702, ROC-AUC 0.759
- Neural Network: Accuracy 0.714, F1 0.732, ROC-AUC 0.785
- Sentiment Logistic Regression with TF-IDF: Accuracy 1.000, weighted F1 1.000 on the held-out test set.

These are notebook results on this supplied database and should be explained rather than treated as universal performance.
