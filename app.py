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
# 3. Custom CSS for Modern UI
# ===============================
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #1f2937;
    text-align: center;
}
h3 {
    text-align: center;
    color: #374151;
}
.upload-box {
    border: 2px dashed #9ca3af;
    padding: 30px;
    border-radius: 12px;
    background-color: #ffffff;
}
.result-box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 4. Header Section
# ===============================
st.markdown("<h1>⚖️ LegalEase</h1>", unsafe_allow_html=True)
st.markdown("<h3>Understand T&C in your own language</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#6b7280;'>Translate complex agreements into simple, 5th-grade level summaries.</p>",
    unsafe_allow_html=True
)

st.divider()

# ===============================
# 5. Sidebar Settings
# ===============================
with st.sidebar:
    st.header("⚙️ Settings")
    target_language = st.selectbox(
        "Choose Language",
        ["English", "Hindi", "Bhojpuri", "Bengali", "Telugu"]
    )
    reading_level = "5th Grade Student"
    st.info("📄 Upload a legal agreement to simplify it instantly.")

# ===============================
# 6. File Upload Section
# ===============================
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload a Contract (Image or Text)",
    type=["png", "jpg", "jpeg", "txt"]
)
st.markdown("</div>", unsafe_allow_html=True)

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
