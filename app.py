from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load your trained model and feature extraction instance using joblib
model = joblib.load("spam_classifier.pkl")
feature_extraction = joblib.load("feature_extraction.pkl")

def clean_email(text):
    # Replace this with your actual data cleaning logic
    text = text.lower()
    # Additional cleaning steps if needed
    return text

def predict(text):
    processed_text = clean_email(text)
    input_data_features = feature_extraction.transform([processed_text])
    prediction = model.predict(input_data_features)[0]
    return prediction

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
def predict_email():
    text = request.form["email_content"]

    prediction = predict(text)

    prediction_probability = round(prediction * 100, 2) if prediction == 0 else "0"
    prediction_label = "Not Spam" if prediction == 1 else "Spam"

    return render_template("predict.html", prediction_probability=prediction_probability, prediction_label=prediction_label)

if __name__ == "__main__":
    app.run(debug=True)
