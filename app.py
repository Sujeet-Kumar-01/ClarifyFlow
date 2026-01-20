import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ===============================
# 1. Gemini Setup
# ===============================
os.environ["GOOGLE_API_KEY"] = "AIzaSyDdKtmcCToeyDploYO_4XRUy0cHP9UiX-s"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

# ===============================
# 2. Page Configuration
# ===============================
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

# ===============================
# 3. Global Custom CSS (Modern UI)
# ===============================
st.markdown("""
<style>
body {
    background-color: #f3f4f6;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    padding: 45px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.upload-box, .result-box {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.stButton > button {
    background: linear-gradient(135deg,#2563eb,#1e40af);
    color: white;
    border-radius: 14px;
    padding: 12px 28px;
    font-size: 16px;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

.result-box {
    animation: fadeIn 0.8s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 4. Hero Section
# ===============================
st.markdown("""
<div class="hero">
    <h1 style="font-size:48px;">⚖️ LegalEase</h1>
    <h3>Understand T&C in your own language</h3>
    <p style="font-size:16px;opacity:0.9;">
        Legal contracts, explained like you're 10.
    </p>
</div>
""", unsafe_allow_html=True)

# ===============================
# 5. Sidebar (Clean & Professional)
# ===============================
with st.sidebar:
    st.markdown("## ⚖️ LegalEase")
    st.caption("AI-powered legal simplification")

    target_language = st.selectbox(
        "🌐 Choose Language",
        ["English", "Hindi", "Bhojpuri", "Bengali", "Telugu"]
    )

    st.markdown("---")
    st.success("✔ 5th-grade reading level")
    st.info("✔ Multilingual support")
    st.warning("✔ Highlights risks & dates")

reading_level = "5th Grade Student"

# ===============================
# 6. Main Layout (Two Columns)
# ===============================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Legal Agreement")
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload image or text file",
        type=["png", "jpg", "jpeg", "txt"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    - Upload any legal agreement  
    - AI simplifies the content  
    - Key dates & risks highlighted  
    - Output in your chosen language  
    """)

content_to_process = None

if uploaded_file:
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_container_width=True)
        content_to_process = image
    else:
        content_to_process = uploaded_file.read().decode("utf-8")

# ===============================
# 7. Action Button & AI Logic
# ===============================
if content_to_process and st.button("✨ Simplify Agreement"):
    with st.spinner("🔍 Analyzing legal document..."):
        prompt = f"""
        Act as a legal expert who specializes in Access to Justice.

        Analyze the provided legal document and respond in {target_language}.

        1. SUMMARY:
        Explain the main purpose of this agreement like I am a {reading_level}.

        2. KEY DATES:
        List important deadlines, renewal dates, or payment dates (if any).

        3. RED FLAGS:
        Point out risky clauses or anything that may reduce my rights.

        4. ACTION ITEMS:
        Clearly tell me what I should do next.

        Keep the language very simple, friendly, and easy to understand.
        """

        response = model.generate_content([prompt, content_to_process])

        st.divider()
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"### 📝 Simplified Explanation ({target_language})")
        st.write(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
