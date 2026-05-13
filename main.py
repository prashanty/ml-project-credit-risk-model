import streamlit as st
from prediction_helper import predict

st.set_page_config(
    page_title="Kredix Finance · Credit Risk",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS (Dark Theme) ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }
.stApp { background: #0d1117; }

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div > input,
input[type="number"] {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] svg { fill: #8b949e !important; }
div[data-baseweb="popover"] > div { background: #161b22 !important; border-color: #30363d !important; }
li[role="option"] { color: #e2e8f0 !important; background: #161b22 !important; }
li[role="option"]:hover { background: #21262d !important; }

label[data-testid="stWidgetLabel"] p {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #8b949e !important;
}

.app-header {
    background: linear-gradient(135deg, #0d1f35 0%, #0d2d4f 55%, #0e3a63 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header h1 { font-size: 1.7rem; font-weight: 600; margin: 0; letter-spacing: -0.3px; color: #f0f6ff; }
.app-header p  { font-size: 0.9rem; margin: 0.3rem 0 0; color: rgba(255,255,255,0.5); font-weight: 300; }
.header-badge {
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.78rem;
    color: #63b3ed;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.5px;
}

.section-card {
    background: #161b22;
    border-radius: 14px;
    padding: 1.5rem 1.75rem 1.25rem;
    margin-bottom: 1rem;
    border: 1px solid #21262d;
    box-shadow: 0 1px 8px rgba(0,0,0,0.3);
}
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #4a7fa8;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #21262d;
}

.ratio-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin-top: 0.35rem;
}
.ratio-label { font-size: 0.75rem; color: #6e7681; margin-bottom: 2px; }
.ratio-value { font-family: 'DM Mono', monospace; font-size: 1.25rem; font-weight: 500; color: #e2e8f0; }
.ratio-tag { font-size: 0.68rem; font-weight: 500; padding: 2px 8px; border-radius: 20px; margin-left: 6px; vertical-align: middle; }
.tag-low    { background: rgba(34,197,94,0.15);  color: #4ade80; }
.tag-medium { background: rgba(245,158,11,0.15); color: #fbbf24; }
.tag-high   { background: rgba(239,68,68,0.15);  color: #f87171; }

.stSlider [data-testid="stTickBar"] { display: none; }
hr { border-color: #21262d !important; }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a4a7a, #2563eb) !important;
    color: #f0f6ff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 20px rgba(37,99,235,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 28px rgba(37,99,235,0.5) !important;
    transform: translateY(-1px) !important;
}

.result-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.25rem; }
.result-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.result-card .rc-label {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.9px;
    text-transform: uppercase; color: #4a7fa8; margin-bottom: 0.5rem;
}
.result-card .rc-value { font-size: 2rem; font-weight: 600; font-family: 'DM Mono', monospace; line-height: 1.1; }
.result-card .rc-sub   { font-size: 0.78rem; color: #6e7681; margin-top: 0.3rem; }

.rc-prob             { color: #f87171; }
.rc-score            { color: #93c5fd; }
.rc-rating-poor      { color: #f87171; }
.rc-rating-average   { color: #fbbf24; }
.rc-rating-good      { color: #60a5fa; }
.rc-rating-excellent { color: #4ade80; }

.score-bar-wrap {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.score-bar-track {
    position: relative; height: 10px; border-radius: 99px;
    background: linear-gradient(to right, #ef4444 0%, #f59e0b 30%, #38bdf8 55%, #22c55e 80%);
    margin: 0.75rem 0; overflow: visible;
}
.score-bar-needle {
    position: absolute; top: -5px; width: 20px; height: 20px; border-radius: 50%;
    background: #0d1117; border: 3px solid #93c5fd;
    box-shadow: 0 0 10px rgba(147,197,253,0.5); transform: translateX(-50%);
}
.score-bar-labels {
    display: flex; justify-content: space-between;
    font-size: 0.7rem; color: #6e7681; font-family: 'DM Mono', monospace; margin-top: 0.2rem;
}
.score-zone-labels { display: flex; justify-content: space-between; font-size: 0.68rem; font-weight: 500; margin-top: 0.5rem; }

.rec-banner { border-radius: 10px; padding: 1rem 1.25rem; font-size: 0.88rem; margin-top: 1rem; border-left: 4px solid; }
.rec-approve { background: rgba(34,197,94,0.08);  border-color: #22c55e; color: #4ade80; }
.rec-review  { background: rgba(245,158,11,0.08); border-color: #f59e0b; color: #fbbf24; }
.rec-reject  { background: rgba(239,68,68,0.08);  border-color: #ef4444; color: #f87171; }
.rec-icon    { font-size: 1.1rem; margin-right: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <div>
    <h1>📊 Kredix Finance</h1>
    <p>Credit Risk Assessment Platform · Powered by ML</p>
  </div>
  <div class="header-badge">RISK ENGINE v2.0</div>
</div>
""", unsafe_allow_html=True)


# ── Section 1: Applicant Profile ──────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">01 · Applicant Profile</div>', unsafe_allow_html=True)
row1 = st.columns(3)
with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
with row1[1]:
    income = st.number_input('Income (₹)', min_value=0, value=1_200_000, step=10_000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2_560_000, step=10_000)
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 2: Loan Structure ─────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">02 · Loan Structure</div>', unsafe_allow_html=True)
row2 = st.columns(3)

loan_to_income_ratio = loan_amount / income if income > 0 else 0
if loan_to_income_ratio < 2:
    lti_tag = '<span class="ratio-tag tag-low">Low</span>'
elif loan_to_income_ratio < 4:
    lti_tag = '<span class="ratio-tag tag-medium">Moderate</span>'
else:
    lti_tag = '<span class="ratio-tag tag-high">High</span>'

with row2[0]:
    st.markdown(f"""
    <div style="margin-bottom:0.5rem">
      <div style="font-size:0.82rem;font-weight:500;color:#8b949e;margin-bottom:6px">Loan to Income Ratio</div>
      <div class="ratio-box">
        <div class="ratio-value">{loan_to_income_ratio:.2f}x {lti_tag}</div>
        <div class="ratio-label" style="margin-top:2px">auto-calculated</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (Months)', min_value=0, step=1, value=36)
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20,
                                               help="Average Days Past Due per delinquency event")
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 3: Credit Behaviour ───────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">03 · Credit Behaviour</div>', unsafe_allow_html=True)
row3 = st.columns(3)
with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization (%)', min_value=0, max_value=100, step=1, value=30)
with row3[2]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)
st.markdown('</div>', unsafe_allow_html=True)


# ── Section 4: Loan Classification ───────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">04 · Loan Classification</div>', unsafe_allow_html=True)
row4 = st.columns(3)
with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])
st.markdown('</div>', unsafe_allow_html=True)


# ── Calculate Button ──────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
calculate = st.button('Calculate Credit Risk →')


# ── Results ───────────────────────────────────────────────────────────────────
if calculate:
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    rating_class = {
        'Poor': 'rc-rating-poor', 'Average': 'rc-rating-average',
        'Good': 'rc-rating-good', 'Excellent': 'rc-rating-excellent',
    }.get(rating, 'rc-score')

    rating_emoji = {'Poor': '🔴', 'Average': '🟡', 'Good': '🔵', 'Excellent': '🟢'}.get(rating, '')

    if rating in ('Excellent', 'Good'):
        rec_class, rec_icon = 'rec-approve', '✅'
        rec_text = '<strong>Recommended for Approval.</strong> Applicant demonstrates strong creditworthiness. Proceed with standard verification.'
    elif rating == 'Average':
        rec_class, rec_icon = 'rec-review', '⚠️'
        rec_text = '<strong>Manual Review Required.</strong> Moderate risk profile detected. Consider additional documentation, higher interest rate, or a co-applicant.'
    else:
        rec_class, rec_icon = 'rec-reject', '❌'
        rec_text = '<strong>Not Recommended.</strong> High probability of default. Consider rejecting or applying significantly stricter loan terms.'

    st.markdown("---")
    st.markdown("<div style='font-size:0.7rem;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;color:#4a7fa8;margin-bottom:0.8rem'>Assessment Results</div>", unsafe_allow_html=True)

    needle_pct = ((credit_score - 300) / 600) * 100
    st.markdown(f"""
    <div class="result-grid">
      <div class="result-card">
        <div class="rc-label">Default Probability</div>
        <div class="rc-value rc-prob">{probability:.1%}</div>
        <div class="rc-sub">Likelihood of default</div>
      </div>
      <div class="result-card">
        <div class="rc-label">Credit Score</div>
        <div class="rc-value rc-score">{credit_score}</div>
        <div class="rc-sub">Range: 300 – 900</div>
      </div>
      <div class="result-card">
        <div class="rc-label">Rating</div>
        <div class="rc-value {rating_class}">{rating_emoji} {rating}</div>
        <div class="rc-sub">Based on credit score</div>
      </div>
    </div>

    <div class="score-bar-wrap">
      <div style="font-size:0.72rem;font-weight:600;letter-spacing:0.9px;text-transform:uppercase;color:#4a7fa8">Credit Score Gauge</div>
      <div class="score-bar-track">
        <div class="score-bar-needle" style="left:{needle_pct:.1f}%"></div>
      </div>
      <div class="score-bar-labels">
        <span>300</span><span>450</span><span>600</span><span>750</span><span>900</span>
      </div>
      <div class="score-zone-labels">
        <span style="color:#f87171">Poor</span>
        <span style="color:#fbbf24">Average</span>
        <span style="color:#38bdf8">Good</span>
        <span style="color:#4ade80">Excellent</span>
      </div>
    </div>

    <div class="rec-banner {rec_class}">
      <span class="rec-icon">{rec_icon}</span>{rec_text}
    </div>
    """, unsafe_allow_html=True)