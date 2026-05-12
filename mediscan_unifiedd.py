"""
MediScan AI — Unified Single-Page Diagnostic System
All inputs + analysis + full medical report in one flow
"""

import streamlit as st
import numpy as np
import pickle
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from datetime import datetime
import io

try:
    from fpdf import FPDF
    _FPDF_OK = True
except ImportError:
    _FPDF_OK = False

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MediScan AI — Cardio-Pulmonary Diagnostic Platform",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: #080d18;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,180,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(100,255,180,0.05) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, rgba(0,212,255,0.06) 0%, rgba(100,255,218,0.03) 100%);
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 24px;
    padding: 2.8rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative; overflow: hidden;
}
.hero::after {
    content: '🫀';
    position: absolute; right: 3rem; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem; opacity: 0.07;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg, #00d4ff 0%, #64ffda 50%, #00b4ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0; line-height: 1.1;
}
.hero-sub {
    color: rgba(180,210,255,0.6);
    font-size: 1rem; margin-top: 0.6rem; font-weight: 300;
}
.hero-badge {
    display: inline-block; margin-top: 1rem;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 20px; padding: 0.3rem 1rem;
    font-size: 0.78rem; color: #00d4ff;
    font-family: 'Syne', sans-serif; font-weight: 600;
    letter-spacing: 0.08em;
}

/* ── STEP HEADER ── */
.step-header {
    display: flex; align-items: center; gap: 1rem;
    margin: 2rem 0 1.2rem;
}
.step-num {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #00d4ff, #64ffda);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 0.9rem; color: #080d18;
    flex-shrink: 0;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: rgba(200,230,255,0.95);
    letter-spacing: 0.04em;
}
.step-sub { font-size: 0.8rem; color: rgba(150,190,230,0.55); margin-top: 0.1rem; }

/* ── GLASS CARD ── */
.glass {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.6rem;
    margin-bottom: 1rem;
}
.glass-cyan {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 16px; padding: 1.6rem;
    margin-bottom: 1rem;
}

/* ── SECTION LABEL ── */
.label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem; font-weight: 700;
    color: #64ffda; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.9rem;
}

/* ── RESULT CARDS ── */
.res-card {
    border-radius: 16px; padding: 1.6rem;
    border: 2px solid; margin-bottom: 1rem;
}
.res-danger { background: rgba(255,59,59,0.07); border-color: rgba(255,90,90,0.45); }
.res-safe   { background: rgba(0,230,118,0.07); border-color: rgba(0,230,118,0.4); }
.res-warn   { background: rgba(255,196,0,0.07); border-color: rgba(255,196,0,0.4); }
.res-title  { font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700; }
.res-pct    { font-family:'Syne',sans-serif; font-size:2.8rem; font-weight:800; line-height:1; }
.res-sub    { font-size:0.8rem; color:rgba(180,210,255,0.5); margin-top:0.4rem; }

/* ── COMBINED RISK ── */
.combined {
    background: linear-gradient(135deg, rgba(0,212,255,0.07), rgba(100,255,218,0.04));
    border: 2px solid rgba(0,212,255,0.3);
    border-radius: 20px; padding: 2.2rem;
    text-align: center; margin: 1.5rem 0;
}
.combined-label {
    font-family:'Syne',sans-serif; font-size:0.72rem;
    letter-spacing:0.15em; text-transform:uppercase;
    color:#00d4ff; margin-bottom:0.4rem;
}
.combined-score {
    font-family:'Syne',sans-serif;
    font-size:4.5rem; font-weight:800; line-height:1;
}
.combined-verdict { font-size:1rem; font-weight:500; margin-top:0.5rem; }

/* ── METRICS ── */
.mrow { display:flex; gap:0.8rem; flex-wrap:wrap; margin:0.8rem 0; }
.mcrd {
    flex:1; min-width:100px;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px; padding:0.8rem 1rem; text-align:center;
}
.mval { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#64ffda; }
.mname { font-size:0.7rem; color:rgba(180,210,255,0.45); text-transform:uppercase; letter-spacing:0.06em; margin-top:0.15rem; }

/* ── DIVIDER ── */
.divider {
    height:1px;
    background:linear-gradient(90deg, transparent, rgba(0,212,255,0.2), transparent);
    margin: 2rem 0;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(90deg, #00d4ff, #64ffda);
    color: #080d18 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    letter-spacing: 0.04em; width: 100%;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
.stNumberInput > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
.stTextArea > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }

label { color: rgba(180,210,255,0.75) !important; font-size: 0.85rem !important; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(0,212,255,0.03);
    border: 2px dashed rgba(0,212,255,0.25);
    border-radius: 14px; padding: 1rem;
}

/* ── REPORT SECTION ── */
.report-section {
    background: rgba(0,212,255,0.03);
    border: 1px solid rgba(0,212,255,0.12);
    border-left: 3px solid #00d4ff;
    border-radius: 0 14px 14px 0;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.report-section-title {
    font-family:'Syne',sans-serif; font-weight:700;
    font-size:0.85rem; color:#64ffda;
    letter-spacing:0.08em; text-transform:uppercase;
    margin-bottom:0.7rem;
}

/* ── DISCLAIMER ── */
.disclaimer {
    background: rgba(255,196,0,0.04);
    border: 1px solid rgba(255,196,0,0.2);
    border-radius: 12px; padding: 1rem 1.4rem;
    font-size: 0.78rem; color: rgba(180,210,255,0.45);
    line-height: 1.7; margin-top: 2rem;
}

hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def load_heart_model():
    try:
        m = pickle.load(open("heart_model.pkl", "rb"))
        s = pickle.load(open("scaler.pkl",      "rb"))
        return m, s
    except Exception:
        return None, None


@st.cache_resource(show_spinner=False)
def load_pneumonia_model():
    try:
        import tensorflow as tf
        m    = tf.keras.models.load_model("pneumonia_cnn_model.h5")
        meta = pickle.load(open("model_metadata.pkl", "rb"))
        return m, meta
    except Exception:
        return None, None


def predict_heart(model, scaler, features):
    X      = np.array(features, dtype=float).reshape(1, -1)
    Xs     = scaler.transform(X)
    prob   = float(model.predict_proba(Xs)[0][1])
    pred   = int(model.predict(Xs)[0])
    return {"has_disease": pred == 1, "probability": prob}


def predict_pneumonia(model, meta, pil_img):
    sz  = meta.get("img_size", (224, 224))
    img = pil_img.convert("RGB").resize(sz)
    arr = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, 0)
    p   = float(model.predict(arr, verbose=0)[0][0])
    return {"has_pneumonia": p > 0.5, "probability": p}


def combined_risk(hp, pp):
    score = 0.55 * hp + 0.45 * pp
    if   score < 0.30: return score, "LOW RISK",      "#00e676"
    elif score < 0.55: return score, "MODERATE RISK", "#ffc400"
    elif score < 0.75: return score, "HIGH RISK",      "#ff6d00"
    else:              return score, "CRITICAL RISK",  "#ff3b3b"


def risk_level(p):
    if   p < 0.30: return "Low Risk",    "#00e676"
    elif p < 0.70: return "Medium Risk", "#ffc400"
    else:          return "High Risk",   "#ff3b3b"


def _safe(t):
    for u, a in {
        "\u2014":"--","\u2013":"-","\u2018":"'","\u2019":"'",
        "\u201c":'"', "\u201d":'"', "\u2022":"*", "\u2265":">=",
        "\u2264":"<=","\u00b0":" deg","\u2192":"->",
    }.items():
        t = t.replace(u, a)
    return t.encode("latin-1", errors="replace").decode("latin-1")


def gauge(value, title, color, height=240):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 28, "color": "white"}},
        title={"text": title, "font": {"size": 13, "color": "rgba(200,230,255,0.6)"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "rgba(200,230,255,0.3)"},
            "bar":  {"color": color, "thickness": 0.28},
            "bgcolor": "rgba(255,255,255,0.02)",
            "bordercolor": "rgba(255,255,255,0.06)",
            "steps": [
                {"range": [0,  30], "color": "rgba(0,230,118,0.1)"},
                {"range": [30, 70], "color": "rgba(255,196,0,0.08)"},
                {"range": [70,100], "color": "rgba(255,59,59,0.12)"},
            ],
            "threshold": {"line": {"color": color, "width": 3},
                          "thickness": 0.8, "value": value},
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"}, height=height,
        margin=dict(t=55, b=10, l=20, r=20)
    )
    return fig


# ══════════════════════════════════════════════════════════════
# LOAD MODELS
# ══════════════════════════════════════════════════════════════
heart_model,  heart_scaler  = load_heart_model()
pneumo_model, pneumo_meta   = load_pneumonia_model()

# ══════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-title">MediScan AI</div>
    <div class="hero-sub">
        Integrated Cardio-Pulmonary Diagnostic Platform &nbsp;·&nbsp;
        Heart Disease Risk Assessment &amp; Pneumonia Screening
    </div>
    <div class="hero-badge">AI-POWERED · RESEARCH &amp; EDUCATIONAL USE ONLY</div>
</div>
""", unsafe_allow_html=True)

# Model status strip
h_ok = heart_model  is not None
p_ok = pneumo_model is not None
st.markdown(f"""
<div style="display:flex; gap:1rem; margin-bottom:2rem; flex-wrap:wrap">
    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:0.5rem 1.2rem; font-size:0.82rem;">
        🫀 Heart Model &nbsp;<b style="color:{'#00e676' if h_ok else '#ff3b3b'}">
        {'● Loaded' if h_ok else '● Not Found'}</b>
    </div>
    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
                border-radius:10px; padding:0.5rem 1.2rem; font-size:0.82rem;">
        🫁 Pneumonia CNN &nbsp;<b style="color:{'#00e676' if p_ok else '#ff3b3b'}">
        {'● Loaded' if p_ok else '● Not Found'}</b>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# STEP 1 — PATIENT INFORMATION
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-header">
    <div class="step-num">1</div>
    <div>
        <div class="step-title">Patient Information</div>
        <div class="step-sub">Personal and demographic details for the medical report — all fields optional except Age and Sex</div>
    </div>
</div>
""", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)
with p1:
    pt_name   = st.text_input("Full Name",   placeholder="e.g. Ahmed Mohamed")
    pt_id     = st.text_input("Patient ID",  placeholder="e.g. PT-00123")
with p2:
    pt_age_r  = st.number_input("Age", min_value=1, max_value=120, value=45)
    pt_sex_r  = st.selectbox("Sex", ["Male", "Female", "Other"])
with p3:
    pt_dob    = st.text_input("Date of Birth", placeholder="DD/MM/YYYY")
    pt_phone  = st.text_input("Contact / Phone", placeholder="Optional")

pt_notes = st.text_area(
    "Clinical Notes / Chief Complaint",
    placeholder="Describe presenting symptoms, relevant medical history, current medications, allergies, or other pertinent clinical observations…",
    height=90
)


# ══════════════════════════════════════════════════════════════
# STEP 2 — CARDIAC PARAMETERS
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="step-header">
    <div class="step-num">2</div>
    <div>
        <div class="step-title">Cardiac Parameters</div>
        <div class="step-sub">Used by the AI heart disease classifier</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.15);
            border-radius:12px; padding:0.9rem 1.2rem; margin-bottom:1.2rem;
            font-size:0.82rem; color:rgba(180,210,255,0.65); line-height:1.7">
    <b style="color:#64ffda">ℹ️ Note on Chest Pain Classification:</b>&nbsp;
    The chest pain field uses the standard AHA/UCI clinical encoding. Patients with
    <em>no chest symptoms</em> should be entered as <b>Asymptomatic</b> — this is a valid
    and common presentation, not an error. "Typical Angina" refers specifically to
    exertional chest tightness relieved by rest or nitrates.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
cp_map = {
    "Typical Angina — Chest tightness on exertion, relieved by rest":          1,
    "Atypical Angina — Chest discomfort not fitting classic angina pattern":    2,
    "Non-Anginal Pain — Chest pain unrelated to cardiac ischaemia":             3,
    "Asymptomatic — No chest pain or discomfort reported":                      4,
}
with c1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="label">Demographics</div>', unsafe_allow_html=True)
    age      = st.number_input("Age (years)", 1, 120, pt_age_r, key="h_age")
    sex_sel  = st.selectbox("Sex", ["Male", "Female"], key="h_sex",
                             index=0 if pt_sex_r == "Male" else 0)
    sex_val  = 1 if sex_sel == "Male" else 0
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="label">Vitals</div>', unsafe_allow_html=True)
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 50, 250, 120,
                                help="Measured at rest on hospital admission")
    chol     = st.number_input("Serum Cholesterol (mg/dl)", 100, 600, 200,
                                help="Total serum cholesterol via BMI")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="label">Cardiac Indicators</div>', unsafe_allow_html=True)
    cp       = st.selectbox(
        "Chest Pain Type",
        list(cp_map.keys()),
        help="Select 'Asymptomatic' if the patient reports no chest pain. "
             "This is a clinical classification, not a severity score."
    )
    thalach  = st.number_input("Max Heart Rate Achieved (bpm)", 50, 250, 150,
                                help="Peak heart rate recorded during exercise stress test")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# STEP 3 — CHEST X-RAY
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="step-header">
    <div class="step-num">3</div>
    <div>
        <div class="step-title">Chest X-Ray Upload</div>
        <div class="step-sub">Posterior-anterior (PA) view recommended · Analysed by VGG16 CNN transfer learning model for pneumonia detection</div>
    </div>
</div>
""", unsafe_allow_html=True)

xray_col, prev_col = st.columns([1, 1])
with xray_col:
    uploaded = st.file_uploader(
        "Upload Chest X-Ray (JPG / PNG)",
        type=["jpg","jpeg","png"],
        label_visibility="collapsed"
    )
with prev_col:
    if uploaded:
        xray_img = Image.open(uploaded)
        st.image(xray_img, caption="Uploaded X-Ray",
                 use_container_width=True, clamp=True)
    else:
        st.markdown("""
        <div style="border:2px dashed rgba(0,212,255,0.2); border-radius:14px;
                    height:180px; display:flex; align-items:center; justify-content:center;
                    color:rgba(150,190,230,0.3); font-size:0.9rem; flex-direction:column; gap:0.5rem">
            <span style="font-size:2.5rem">🩻</span>
            <span>X-ray preview appears here</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ANALYSE BUTTON
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
run = st.button("🔬  Run Integrated Cardio-Pulmonary Analysis", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════
if run:

    # ── Validations ──────────────────────────────────────────
    errors = []
    if not h_ok:   errors.append("heart_model.pkl / scaler.pkl not found")
    if not p_ok:   errors.append("pneumonia_cnn_model.h5 / model_metadata.pkl not found")
    if not uploaded: errors.append("Please upload a chest X-ray image")
    if errors:
        for e in errors:
            st.error(f"❌ {e}")
        st.stop()

    # ── Run models ───────────────────────────────────────────
    with st.spinner("Running AI analysis…"):
        features = [age, sex_val, cp_map[cp], trestbps, chol, thalach]
        hr = predict_heart(heart_model, heart_scaler, features)
        pr = predict_pneumonia(pneumo_model, pneumo_meta, xray_img)

    h_prob  = hr["probability"]
    p_prob  = pr["probability"]
    h_pct   = h_prob * 100
    p_pct   = p_prob * 100
    n_pct   = (1 - p_prob) * 100
    score, risk_lvl, risk_col = combined_risk(h_prob, p_prob)
    score_pct = score * 100
    h_rlvl, h_rcol = risk_level(h_prob)
    report_time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    dual_pos = hr["has_disease"] and pr["has_pneumonia"]

    h_color = "#ff6b6b" if hr["has_disease"] else "#00e676"
    p_color = "#ff6b6b" if pr["has_pneumonia"] else "#00e676"

    # ── RESULTS HEADER ───────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <div class="step-num" style="background:linear-gradient(135deg,#ff6b6b,#ff3b3b); color:white">✦</div>
        <div>
            <div class="step-title">Diagnostic Results</div>
            <div class="step-sub">AI analysis complete — review findings below</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── COMBINED RISK BANNER ─────────────────────────────────
    st.markdown(f"""
    <div class="combined">
        <div class="combined-label">Combined Cardio-Pulmonary Risk Score</div>
        <div class="combined-score" style="color:{risk_col}">{score_pct:.1f}%</div>
        <div class="combined-verdict" style="color:{risk_col}">{risk_lvl}</div>
        <div style="font-size:0.78rem; color:rgba(180,210,255,0.4); margin-top:0.6rem">
            Weighted: 55% cardiac · 45% pulmonary
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SIDE-BY-SIDE RESULTS ─────────────────────────────────
    r1, r2 = st.columns(2)

    with r1:
        cls = "res-danger" if hr["has_disease"] else "res-safe"
        lbl = "⚠️ Heart Disease Detected" if hr["has_disease"] else "✅ No Heart Disease"
        st.markdown(f"""
        <div class="res-card {cls}">
            <div class="res-title" style="color:{h_color}">{lbl}</div>
            <div class="res-pct"   style="color:{h_color}">{h_pct:.1f}%</div>
            <div class="res-sub">Cardiac disease probability · AI Classifier</div>
            <div style="margin-top:0.8rem; display:inline-block; background:rgba(255,255,255,0.06);
                        border-radius:8px; padding:0.25rem 0.75rem; font-size:0.8rem;
                        color:{h_rcol}; font-family:Syne,sans-serif; font-weight:700">
                {h_rlvl}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        cls2 = "res-danger" if pr["has_pneumonia"] else "res-safe"
        lbl2 = "⚠️ Pneumonia Detected" if pr["has_pneumonia"] else "✅ No Pneumonia — Normal X-Ray"
        st.markdown(f"""
        <div class="res-card {cls2}">
            <div class="res-title" style="color:{p_color}">{lbl2}</div>
            <div class="res-pct"   style="color:{p_color}">{p_pct:.1f}%</div>
            <div class="res-sub">P(Pneumonia) · VGG16 Transfer Learning CNN</div>
            <div style="margin-top:0.8rem; display:inline-block; background:rgba(255,255,255,0.06);
                        border-radius:8px; padding:0.25rem 0.75rem; font-size:0.8rem;
                        color:{p_color}; font-family:Syne,sans-serif; font-weight:700">
                {'High Confidence' if max(p_prob, 1-p_prob) > 0.75 else 'Moderate Confidence'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 3 GAUGES ─────────────────────────────────────────────
    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(gauge(score_pct, "Combined Risk",   risk_col),  use_container_width=True)
    with g2: st.plotly_chart(gauge(h_pct,     "🫀 Cardiac Risk",  h_color),   use_container_width=True)
    with g3: st.plotly_chart(gauge(p_pct,     "🫁 Pneumonia Risk", p_color),  use_container_width=True)

    # ── PATIENT METRICS ──────────────────────────────────────
    st.markdown(f"""
    <div class="mrow">
        <div class="mcrd"><div class="mval">{age}</div><div class="mname">Age</div></div>
        <div class="mcrd"><div class="mval">{sex_sel}</div><div class="mname">Sex</div></div>
        <div class="mcrd"><div class="mval">{trestbps}</div><div class="mname">BP mmHg</div></div>
        <div class="mcrd"><div class="mval">{chol}</div><div class="mname">Cholesterol</div></div>
        <div class="mcrd"><div class="mval">{thalach}</div><div class="mname">Max HR</div></div>
        <div class="mcrd"><div class="mval" style="color:{h_color}">{h_pct:.0f}%</div><div class="mname">Cardiac Prob</div></div>
        <div class="mcrd"><div class="mval" style="color:{p_color}">{p_pct:.0f}%</div><div class="mname">Pneumo Prob</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── RADAR CHART ──────────────────────────────────────────
    radar_col, bar_col = st.columns(2)

    with radar_col:
        age_n  = min(100, max(0, (age - 20) / 70 * 100))
        bp_n   = min(100, max(0, (trestbps - 80) / 120 * 100))
        ch_n   = min(100, max(0, (chol - 100) / 300 * 100))
        hr_n   = min(100, max(0, (thalach - 60) / 160 * 100))
        cats   = ["Age Factor", "Blood Pressure", "Cholesterol", "Max Heart Rate", "Cardiac Risk", "Pneumonia Risk"]
        vals   = [age_n, bp_n, ch_n, hr_n, h_pct, p_pct]
        fig_r  = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(0,212,255,0.10)",
            line=dict(color="#00d4ff", width=2),
        ))
        fig_r.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0.02)",
                radialaxis=dict(visible=True, range=[0,100],
                                gridcolor="rgba(255,255,255,0.08)",
                                tickfont=dict(color="rgba(200,230,255,0.35)", size=8)),
                angularaxis=dict(tickfont=dict(color="rgba(200,230,255,0.7)", size=10)),
            ),
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"),
            height=310, showlegend=False,
            margin=dict(t=20, b=20, l=40, r=40),
            title=dict(text="Health Dimension Profile",
                       font=dict(size=12, color="rgba(200,230,255,0.55)"))
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with bar_col:
        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(
            x=["🫀 Cardiac", "🫁 Pneumonia", "Combined"],
            y=[h_pct, p_pct, score_pct],
            marker_color=[h_color, p_color, risk_col],
            text=[f"{h_pct:.1f}%", f"{p_pct:.1f}%", f"{score_pct:.1f}%"],
            textposition="outside",
            textfont=dict(color="white", size=12, family="Syne"),
        ))
        fig_b.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), height=310,
            yaxis=dict(range=[0,120], ticksuffix="%",
                       gridcolor="rgba(255,255,255,0.05)"),
            xaxis=dict(tickfont=dict(color="rgba(200,230,255,0.65)")),
            margin=dict(t=20, b=20, l=10, r=10),
            title=dict(text="Risk Component Breakdown",
                       font=dict(size=12, color="rgba(200,230,255,0.55)"))
        )
        st.plotly_chart(fig_b, use_container_width=True)

    # ── CLINICAL FINDINGS ────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <div class="step-num" style="background:rgba(0,212,255,0.15); color:#00d4ff; border:1px solid rgba(0,212,255,0.3)">🔬</div>
        <div>
            <div class="step-title">Clinical Assessment</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    findings = []
    if hr["has_disease"]:
        findings.append("Significant cardiac disease risk indicators detected — AI classifier confidence above decision threshold.")
    if pr["has_pneumonia"]:
        findings.append("Radiological signs consistent with pneumonia — VGG16 CNN confidence above 50% threshold.")
    if dual_pos:
        findings.append("Co-occurrence of cardiac and pulmonary findings may indicate systemic inflammatory process or compounded cardiovascular burden.")
    if not findings:
        findings.append("No significant pathology detected in either cardiopulmonary system at current thresholds.")
    if chol > 240:
        findings.append(f"Elevated cholesterol ({chol} mg/dl) — above the 240 mg/dl threshold for hypercholesterolaemia.")
    if trestbps > 140:
        findings.append(f"Elevated resting blood pressure ({trestbps} mm Hg) — consistent with Stage 2 hypertension range.")

    if score >= 0.75:
        recs = [
            ("🚨", "Immediate specialist referral — do not delay."),
            ("🏥", "Urgent cardiology + pulmonology consultation advised."),
            ("📋", "Consider hospital admission for comprehensive evaluation."),
            ("💉", "Request: CBC, BMP, troponin, BNP, CRP, procalcitonin."),
            ("🫁", "High-resolution CT chest may be warranted."),
        ]
    elif score >= 0.55:
        recs = [
            ("📅", "Schedule specialist follow-up within 1–2 weeks."),
            ("🔁", "Repeat chest imaging in 4–6 weeks to monitor progression."),
            ("📈", "Monitor symptoms closely and track changes daily."),
            ("🩺", "Consider echocardiogram and pulmonary function tests."),
        ]
    elif score >= 0.30:
        recs = [
            ("🩺", "Routine follow-up with primary care physician."),
            ("🏃", "Lifestyle modifications: diet, exercise, smoking cessation."),
            ("🔁", "Repeat screening in 6 months."),
            ("📊", "Consider lipid panel and glucose tolerance test."),
        ]
    else:
        recs = [
            ("✅", "Continue routine annual health monitoring."),
            ("🏃", "Maintain healthy lifestyle habits."),
            ("📅", "Schedule standard annual health check-up."),
            ("💡", "Stay up to date with influenza and pneumococcal vaccinations."),
        ]

    fa, ra = st.columns(2)
    with fa:
        fhtml = "".join(
            f"<div style='padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.04); font-size:0.86rem; color:rgba(200,230,255,0.82)'>• {f}</div>"
            for f in findings
        )
        st.markdown(f"""
        <div class="glass-cyan">
            <div class="label">Key Findings</div>
            <div style="margin-bottom:0.8rem; font-size:0.85rem">
                <b>🫀 Cardiac Screen:</b>&nbsp;
                <span style="color:{h_color}">{'⚠️ Positive' if hr['has_disease'] else '✅ Negative'}</span>
                &nbsp;·&nbsp; {h_pct:.1f}%
            </div>
            <div style="margin-bottom:1rem; font-size:0.85rem">
                <b>🫁 Pulmonary Screen:</b>&nbsp;
                <span style="color:{p_color}">{'⚠️ Positive' if pr['has_pneumonia'] else '✅ Negative'}</span>
                &nbsp;·&nbsp; {p_pct:.1f}%
            </div>
            {fhtml}
        </div>
        """, unsafe_allow_html=True)

    with ra:
        rhtml = "".join(
            f"<div style='display:flex; gap:0.6rem; margin-bottom:0.65rem; align-items:flex-start'>"
            f"<span style='font-size:1rem; flex-shrink:0'>{ic}</span>"
            f"<span style='font-size:0.85rem; color:rgba(200,230,255,0.8); line-height:1.5'>{tx}</span></div>"
            for ic, tx in recs
        )
        st.markdown(f"""
        <div class="glass-cyan">
            <div class="label">Recommendations</div>
            {rhtml}
        </div>
        """, unsafe_allow_html=True)

    # ── INVESTIGATIONS & REFERRALS ───────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    inv_col, ref_col = st.columns(2)

    inv_rows = [
        ("Complete Blood Count (CBC)", "Baseline haematological status", "Routine"),
        ("Basic Metabolic Panel", "Electrolytes, renal function, glucose", "Routine"),
    ]
    if hr["has_disease"] or h_pct >= 30:
        inv_rows += [
            ("12-Lead ECG", "Cardiac rhythm and ischaemia", "Priority" if hr["has_disease"] else "Elective"),
            ("Echocardiogram", "Structural cardiac assessment", "Priority" if hr["has_disease"] else "Elective"),
            ("Troponin I / T", "Myocardial injury marker", "Urgent" if h_pct >= 70 else "Priority"),
            ("Lipid Panel (Fasting)", "LDL, HDL, triglycerides", "Routine"),
        ]
    if pr["has_pneumonia"] or p_pct >= 30:
        inv_rows += [
            ("Chest X-Ray (PA + Lateral)", "Characterise infiltrates", "Priority" if pr["has_pneumonia"] else "Elective"),
            ("Sputum Culture & Sensitivity", "Identify causative organism", "Priority"),
            ("Procalcitonin", "Bacterial infection severity", "Urgent" if p_pct >= 70 else "Priority"),
            ("Oxygen Saturation / ABG", "Respiratory gas exchange", "Urgent" if pr["has_pneumonia"] else "Routine"),
        ]

    with inv_col:
        st.markdown('<div class="label">🧪 Recommended Investigations</div>', unsafe_allow_html=True)
        inv_df = pd.DataFrame(inv_rows, columns=["Investigation", "Purpose", "Priority"])
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

    referral_data = {
        "Specialist": ["Cardiologist", "Pulmonologist", "GP", "Radiologist"],
        "Indicated?": [
            "🔴 Yes" if hr["has_disease"] else "🟡 Consider" if h_pct >= 30 else "✅ Not Required",
            "🔴 Yes" if pr["has_pneumonia"] else "🟡 Consider" if p_pct >= 30 else "✅ Not Required",
            "🔴 Priority" if score >= 0.55 else "🟡 Routine",
            "🔴 Yes" if pr["has_pneumonia"] else "🟡 Consider",
        ],
        "Timeframe": [
            "Immediate" if hr["has_disease"] and h_pct >= 70 else "1–2 weeks" if hr["has_disease"] else "6 months",
            "Immediate" if pr["has_pneumonia"] and p_pct >= 70 else "1–2 weeks" if pr["has_pneumonia"] else "Annual",
            "1 week" if score >= 0.55 else "6 weeks",
            "1–2 weeks" if pr["has_pneumonia"] else "Routine",
        ],
    }
    with ref_col:
        st.markdown('<div class="label">🏥 Specialist Referral Matrix</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(referral_data), use_container_width=True, hide_index=True)

    # ── PDF REPORT ───────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="step-header">
        <div class="step-num" style="background:rgba(0,212,255,0.15); color:#00d4ff; border:1px solid rgba(0,212,255,0.3)">📄</div>
        <div>
            <div class="step-title">Download Full Medical Report</div>
            <div class="step-sub">PDF report with all findings, recommendations, and patient info</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if _FPDF_OK:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # ── Header ─────────────────────────────────────────
        pdf.set_fill_color(8, 13, 24)
        pdf.rect(0, 0, 210, 45, "F")
        pdf.set_text_color(0, 212, 255)
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 14, _safe("MediScan AI — Integrated Cardio-Pulmonary Report"),
                 ln=True, align="C")
        pdf.set_font("Arial", size=9)
        pdf.set_text_color(150, 180, 220)
        pdf.cell(0, 8, _safe(f"Generated: {report_time}   |   CONFIDENTIAL — For Clinical Use Only"),
                 ln=True, align="C")
        pdf.ln(12)
        pdf.set_text_color(0, 0, 0)

        # ── Patient Info ────────────────────────────────────
        pdf.set_fill_color(230, 245, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "PATIENT INFORMATION", ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for k, v in [
            ("Name",            pt_name   or "—"),
            ("Patient ID",      pt_id     or "—"),
            ("Age",             str(pt_age_r)),
            ("Sex",             pt_sex_r),
            ("Date of Birth",   pt_dob    or "—"),
            ("Contact",         pt_phone  or "—"),
            ("Date of Report",  report_time),
        ]:
            pdf.cell(60, 8, _safe(f"{k}:"), border=0)
            pdf.cell(0,  8, _safe(str(v)), ln=True)
        if pt_notes:
            pdf.ln(2)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "Clinical Notes:", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 7, _safe(pt_notes))
        pdf.ln(4)

        # ── Combined Risk ───────────────────────────────────
        pdf.set_fill_color(220, 240, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "COMBINED CARDIOPULMONARY RISK ASSESSMENT", ln=True, fill=True)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 9, _safe(f"Combined Risk Score  : {score_pct:.1f}%   |   {risk_lvl}"), ln=True)
        pdf.cell(0, 9, _safe(f"Cardiac Disease Risk : {h_pct:.1f}%   |   {'POSITIVE' if hr['has_disease'] else 'NEGATIVE'}"), ln=True)
        pdf.cell(0, 9, _safe(f"Pneumonia Risk       : {p_pct:.1f}%   |   {'POSITIVE' if pr['has_pneumonia'] else 'NEGATIVE'}"), ln=True)
        pdf.ln(4)

        # ── Cardiac Parameters ──────────────────────────────
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "CARDIAC PARAMETERS", ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for k, v in [
            ("Age",                  age),
            ("Sex",                  sex_sel),
            ("Chest Pain Type",      cp),
            ("Resting BP (mm Hg)",   trestbps),
            ("Cholesterol (mg/dl)",  chol),
            ("Max Heart Rate",       thalach),
        ]:
            pdf.cell(70, 8, _safe(f"{k}:"))
            pdf.cell(0,  8, _safe(str(v)), ln=True)
        pdf.ln(4)

        # ── Clinical Findings ───────────────────────────────
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "CLINICAL FINDINGS", ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for f in findings:
            pdf.multi_cell(0, 8, _safe(f"  * {f}"))
        pdf.ln(4)

        # ── Recommendations ─────────────────────────────────
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "RECOMMENDATIONS", ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for _, tx in recs:
            pdf.multi_cell(0, 8, _safe(f"  -> {tx}"))
        pdf.ln(4)

        # ── Investigations ──────────────────────────────────
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "RECOMMENDED INVESTIGATIONS", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        for inv, pur, pri in inv_rows:
            pdf.multi_cell(0, 7, _safe(f"  [{pri}]  {inv} — {pur}"))
        pdf.ln(4)

        # ── Referral Matrix ─────────────────────────────────
        pdf.set_fill_color(240, 248, 255)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "SPECIALIST REFERRAL MATRIX", ln=True, fill=True)
        pdf.set_font("Arial", size=11)
        for sp, ind, tf in zip(
            referral_data["Specialist"],
            referral_data["Indicated?"],
            referral_data["Timeframe"]
        ):
            ind_clean = ind.replace("🔴","[!]").replace("🟡","[~]").replace("✅","[OK]")
            pdf.cell(0, 8, _safe(f"  {sp}: {ind_clean}  —  {tf}"), ln=True)
        pdf.ln(4)

        # ── Disclaimer ──────────────────────────────────────
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.multi_cell(0, 6, _safe(
            "DISCLAIMER: This report is generated by an AI-based research tool and is intended for "
            "educational and research purposes only. It does not constitute a medical diagnosis or "
            "replace professional clinical judgement. Always consult a qualified and licensed "
            "healthcare professional before making any medical decisions."
        ))

        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        fname = f"MediScan_{(pt_name or 'Patient').replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

        st.download_button(
            label="📄  Download Full Integrated Medical Report (PDF)",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.warning("Install `fpdf` to enable PDF export: `pip install fpdf`")

    # ── DISCLAIMER FOOTER ────────────────────────────────────
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <b>Medical Disclaimer:</b> This integrated report is produced by AI models for research and
        educational purposes only. Probabilities shown are model outputs, not clinical diagnoses.
        All findings must be correlated with clinical history, physical examination, and validated
        diagnostic workup by a licensed healthcare professional. Do not make treatment decisions
        based solely on this output.
    </div>
    """, unsafe_allow_html=True)
