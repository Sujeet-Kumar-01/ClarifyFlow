import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ------------------ Gemini Setup ------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="ClarifyFlow",
    page_icon="📄",
    layout="centered"
)

# ------------------ Custom CSS (Light Modern UI) ------------------
st.markdown("""
<style>
    .main {
        background-color: #f9fafb;
    }
    .block-container {
        padding-top: 2rem;
    }
    .title-text {
        font-size: 2.3rem;
        font-weight: 700;
        color: #111827;
    }
    .subtitle-text {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.markdown('<div class="title-text">📘 Understand T&C in your own language</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Translate complex agreements into simple, 5th-grade level summaries.</div>',
    unsafe_allow_html=True
)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.header("⚙️ Settings")
    target_language = st.selectbox(
        "Choose Output Language",
        ["English", "Hindi", "Bhojpuri", "Bengali", "Telugu"]
    )
    reading_level = "5th Grade Student"

# ------------------ Upload Section ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload a Contract (Image or Text)",
    type=["png", "jpg", "jpeg", "txt"]
)
st.markdown('</div>', unsafe_allow_html=True)

content_to_process = None

if uploaded_file:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Contract", use_container_width=True)
        content_to_process = image
    else:
        content_to_process = uploaded_file.read().decode("utf-8")
        st.success("📄 Text document uploaded successfully")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Action Button ------------------
if content_to_process and st.button("✨ Simplify Now"):
    with st.spinner("Decoding legal language..."):
        prompt = f"""
        You are a legal expert working on Access to Justice.
        Read the document and respond in {target_language}.

        Provide:
        1. SUMMARY – Explain simply like to a {reading_level}
        2. KEY DATES – Any deadlines or expiry dates
        3. RED FLAGS – Risky or unfair clauses
        4. ACTION ITEMS – What the user should do next

        Keep language extremely simple and clear.
        """

        response = model.generate_content([prompt, content_to_process])

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### ✅ Simplified Explanation ({target_language})")
        st.write(response.text)
        st.markdown('</div>', unsafe_allow_html=True)
