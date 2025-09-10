
# 🏥 Intelligent Disease Predictor: Modern Medicine meets TCM

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

A revolutionary healthcare application that bridges evidence-based modern medicine with holistic Traditional Chinese Medicine (TCM) principles. This AI-powered platform provides comprehensive health insights by combining machine learning disease prediction with ancient wellness wisdom.

![HealthBot Demo](https://via.placeholder.com/800x400?text=HealthBot+Modern+Medicine+%2B+TCM+Interface)

## ✨ Features

### 🧪 Modern Medicine Module
- **AI-Powered Diagnosis**: Support Vector Classifier (SVC) trained on comprehensive medical data
- **Symptom Analysis**: Processes 131+ symptoms to predict 41 different diseases
- **Evidence-Based Recommendations**: 
  - Medication guidance
  - Dietary recommendations
  - Exercise routines
  - Medical precautions
- **Comprehensive Data**: Integrated datasets for complete healthcare information

### 🌿 Traditional Chinese Medicine Module
- **Pattern Diagnosis**: Identifies TCM patterns (Qi deficiency, Yin/Yang imbalance, etc.)
- **Holistic Recommendations**:
  - Herbal medicine suggestions
  - Acupressure/acupuncture points
  - TCM dietary principles
  - Lifestyle adjustments
- **DeepSeek API Integration**: AI-powered TCM insights with fallback system

### 🎯 Unified Interface
- **Dual-Perspective Navigation**: Switch between modern and traditional medicine views
- **User-Friendly Design**: Streamlit-based responsive interface
- **Educational Content**: Learn about both medical paradigms
- **Comprehensive Results**: Detailed treatment plans from both perspectives

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/Intelligent_Disease_Predictor.git
cd Intelligent_Disease_Predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys** (optional for full TCM functionality)
```bash
# Create secrets file
mkdir -p .streamlit
echo "DEEPSEEK_API_KEY = 'your_api_key_here'" > .streamlit/secrets.toml
```

4. **Run the application**
```bash
streamlit run main.py
```

## 📁 Project Structure

```
Intelligent_Disease_Predictor/
├── main.py                 # Main application file
├── tcm.py                  # Traditional Chinese Medicine module
├── modern_medicine.py      # Modern medicine module
├── models/
│   └── supprtVectorC.pkl   # Trained SVC model
├── datasets/
│   ├── Training.csv        # Primary training data
│   ├── symtoms_df.csv      # Symptoms descriptions
│   ├── precautions_df.csv  # Precaution data
│   ├── workout_df.csv      # Exercise recommendations
│   ├── description.csv     # Disease descriptions
│   ├── medications.csv     # Medication information
│   └── diets.csv           # Dietary recommendations
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: scikit-learn, pandas, numpy
- **AI Integration**: DeepSeek API
- **Data Storage**: CSV datasets
- **Model Serialization**: pickle

## 📊 Model Performance

The Support Vector Classifier (SVC) was selected after comprehensive evaluation against multiple algorithms:
- Support Vector Classifier (SVC) - **Selected (Best Performance)**
- Random Forest Classifier
- Gradient Boosting Classifier
- K-Neighbors Classifier
- Multinomial Naive Bayes

## 🌟 Unique Value Proposition

This project stands out by:
- **Bridging Medical Paradigms**: First platform to seamlessly integrate modern medicine with TCM
- **Comprehensive Care**: From diagnosis to treatment across both systems
- **Educational Approach**: Teaches users about different medical philosophies
- **Robust Architecture**: Fallback systems ensure reliability
- **Accessible Healthcare**: Makes complex medical information understandable

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, open issues, or suggest new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with questions about medical conditions.

## 📞 Support

For support, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team

---

**Built with ❤️ for better healthcare integration**
