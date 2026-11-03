# MedXTech: Hospital Management Website with Health Risk Prediction

MedXTech is a hospital management website with separate interfaces for doctors and patients, plus a machine learning model that predicts a user's health risk category from physiological readings. Built as a two-person academic project.

## Features
- Web interface with patient and doctor login, registration, and a health-risk prediction page
- Patients can book consultation appointments and update their symptoms and conditions
- Specialty pages (cardiology, neurology, orthopedics, skin, gynecology, psychology)
- Health risk prediction page powered by a soft-voting ensemble of four scikit-learn classifiers (Gaussian Naive Bayes, Decision Tree, Logistic Regression, SVC)
- Flask backend that loads the saved model and scaler and returns predictions

## Screenshots
See [UI/README.md](UI/README.md) for screenshots of the interface.

## Future scope
- Encrypted transactions using blockchain technology
- Collaboration with labs, pharmacies and hospitals
- Chatbots for round-the-clock user support

## Results
| Metric | Result |
|---|---:|
| Test accuracy | **85%** |
| ROC-AUC | **0.86** |

The model was trained and evaluated in Google Colab. The trained model and its feature scaler were saved with joblib and are included in this repo.

## Tech stack
Python, Flask, scikit-learn, pandas, NumPy, HTML, CSS, JavaScript, joblib, Google Colab

## Project structure
```text
Health-prediction/
├── FlaskProject1/
│   ├── main.py                       # Flask backend
│   ├── requirements.txt
│   └── models/
│       ├── voting_classifier.joblib  # trained ensemble model
│       └── scaler.joblib             # feature scaler
└── UI/
    ├── index.html, machineLearningAlgo.html, booknow.html, ...
    ├── Patient_Login.html, Doctor_login.html, Registration.html, ...
    ├── css/, js/, image/
    └── README.md
```

## How to run
1. Clone the repo and open the `FlaskProject1` folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the backend: `python main.py`
4. Open the local address shown in the terminal in your browser.

## Team contributions
- **Vanshika Verma** ([@UncoolW](https://github.com/UncoolW)): trained and evaluated the machine learning model, and saved the trained model and scaler with joblib for use in the app.
- **Yatin Singh** ([@Yatin8840](https://github.com/Yatin8840)): Flask backend, web interface, and integration of the model into the application.

## Disclaimer
This is an academic project for learning and demonstration. It is not clinically validated and must not be used for medical diagnosis or treatment.
