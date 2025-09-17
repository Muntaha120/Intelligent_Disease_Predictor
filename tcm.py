import streamlit as st
import requests
import json
import time
from groq import Groq
from streamlit_lottie import st_lottie
import os


# --- Load Lottie Animation ---
# You can find free animations at lottiefiles.com
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Example: A soothing animation for a wellness app
LOTTIE_URL = "https://lottie.host/17498c0b-1937-4d6d-8947-a89c36293f0b/Yw7J1R7f9A.json"
lottie_animation = load_lottieurl(LOTTIE_URL)

# --- Custom CSS for this page ---
st.markdown("""
<style>
    /* General body styling for a consistent aesthetic */
    .stApp {
        background-color: #f0f2f6; /* Light grey background for readability */
    }

    /* Main container and content styling */
    .tcm-container {
        max-width: 900px;
        margin: auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    /* Header styling */
    h1 {
        text-align: center;
        color: #006400; /* Dark Green */
        font-weight: 700;
        letter-spacing: 1px;
    }

    h2 {
        color: #006400; /* Dark Green */
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
    }

    /* Disclaimer Box */
    .tcm-disclaimer {
        background-color: #f0fff0; /* Honeydew */
        border-left: 5px solid #3CB371; /* Medium Sea Green */
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
        font-style: italic;
    }

    /* User Input Section */
    .symptom-input-container {
        background-color: #e8f5e9; /* Lighter green */
        padding: 20px;
        border-radius: 12px;
        margin-top: 25px;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        font-weight: bold;
        padding: 12px;
        border-radius: 12px;
        border: none;
        background-color: #4CAF50; /* Green */
        color: white;
        font-size: 1.1em;
        transition: transform 0.2s, background-color 0.2s;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }

    /* Output Styling */
    .analysis-section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
    }

    .analysis-section h3 {
        color: #388e3c; /* Darker Green */
        margin-top: 0;
    }

</style>
""", unsafe_allow_html=True)


# --- Function to get TCM analysis from Groq API ---
def get_tcm_analysis_groq(symptoms_list, api_key):
    """Get TCM analysis from Groq API"""
    if not api_key:
        return "API key not configured."

    client = Groq(api_key=api_key)
    symptoms_str = ", ".join(symptoms_list)

    # A more detailed and structured prompt
    prompt = f"""You are an expert Traditional Chinese Medicine (TCM) practitioner. Your task is to provide a detailed and structured TCM analysis based on the following symptoms: {symptoms_str}.

Please format your response clearly with headings for each section.
The sections should include:

1.  **TCM Diagnosis (Pattern Identification)**: Identify the underlying TCM pattern (e.g., Qi Stagnation, Blood Deficiency, Liver Yin Deficiency, etc.).
2.  **Physical Meaning**: Explain what this pattern means in simple, clear terms (e.g., "This means your body's energy flow is blocked").
3.  **Dietary Recommendations**: Provide specific food and dietary advice to address the identified pattern.
4.  **Herbal Medicine Suggestions**: Suggest common TCM herbal formulas that are traditionally used for this pattern. State that these should be used under professional guidance.
5.  **Acupressure Insights**: Recommend 1-3 specific acupressure points to massage and explain their benefits.
6.  **Lifestyle Advice**: Offer practical lifestyle suggestions (e.g., exercise, sleep, stress management) to support healing.
7.  **Disclaimer**: A final, clear statement that this is for informational purposes and not a substitute for professional medical advice."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Groq's most suitable model for this task
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the Groq API: {e}")
        return None


# --- Streamlit UI for the TCM page ---
def show_tcm_interface():
    st.title("🌿 Traditional Chinese Medicine Insights")
    st.markdown("This page provides a Traditional Chinese Medicine (TCM) analysis based on your symptoms.")
    st.markdown(
        '<div class="tcm-disclaimer">⚠️ <b>Disclaimer:</b> This is for informational purposes only. Consult a licensed TCM practitioner for a proper diagnosis and treatment.</div>',
        unsafe_allow_html=True
    )

    # Get API key from secrets
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API key not configured. Please add it to your `.streamlit/secrets.toml` file.")
        return

    # User input section with improved aesthetics
    st.markdown('<div class="symptom-input-container">', unsafe_allow_html=True)
    symptoms_input_tcm = st.text_input(
        "Enter your symptoms (comma-separated):",
        placeholder="e.g., fatigue, headache, digestive issues"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Get TCM Analysis", type="primary"):
        if symptoms_input_tcm.strip():
            user_symptoms = [s.strip().lower() for s in symptoms_input_tcm.split(',')]

            # Show Lottie animation while processing
            with st.spinner("Analyzing symptoms with the wisdom of TCM..."):
                if lottie_animation:
                    st_lottie(lottie_animation, height=200, key="tcm_lottie")

                tcm_analysis = get_tcm_analysis_groq(user_symptoms, api_key)

            # Display results
            if tcm_analysis:
                st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
                st.markdown(tcm_analysis, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("Please enter symptoms to get a TCM analysis.")


# Run the function to display the interface
show_tcm_interface()
