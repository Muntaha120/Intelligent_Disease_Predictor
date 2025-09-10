import streamlit as st
import requests
import json
import time

# --- Custom CSS for this page ---
st.markdown("""
<style>
.tcm-header {
    text-align: center;
    color: #006400; /* Dark Green */
}
.tcm-disclaimer {
    background-color: #f0fff0; /* Honeydew */
    border-left: 5px solid #3CB371; /* Medium Sea Green */
    padding: 10px;
    border-radius: 8px;
    margin-top: 20px;
}
.symptom-input {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}
.tcm-button {
    background-color: #4CAF50 !important;
    color: white !important;
}
.tcm-button:hover {
    background-color: #45a049 !important;
}
</style>
""", unsafe_allow_html=True)


# --- Function to get TCM analysis from Deepseek API ---
def get_tcm_analysis(symptoms_list, api_key):
    """Get TCM analysis from DeepSeek API"""
    if not api_key:
        return "API key not configured. Please check your configuration."

    # Try different possible endpoints for DeepSeek API
    endpoints = [
        "https://api.deepseek.com/v1/chat/completions",
        "https://api.deepseek.com/chat/completions"
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    symptoms_str = ", ".join(symptoms_list)

    # Improved prompt for better TCM responses
    prompt = f"""As a Traditional Chinese Medicine (TCM) practitioner, analyze these symptoms: {symptoms_str}.

Please provide:
1. TCM diagnosis (pattern identification like Qi deficiency, Yin/Yang imbalance, etc.)
2. Possible causes from a TCM perspective
3. Dietary recommendations
4. Herbal medicine suggestions (common formulas)
5. Acupressure/acupuncture points
6. Lifestyle advice

Format your response in clear sections with brief explanations."""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system",
             "content": "You are a knowledgeable Traditional Chinese Medicine practitioner with expertise in diagnosis and treatment."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    # Try each endpoint until one works
    for endpoint in endpoints:
        try:
            with st.spinner("Consulting ancient TCM wisdom..."):
                response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()
                return result['choices'][0]['message']['content']

        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.Timeout:
            st.error("Request timed out. The API is taking too long to respond.")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                st.error("Authentication failed. Please check your API key.")
            elif response.status_code == 404:
                continue  # Try next endpoint
            elif response.status_code == 429:
                st.error("Rate limit exceeded. Please try again later.")
            else:
                st.error(f"HTTP Error: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None

    # If all endpoints failed
    st.error("Could not connect to the DeepSeek API. Please check your internet connection or try again later.")
    return None


# --- Fallback TCM Responses ---
def get_fallback_tcm_response(symptoms):
    """Provide fallback responses if API is not working"""
    symptom_keywords = {
        "fatigue": "Qi Deficiency",
        "headache": "Liver Yang Rising",
        "insomnia": "Heart Yin Deficiency",
        "digestive": "Spleen Qi Deficiency",
        "anxiety": "Heart Fire or Liver Qi Stagnation",
        "pain": "Blood Stasis or Qi Stagnation",
        "cold": "Wei Qi Deficiency",
        "stress": "Liver Qi Stagnation"
    }

    # Find the most relevant pattern
    pattern = "Qi imbalance"
    for keyword, diagnosis in symptom_keywords.items():
        if keyword in " ".join(symptoms).lower():
            pattern = diagnosis
            break

    return f"""
**TCM Diagnosis:** {pattern}

**General Recommendations:**
- Maintain a balanced diet with seasonal foods
- Practice stress-reducing activities like meditation or Tai Chi
- Ensure adequate rest and regular sleep patterns
- Consider consulting a licensed TCM practitioner for personalized advice

*Note: This is a general response as the AI service is currently unavailable. For a personalized analysis, please check your API configuration.*
"""


# --- Streamlit UI for the TCM page ---
def show_tcm_interface():
    st.title("🌿 Traditional Chinese Medicine Insights")
    st.markdown("This page provides a Traditional Chinese Medicine (TCM) analysis based on your symptoms.")
    st.markdown(
        '<div class="tcm-disclaimer">⚠️ <b>Disclaimer:</b> This is for informational purposes only. Consult a licensed TCM practitioner for a proper diagnosis and treatment.</div>',
        unsafe_allow_html=True
    )

    # Try to get API key from secrets
    try:
        DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
        api_key_available = True
    except:
        DEEPSEEK_API_KEY = None
        api_key_available = False
        st.warning("DeepSeek API key not found in secrets. Using fallback mode.")

    # Option to input API key manually
    if not api_key_available:
        DEEPSEEK_API_KEY = st.text_input("Enter your DeepSeek API Key (optional):", type="password")
        if DEEPSEEK_API_KEY:
            api_key_available = True
            st.success("API key entered successfully")

    # User input
    st.markdown('<div class="symptom-input">', unsafe_allow_html=True)
    symptoms_input_tcm = st.text_input(
        "Enter your symptoms (comma-separated):",
        placeholder="e.g., fatigue, headache, digestive issues"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Get TCM Analysis", type="primary"):
        if symptoms_input_tcm.strip():
            user_symptoms = [s.strip().lower() for s in symptoms_input_tcm.split(',')]

            # Try to get analysis from API
            tcm_analysis = None
            if api_key_available:
                tcm_analysis = get_tcm_analysis(user_symptoms, DEEPSEEK_API_KEY)

            # If API failed or no API key, use fallback
            if not tcm_analysis:
                tcm_analysis = get_fallback_tcm_response(user_symptoms)
                st.info("Using fallback TCM analysis. For full functionality, please configure your DeepSeek API key.")

            # Display results
            st.markdown("---")
            st.subheader("TCM Analysis")
            st.info(tcm_analysis)
        else:
            st.error("Please enter symptoms to get a TCM analysis.")


# If this file is run directly
if __name__ == "__main__":
    show_tcm_interface()