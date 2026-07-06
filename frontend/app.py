import streamlit as st
import os
import requests

# Setup Streamlit page
st.set_page_config(page_title="LearnSync - AI Study Concierge", page_icon="📚", layout="wide")

# Inject Custom CSS for Modern UI
st.markdown("""
<style>
    /* Hide Streamlit default UI elements for a cleaner SaaS look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Gradient Title */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-top: 5px;
        margin-bottom: 40px;
    }
    
    /* Smooth Button Enhancements */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        background: linear-gradient(90deg, #4ECDC4, #556270);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(78, 205, 196, 0.3);
        border: none;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

import base64

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

logo_base64 = get_base64_of_bin_file(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))

# Hero Section
if logo_base64:
    st.markdown(f'''
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 5px; padding-top: 10px;">
        <img src="data:image/png;base64,{logo_base64}" style="width: 85px; height: 85px; border-radius: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <h1 class="hero-title" style="margin-bottom: 0px;">LearnSync</h1>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<h1 class="hero-title">📚 LearnSync</h1>', unsafe_allow_html=True)

st.markdown('<p class="hero-subtitle">Your personal AI Study Concierge. Upload a PDF and magically generate summaries & active recall quizzes.</p>', unsafe_allow_html=True)

# Sidebar for API Key configuration
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("Google API Key", type="password", help="Enter your Gemini API Key from Google AI Studio")
    st.markdown("---")
    st.markdown("🔒 *LearnSync operates strictly via secure API. Your key is never stored.*")
    
# Define Backend URL directly (hidden from UI)
backend_url = os.getenv("BACKEND_URL", "https://esprydi-learnsync-backend.hf.space")

# Main area layout (Top-to-Bottom)
st.markdown('### 📄 Document Upload')
uploaded_file = st.file_uploader("Drop your Study Material here (PDF)", type=["pdf"], help="Maximum file size is 15 MB")
st.caption("⚠️ Maximum file size: **15 MB**")

if uploaded_file is not None:
    if not api_key:
        st.warning("⚠️ Please provide your Google API Key in the sidebar.")
    else:
        if st.button("🚀 Start Learning Process"):
            st.session_state['start_processing'] = True

if 'start_processing' in st.session_state and st.session_state['start_processing']:
    st.markdown("---")
    st.markdown("### 🧠 AI Analysis")
    with st.spinner("✨ Agents are extracting knowledge and crafting your quiz..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            headers = {"X-Google-API-Key": api_key}
            response = requests.post(
                f"{backend_url.rstrip('/')}/analyze-pdf", 
                files=files, 
                headers=headers, 
                timeout=600
            )
            
            if response.status_code == 200:
                st.success("✅ Analysis Complete!")
                result_data = response.json()
                
                st.markdown("---")
                st.markdown(result_data.get("result", "No results returned."))
            else:
                st.error(f"❌ Failed to process document. Status Code: {response.status_code}")
                try:
                    error_detail = response.json().get("detail", response.text)
                    st.error(error_detail)
                except:
                    st.error(response.text)
                
        except requests.exceptions.RequestException:
            st.error("🔌 An error occurred while connecting to the backend server.")
            st.info("Make sure the AI backend is deployed and running.")
    
    # Reset state after processing
    st.session_state['start_processing'] = False
