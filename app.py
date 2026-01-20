import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Setup Gemini
# Replace 'YOUR_API_KEY' with the key you got from AI Studio
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

# 2. UI Configuration
st.set_page_config(page_title="ClarifyFlow", page_icon="⚖️")
st.title("⚖️ ClarifyFlow: Legalese to Plain Language")
st.subheader("Translate complex contracts into simple, 5th-grade level summaries.")

# 3. Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    target_language = st.selectbox("Select Language", ["English", "Hindi", "Bhojpuri", "Spanish", "French"])
    reading_level = "5th Grade Student"

# 4. File Upload
uploaded_file = st.file_uploader("Upload a Contract (Image or Text)", type=['png', 'jpg', 'jpeg', 'txt'])

if uploaded_file is not None:
    # Display the uploaded document
    if uploaded_file.type.startswith('image'):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Contract", use_container_width=True)
        content_to_process = image
    else:
        content_to_process = uploaded_file.read().decode("utf-8")

    if st.button("Simplify Now"):
        with st.spinner("Decoding legalese..."):
            # The Magic Prompt
            prompt = f"""
            Act as a legal expert who specializes in Access to Justice. 
            Analyze the provided legal document and provide the following in {target_language}:
            
            1. SUMMARY: Explain the main purpose of this document like I am a {reading_level}.
            2. KEY DATES: List any deadlines, expiration dates, or payment dates.
            3. RED FLAGS: Highlight any sections that might be risky or take away my rights.
            4. ACTION ITEMS: What should I do next?
            
            Keep the tone helpful and very simple.
            """
            
            # Call Gemini
            response = model.generate_content([prompt, content_to_process])
            
            st.divider()
            st.markdown(f"### Simplified Summary ({target_language})")
            st.write(response.text)

