import streamlit as st
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="ConsentGuard OS", layout="centered")

# ---------------- PREMIUM UI CSS ---------------- #
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Glass Card */
.card {
    padding: 25px;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover {
    transform: scale(1.05);
    transition: 0.2s;
}

/* Risk Colors */
.safe { color: #22c55e; font-weight: bold; font-size: 22px; }
.caution { color: #facc15; font-weight: bold; font-size: 22px; }
.risk { color: #ef4444; font-weight: bold; font-size: 22px; }

/* Progress Bar */
.stProgress > div > div > div {
    background-image: linear-gradient(to right, #22c55e, #facc15, #ef4444);
}

</style>
""", unsafe_allow_html=True)

# ---------------- AI LOGIC ---------------- #
def analyze_text(text):
    text = text.lower()
    score = 0
    detected = []

    risky_keywords = {
        "location": 2,
        "tracking": 2,
        "third-party": 2,
        "camera": 3,
        "contacts": 3,
        "microphone": 3,
        "personal data": 2
    }

    for word, value in risky_keywords.items():
        if word in text:
            score += value
            detected.append(word)

    score_percent = min(score * 15, 100)

    if score <= 2:
        return "SAFE", "🟢 Minimal data collection", score_percent, detected
    elif score <= 5:
        return "CAUTION", "🟡 Moderate data usage", score_percent, detected
    else:
        return "HIGH RISK", "🔴 Sensitive data & tracking detected", score_percent, detected


# ---------------- HEADER ---------------- #
st.title("🔐 ConsentGuard OS")
st.caption("AI-Powered System-Level Privacy Protection")

st.markdown("""
<div class="card">
<h2>🧠 AI Privacy Engine Active</h2>
<p>Analyzing permissions, tracking behavior, and consent patterns in real time.</p>
</div>
""", unsafe_allow_html=True)

st.info("Flow: User Action → AI Analysis → Risk Score → Alert → Protection")

# ---------------- SESSION ---------------- #
if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.history = []

# ---------------- INPUT MODE ---------------- #
mode = st.radio("Select Input Type", ["Privacy Policy Text", "App Permissions"])

input_text = ""
app_name = ""
permissions = []

# ---------------- FIXED INPUT UI ---------------- #
if mode == "Privacy Policy Text":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📄 Paste Privacy Policy")
    input_text = st.text_area("", height=150, placeholder="Paste privacy policy here...")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📱 App Installation Simulation")

    app_name = st.selectbox("Select App", ["Instagram", "WhatsApp", "Zoom"])

    permissions = st.multiselect(
        "Requested Permissions",
        ["Camera", "Location", "Contacts", "Microphone", "Storage"]
    )

    input_text = " ".join(permissions)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROTECTION ---------------- #
protection_mode = st.toggle("🛡 Enable Auto Protection Mode")

# ---------------- ANALYZE ---------------- #
if st.button("🚀 Analyze Privacy Risk"):

    if input_text.strip() == "":
        st.warning("Please enter data")

    else:
        result, explanation, score, detected = analyze_text(input_text)

        st.session_state.result = result
        st.session_state.explanation = explanation
        st.session_state.score = score
        st.session_state.detected = detected

        st.session_state.history.append((input_text, result))

# ---------------- RESULT ---------------- #
if st.session_state.result:

    result = st.session_state.result
    explanation = st.session_state.explanation
    score = st.session_state.score
    detected = st.session_state.detected

    st.markdown("---")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("## 🚨 ConsentGuard Alert")

    if mode == "App Permissions":
        st.write(f"📱 App: {app_name}")
        st.write(f"🔑 Permissions: {permissions}")

    # Risk badge
    if result == "SAFE":
        st.markdown("<p class='safe'>🟢 SAFE</p>", unsafe_allow_html=True)
    elif result == "CAUTION":
        st.markdown("<p class='caution'>🟡 CAUTION</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='risk'>🔴 HIGH RISK</p>", unsafe_allow_html=True)

    st.write(explanation)

    # Trust score
    st.markdown("### 🔐 Trust Score")
    st.progress(score)
    st.write(f"**{score}/100 Privacy Safety**")

    # Risk breakdown
    st.write("🔍 Risk Factors:", detected if detected else "None")

    # Dark pattern
    if "accept all" in input_text.lower():
        st.warning("⚠ Dark Pattern Detected")

    # Simple explanation
    simple = {
        "SAFE": "This app is safe 👍",
        "CAUTION": "This app needs some data ⚠",
        "HIGH RISK": "This app can misuse your data ❌"
    }
    st.info("👵 " + simple[result])

    # Protection
    if protection_mode and result == "HIGH RISK":
        st.error("🛡 Auto Protection: Blocked unsafe permissions")

    # Auto fix
    if result == "HIGH RISK":
        if st.button("🔧 Apply Safe Settings"):
            st.success("Permissions minimized")

    # Voice
    if st.button("🔊 Voice Explanation"):
        components.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("Risk level is {result}");
        window.speechSynthesis.speak(msg);
        </script>
        """)

    st.success("✅ Running as OS-Level Simulation")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- HISTORY ---------------- #
if st.session_state.history:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📜 Scan History")

    for item in st.session_state.history[-5:]:
        st.write(item)

    st.markdown('</div>', unsafe_allow_html=True)