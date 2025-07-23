from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from joblib import load
import numpy as np
import pandas as pd
import MySQLdb.cursors

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500"])

# ------------------ MODEL LOADING ------------------
model = load("./models/voting_classifier.joblib")
scaler = load("./models/scaler.joblib")

feature_names = [
    "Heart Rate", "Respiratory Rate", "Body Temperature", "Oxygen Saturation",
    "Age", "Gender", "Derived_HRV", "Derived_Pulse_Pressure", "Derived_BMI", "Derived_MAP"
]

# ------------------ DATABASE CONFIG ------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # 🔁 Change to your MySQL username
app.config['MYSQL_PASSWORD'] = '8840'  # 🔁 Change to your MySQL password
app.config['MYSQL_DB'] = 'medxtech'  # 🔁 Ensure this DB exists in MySQL

mysql = MySQL(app)
bcrypt = Bcrypt(app)


# ------------------ ML PREDICTION ROUTE ------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data.get("features")

        if not features or len(features) != len(feature_names):
            return jsonify({"error": "Invalid input. Ensure all required fields are provided."}), 400

        input_df = pd.DataFrame([features], columns=feature_names)
        scaled_features = scaler.transform(input_df)
        prediction = model.predict(scaled_features)
        risk_category = "Healthy" if prediction[0] == 0 else "Unhealthy"

        return jsonify({"risk_category": risk_category})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ SIGNUP ROUTE ------------------
@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.form
    fname = data.get('fname')
    lname = data.get('lname')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('pass')
    cpass = data.get('cpass')

    if password != cpass:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')
    hashed_confirm_pass = bcrypt.generate_password_hash(cpass).decode('utf-8')
    image = request.files['image'].read()

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO patients (fname, lname, email, phone, password, confirm_password, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (fname, lname, email, phone, hashed_pass, hashed_confirm_pass, image))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Signup successful'})
    except  Exception as e:
        print("ERROR:", e)
        return jsonify({'error': 'Some error Occured'}), 500

# ------------------ LOGIN ROUTE -----------------
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM patients WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'user': user['fname']})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# ------------------ MAIN ------------------
if __name__ == '__main__':
    app.run(debug=True)