import streamlit as st
import numpy as np
import pandas as pd
import pickle

# --- Configuration and Custom CSS ---
# Set the page configuration first
st.set_page_config(
    page_title="HealthBot - Modern Medicine & TCM",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gradient background CSS
page_bg_css = """
<style>
.stApp {
  background-image: linear-gradient(to right, #e6e6fa, #add8e6); /* Lavender and Blue */
  background-size: cover;
  background-attachment: fixed;
}

/* Custom styles for better aesthetics */
h1 {
    color: #4B0082;
    text-align: center;
    font-weight: 800;
}

h2 {
    color: #4B0082;
    font-weight: 600;
}

.stButton>button {
    background-color: #9370DB;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 1.1em;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease-in-out;
}

.stButton>button:hover {
    background-color: #8A2BE2;
    transform: scale(1.05);
}

.stTextInput>div>div>input {
    border-radius: 12px;
    border: 1px solid #9370DB;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.stExpander {
    border-radius: 12px;
    background-color: rgba(255, 255, 255, 0.7);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.sidebar .sidebar-content {
    background-image: linear-gradient(to bottom, #e6e6fa, #add8e6);
}

.nav-item {
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
    transition: all 0.3s;
}

.nav-item:hover {
    background-color: rgba(147, 112, 219, 0.2);
}

.nav-item.active {
    background-color: #9370DB;
    color: white;
}

</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# Import your modules
try:
    from tcm import show_tcm_interface

    tcm_available = True
except ImportError:
    tcm_available = False
    st.sidebar.warning("TCM module not available")


# Load datasets and model
@st.cache_data
def load_data():
    return (
        pd.read_csv("datasets/symtoms_df.csv"),
        pd.read_csv("datasets/precautions_df.csv"),
        pd.read_csv("datasets/workout_df.csv"),
        pd.read_csv("datasets/description.csv"),
        pd.read_csv('datasets/medications.csv'),
        pd.read_csv("datasets/diets.csv")
    )


try:
    sym_des, precautions, workout, description, medications, diets = load_data()
    data_loaded = True
except FileNotFoundError:
    data_loaded = False
    st.error("Some data files are missing. Please check your datasets folder.")


@st.cache_resource
def load_model():
    return pickle.load(open('models/supprtVectorC.pkl', 'rb'))


try:
    svc = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False
    st.error("Model file not found. Please check your models folder.")


# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description'].iloc[0] if not \
        description[description['Disease'] == dis]['Description'].empty else "No description available."
    pre_data = precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = pre_data.values[0].tolist() if not pre_data.empty else []
    med = medications[medications['Disease'] == dis]['Medication'].tolist() if not \
        medications[medications['Disease'] == dis]['Medication'].empty else []
    die = diets[diets['Disease'] == dis]['Diet'].tolist() if not diets[diets['Disease'] == dis]['Diet'].empty else []
    wrkout = workout[workout['disease'] == dis]['workout'].tolist() if not workout[workout['disease'] == dis][
        'workout'].empty else []
    return desc, pre, med, die, wrkout


symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4,
                 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9,
                 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13,
                 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18,
                 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22,
                 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27,
                 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32,
                 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37,
                 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42,
                 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46,
                 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50,
                 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54,
                 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58,
                 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61,
                 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66,
                 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70,
                 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74,
                 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78,
                 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82,
                 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86,
                 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89,
                 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92,
                 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96,
                 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100,
                 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103,
                 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107,
                 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110,
                 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113,
                 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116,
                 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120,
                 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124,
                 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127,
                 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction',
                 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma',
                 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)',
                 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A',
                 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis',
                 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)',
                 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism',
                 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis',
                 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection',
                 35: 'Psoriasis', 27: 'Impetigo'}


def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1

    if np.sum(input_vector) == 0:
        return "No valid symptoms provided."

    if np.any(input_vector):
        prediction_index = svc.predict([input_vector])[0]
        # To debug the model's raw output, uncomment the line below:
        # st.info(f"DEBUG: Raw prediction index is {prediction_index}")

        if prediction_index in diseases_list:
            return diseases_list[prediction_index]
        else:
            return "Could not determine a specific disease."
    else:
        return "Not enough unique or recognized symptoms for a prediction."


def show_modern_medicine_interface():
    st.title("🏥 Modern Medicine Disease Predictor")
    st.markdown("""
        <p style='text-align: center; font-size: 1.2em; color: #555;'>
            Enter your symptoms separated by commas to get a possible diagnosis based on modern medicine.
        </p>
    """, unsafe_allow_html=True)

    # Input section
    st.markdown("---")
    st.subheader("Your Symptoms")
    symptoms_input = st.text_input(
        "List your symptoms (comma-separated):",
        key="symptoms_input",
        placeholder="e.g., headache, fever, muscle_pain"
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button("Get Prediction")
    st.markdown("---")

    if predict_button:
        if symptoms_input.strip() == "":
            st.warning("Please enter at least one symptom to get a prediction.")
        else:
            with st.spinner("Analyzing symptoms and predicting disease..."):
                user_symptoms = [s.strip().replace(" ", "_").lower() for s in symptoms_input.split(',')]
                valid_symptoms = [s for s in user_symptoms if s in symptoms_dict]
                invalid_symptoms = [s for s in user_symptoms if s not in symptoms_dict]

                if not valid_symptoms:
                    st.error("None of the entered symptoms were recognized. Please check your spelling and try again.")
                else:
                    predicted_disease = get_predicted_value(valid_symptoms)

                    if predicted_disease in diseases_list.values():
                        st.subheader(f"✨ Predicted Disease: **{predicted_disease}**")
                        dis_des, precautions_list, medications_list, rec_diet_list, workout_list = helper(
                            predicted_disease)

                        st.markdown("---")

                        with st.expander("📝 Disease Description"):
                            st.markdown(f"**Description:** {dis_des}")

                        with st.expander("🛡️ Precautions to Take"):
                            if precautions_list:
                                for i, pre in enumerate(precautions_list):
                                    if pre and pre != 'nan':
                                        st.markdown(f"- **{pre.capitalize()}**")
                            else:
                                st.write("No specific precautions found.")

                        with st.expander("💊 Recommended Medications"):
                            if medications_list:
                                for med in medications_list:
                                    st.markdown(f"- **{med.capitalize()}**")
                            else:
                                st.write("No specific medications found (consult a doctor).")

                        with st.expander("🥦 Recommended Diet"):
                            if rec_diet_list:
                                for diet in rec_diet_list:
                                    st.markdown(f"- **{diet.capitalize()}**")
                            else:
                                st.write("No specific diet recommendations found.")

                        with st.expander("🏋️‍♂️ Suggested Workouts"):
                            if workout_list:
                                for wrkout in workout_list:
                                    st.markdown(f"- **{wrkout.capitalize()}**")
                            else:
                                st.write("No specific workout recommendations found.")

                    else:
                        st.error(f"Could not make a confident prediction. {predicted_disease}")

                    if invalid_symptoms:
                        st.warning(
                            f"The following symptoms were not recognized: **{', '.join(invalid_symptoms)}**. They were not used in the prediction.")


# --- Navigation ---
st.sidebar.title("🌿 HealthBot Navigation")
st.sidebar.markdown("### Choose your approach:")

# Navigation options
nav_options = ["Modern Medicine", "Traditional Chinese Medicine"]
selected_nav = st.sidebar.radio("Select Approach", nav_options)

# Display the selected interface
if selected_nav == "Modern Medicine":
    show_modern_medicine_interface()
elif selected_nav == "Traditional Chinese Medicine" and tcm_available:
    show_tcm_interface()
elif selected_nav == "Traditional Chinese Medicine" and not tcm_available:
    st.error("TCM module is not available. Please check your tcm.py file.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**HealthBot** combines modern medical knowledge with traditional Chinese medicine 
to provide comprehensive health insights.
""")
