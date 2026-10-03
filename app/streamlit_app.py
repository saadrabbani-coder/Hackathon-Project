import os
import html
import sqlite3
import joblib
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

BASE = os.path.dirname(__file__)
ROOT = os.path.dirname(BASE)
DB_PATH = os.path.join(ROOT, "data", "ecommerce_hackathon.db")
MODEL_DIR = os.path.join(ROOT, "models")

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
PLUM_DEEP = "#1A1123"
PLUM = "#251932"
PLUM_RAISED = "#2F2140"
GOLD = "#D9B970"
GOLD_SOFT = "#B8975A"
IVORY = "#F3EDE2"
MAUVE = "#A393B0"
LINE = "rgba(217,185,112,0.22)"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, label, input, textarea, button {{
    font-family: 'Manrope', system-ui, -apple-system, sans-serif;
}}

.stApp {{
    background:
        radial-gradient(1200px 600px at 85% -10%, rgba(217,185,112,0.10), transparent 60%),
        radial-gradient(900px 500px at -10% 110%, rgba(140,90,170,0.18), transparent 60%),
        {PLUM_DEEP};
    color: {IVORY};
}}

#MainMenu, footer, header[data-testid="stHeader"] {{ background: transparent; }}
footer {{ visibility: hidden; }}

.block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1280px; }}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {PLUM} 0%, {PLUM_DEEP} 100%);
    border-right: 1px solid {LINE};
}}
section[data-testid="stSidebar"] .brand {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.9rem; font-weight: 600; color: {GOLD};
    line-height: 1.05; margin: 0.4rem 0 0.2rem;
}}
section[data-testid="stSidebar"] .brand-sub {{
    color: {MAUVE}; font-size: 0.85rem; margin-bottom: 1.6rem;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    padding: 0.65rem 0.9rem; border-radius: 10px; margin-bottom: 0.25rem;
    border: 1px solid transparent; transition: background .2s, border-color .2s;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background: rgba(217,185,112,0.06);
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background: rgba(217,185,112,0.12); border-color: {LINE};
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
    font-size: 0.98rem; font-weight: 500; color: {IVORY};
}}

/* ---------- Page heading ---------- */
.hero {{ margin-bottom: 2rem; padding-bottom: 1.4rem; border-bottom: 1px solid {LINE}; }}
.hero h1 {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(2.2rem, 4vw, 3.4rem); font-weight: 600;
    color: {IVORY}; letter-spacing: -0.01em; line-height: 1.05; margin: 0;
}}
.hero p {{ color: {MAUVE}; font-size: 1rem; margin: 0.6rem 0 0; max-width: 62ch; }}

h2, h3 {{ font-family: 'Cormorant Garamond', Georgia, serif !important; color: {IVORY} !important; }}
.section-title {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.7rem; font-weight: 600; color: {IVORY}; margin: 0.4rem 0 0.2rem;
}}
.section-note {{ color: {MAUVE}; font-size: 0.9rem; margin-bottom: 0.8rem; }}

/* ---------- KPI tiles ---------- */
.kpi-row {{ display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }}
@media (max-width: 900px) {{ .kpi-row {{ grid-template-columns: 1fr; }} }}
.kpi {{
    background: linear-gradient(160deg, {PLUM_RAISED} 0%, {PLUM} 100%);
    border: 1px solid {LINE}; border-radius: 18px; padding: 1.4rem 1.6rem;
}}
.kpi.feature {{
    background: linear-gradient(150deg, #3A2A1E 0%, {PLUM_RAISED} 55%, {PLUM} 100%);
    border-color: rgba(217,185,112,0.45);
}}
.kpi .label {{ color: {MAUVE}; font-size: 0.88rem; font-weight: 500; }}
.kpi .value {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 2.6rem; font-weight: 600; color: {IVORY}; line-height: 1.1; margin-top: 0.35rem;
}}
.kpi.feature .value {{ color: {GOLD}; font-size: 3.1rem; }}

/* ---------- Panels ---------- */
.panel-gap {{ height: 0.4rem; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(37,25,50,0.65);
    border: 1px solid {LINE} !important; border-radius: 18px !important;
}}

/* ---------- Inputs ---------- */
.stNumberInput input, .stTextArea textarea, div[data-baseweb="select"] > div {{
    background: {PLUM_DEEP} !important; color: {IVORY} !important;
    border: 1px solid rgba(163,147,176,0.28) !important; border-radius: 10px !important;
}}
.stNumberInput input:focus, .stTextArea textarea:focus {{
    border-color: {GOLD} !important; box-shadow: 0 0 0 2px rgba(217,185,112,0.25) !important;
}}
.stNumberInput button {{ background: {PLUM_RAISED} !important; color: {IVORY} !important; border: none !important; }}
label p {{ color: {MAUVE} !important; font-weight: 500 !important; }}

/* ---------- Buttons ---------- */
.stButton > button {{
    background: linear-gradient(135deg, {GOLD} 0%, {GOLD_SOFT} 100%);
    color: {PLUM_DEEP}; font-weight: 700; font-size: 0.98rem;
    border: none; border-radius: 999px; padding: 0.7rem 2rem; width: 100%;
    box-shadow: 0 8px 24px rgba(217,185,112,0.22); transition: transform .15s, box-shadow .15s;
}}
.stButton > button:hover {{ transform: translateY(-1px); box-shadow: 0 12px 30px rgba(217,185,112,0.32); color: {PLUM_DEEP}; }}
.stButton > button:focus-visible {{ outline: 2px solid {IVORY}; outline-offset: 3px; }}

/* ---------- Result: churn dial ---------- */
.result {{ display: flex; align-items: center; gap: 1.8rem; flex-wrap: wrap; }}
.dial {{
    --p: 0; --c: {GOLD};
    width: 170px; height: 170px; border-radius: 50%;
    background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(163,147,176,0.15) 0);
    display: grid; place-items: center; flex-shrink: 0;
    animation: dial-in .9s ease-out;
}}
.dial-inner {{
    width: 136px; height: 136px; border-radius: 50%; background: {PLUM};
    display: grid; place-items: center; text-align: center;
}}
.dial-num {{ font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2.5rem; font-weight: 600; color: {IVORY}; line-height: 1; }}
.dial-cap {{ color: {MAUVE}; font-size: 0.78rem; margin-top: 0.2rem; }}
@keyframes dial-in {{ from {{ transform: scale(.92); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ .dial {{ animation: none; }} }}

.verdict {{ font-family: 'Cormorant Garamond', Georgia, serif; font-size: 2rem; font-weight: 600; line-height: 1.1; }}
.verdict-note {{ color: {MAUVE}; font-size: 0.95rem; margin-top: 0.4rem; max-width: 42ch; }}

/* ---------- Result: sentiment ---------- */
.sentiment {{
    display: inline-flex; align-items: center; gap: 0.7rem;
    padding: 0.8rem 1.4rem; border-radius: 999px; border: 1px solid;
    font-family: 'Cormorant Garamond', Georgia, serif; font-size: 1.8rem; font-weight: 600;
}}
.sentiment .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
.quote {{
    font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic;
    font-size: 1.25rem; color: {IVORY}; line-height: 1.5;
    border-left: 2px solid {GOLD}; padding-left: 1rem; margin-top: 1.2rem; max-width: 70ch;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Data & models (unchanged logic)
# ---------------------------------------------------------------------------
@st.cache_data
def load_dashboard_data():
    con = sqlite3.connect(DB_PATH)
    total_revenue = pd.read_sql_query("""
        SELECT ROUND(SUM(unit_price * quantity * (1-discount)),2) revenue
        FROM orders WHERE returned=0 AND unit_price>0 AND quantity>0
    """, con).iloc[0, 0]
    total_orders = pd.read_sql_query("SELECT COUNT(*) n FROM orders", con).iloc[0, 0]
    total_customers = pd.read_sql_query("SELECT COUNT(*) n FROM customers", con).iloc[0, 0]
    monthly = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) month,
        ROUND(SUM(unit_price*quantity*(1-discount)),2) revenue
        FROM orders WHERE returned=0 AND unit_price>0 AND quantity>0
        GROUP BY month ORDER BY month
    """, con)
    category = pd.read_sql_query("""
        SELECT p.category,
        ROUND(SUM(o.unit_price*o.quantity*(1-o.discount)),2) revenue
        FROM orders o JOIN products p ON o.product_id=p.product_id
        WHERE o.returned=0 AND o.unit_price>0 AND o.quantity>0
        GROUP BY p.category ORDER BY revenue DESC
    """, con)
    con.close()
    return total_revenue, total_orders, total_customers, monthly, category


@st.cache_resource
def load_models():
    churn_model = joblib.load(os.path.join(MODEL_DIR, "churn_model.joblib"))
    churn_features = joblib.load(os.path.join(MODEL_DIR, "churn_features.joblib"))
    sentiment_model = joblib.load(os.path.join(MODEL_DIR, "sentiment_model.joblib"))
    return churn_model, churn_features, sentiment_model


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def section(title, note=""):
    note_html = f'<div class="section-note">{note}</div>' if note else ""
    st.markdown(f'<div class="section-title">{title}</div>{note_html}', unsafe_allow_html=True)


def chart_theme(chart):
    return (
        chart.configure(background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor=MAUVE, titleColor=MAUVE, gridColor="rgba(163,147,176,0.12)",
            domainColor="rgba(163,147,176,0.25)", tickColor="rgba(163,147,176,0.25)",
            labelFont="Manrope", titleFont="Manrope", labelFontSize=12, titleFontSize=12,
        )
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand">Customer<br>Intelligence</div>'
        '<div class="brand-sub">AI insights for your store</div>',
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Choose a section",
        ["Dashboard", "Churn Prediction", "Sentiment Analysis"],
        label_visibility="collapsed",
    )


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
if page == "Dashboard":
    hero(
        "Store performance",
        "Net revenue after discounts and returns, with how it moves month to month and which categories drive it.",
    )
    revenue, orders, customers, monthly, category = load_dashboard_data()
    revenue = revenue or 0

    st.markdown(
        f"""
        <div class="kpi-row">
            <div class="kpi feature"><div class="label">Net revenue</div><div class="value">${revenue:,.2f}</div></div>
            <div class="kpi"><div class="label">Total orders</div><div class="value">{orders:,}</div></div>
            <div class="kpi"><div class="label">Total customers</div><div class="value">{customers:,}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    with left:
        with st.container(border=True):
            section("Monthly revenue", "Completed, non-returned orders")
            base = alt.Chart(monthly).encode(
                x=alt.X("month:N", title=None, axis=alt.Axis(labelAngle=-40)),
                y=alt.Y("revenue:Q", title=None, axis=alt.Axis(format="$~s")),
                tooltip=[alt.Tooltip("month:N", title="Month"), alt.Tooltip("revenue:Q", title="Revenue", format="$,.2f")],
            )
            area = base.mark_area(
                interpolate="monotone",
                line={"color": GOLD, "strokeWidth": 2.5},
                color=alt.Gradient(
                    gradient="linear",
                    stops=[
                        alt.GradientStop(color="rgba(217,185,112,0.45)", offset=0),
                        alt.GradientStop(color="rgba(217,185,112,0.0)", offset=1),
                    ],
                    x1=1, x2=1, y1=0, y2=1,
                ),
            )
            points = base.mark_circle(size=55, color=GOLD, opacity=0.9)
            st.altair_chart(chart_theme((area + points).properties(height=340)), use_container_width=True)

    with right:
        with st.container(border=True):
            section("Revenue by category", "Ranked highest to lowest")
            bars = (
                alt.Chart(category)
                .mark_bar(cornerRadiusEnd=6, height=18)
                .encode(
                    y=alt.Y("category:N", sort="-x", title=None),
                    x=alt.X("revenue:Q", title=None, axis=alt.Axis(format="$~s")),
                    color=alt.Color(
                        "revenue:Q", legend=None,
                        scale=alt.Scale(range=["#6B4E7E", GOLD]),
                    ),
                    tooltip=[alt.Tooltip("category:N", title="Category"), alt.Tooltip("revenue:Q", title="Revenue", format="$,.2f")],
                )
                .properties(height=340)
            )
            st.altair_chart(chart_theme(bars), use_container_width=True)


# ---------------------------------------------------------------------------
# Churn prediction
# ---------------------------------------------------------------------------
elif page == "Churn Prediction":
    hero(
        "Churn prediction",
        "Enter a customer's profile and buying history to estimate how likely they are to stop ordering.",
    )
    model, feature_info, _ = load_models()

    form_col, result_col = st.columns([3, 2], gap="large")

    with form_col:
        with st.container(border=True):
            section("Customer profile")
            a, b = st.columns(2)
            age = a.number_input("Age", 18, 100, 35)
            membership = b.selectbox("Membership type", ["Standard", "Silver", "Gold", "Premium"])

            st.markdown('<div class="panel-gap"></div>', unsafe_allow_html=True)
            section("Buying history")
            c, d = st.columns(2)
            total_orders = c.number_input("Total orders", 1, 1000, 5)
            total_spending = d.number_input("Total spending ($)", 0.0, 10000000.0, 1000.0)
            avg_order = c.number_input("Average order value ($)", 0.0, 1000000.0, 200.0)
            days_last = d.number_input("Days since last order", 0, 2000, 30)
            return_rate = c.number_input("Return rate (0–1)", 0.0, 1.0, 0.05)
            avg_delivery = d.number_input("Average delivery days", 0.0, 30.0, 4.0)

            x = pd.DataFrame([{
                "total_orders": total_orders, "total_spending": total_spending,
                "avg_order_value": avg_order, "days_since_last_order": days_last,
                "return_rate": return_rate, "avg_delivery_days": avg_delivery,
                "age": age, "membership_type": membership,
            }])
            predict = st.button("Predict churn")

    with result_col:
        with st.container(border=True):
            section("Result")
            if predict:
                pred = int(model.predict(x)[0])
                prob = float(model.predict_proba(x)[0][1])
                color = "#E07A7A" if pred == 1 else "#7FC8A9"
                verdict = "Likely to churn" if pred == 1 else "Likely to stay"
                note = (
                    "Consider a win-back offer or a personal check-in soon."
                    if pred == 1
                    else "This customer looks engaged. Keep the experience consistent."
                )
                st.markdown(
                    f"""
                    <div class="result">
                        <div class="dial" style="--p:{prob*100:.1f}; --c:{color};">
                            <div class="dial-inner">
                                <div><div class="dial-num">{prob:.0%}</div><div class="dial-cap">churn probability</div></div>
                            </div>
                        </div>
                        <div>
                            <div class="verdict" style="color:{color};">{verdict}</div>
                            <div class="verdict-note">{note}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="section-note">Fill in the details and press <b>Predict churn</b> to see the probability.</div>',
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------------------------
# Sentiment analysis
# ---------------------------------------------------------------------------
elif page == "Sentiment Analysis":
    hero(
        "Review sentiment",
        "Paste a customer review to see whether it reads as positive, negative or neutral.",
    )
    _, _, model = load_models()

    with st.container(border=True):
        review = st.text_area(
            "Customer review",
            "The product is excellent and I am very happy with my purchase.",
            height=160,
        )
        _, btn_col, _ = st.columns([2, 1, 2])
        analyze = btn_col.button("Analyze sentiment")

    if analyze:
        sentiment = model.predict([review])[0]
        key = str(sentiment).strip().lower()
        palette = {
            "positive": "#7FC8A9", "pos": "#7FC8A9", "1": "#7FC8A9",
            "negative": "#E07A7A", "neg": "#E07A7A", "0": "#E07A7A",
            "neutral": GOLD,
        }
        color = palette.get(key, GOLD)
        with st.container(border=True):
            section("Predicted sentiment")
            st.markdown(
                f"""
                <div class="sentiment" style="color:{color}; border-color:{color}55; background:{color}14;">
                    <span class="dot" style="background:{color};"></span>{str(sentiment).capitalize()}
                </div>
                <div class="quote">“{html.escape(review)}”</div>
                """,
                unsafe_allow_html=True,
            )
