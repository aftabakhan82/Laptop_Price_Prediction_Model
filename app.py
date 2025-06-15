import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

st.set_page_config(page_title="Laptop Price Prediction", page_icon="💻", layout="centered")

st.title("💻 Laptop Price Prediction")
st.markdown("### Select Features to Predict Laptop Price")

ram = st.selectbox("RAM (GB)", [2, 4, 8, 16, 32, 64], index=2)
weight = st.selectbox("Weight (kg)", [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0], index=2)
memory = st.selectbox("Memory (GB)", [128, 256, 512, 1024, 1500, 2000], index=2)

selected_model = st.selectbox("Choose a Model", ["Linear Regression", "Decision Tree", "Random Forest", "Support Vector", "KNN","XGBoost Regression"])

test_data = np.array([[ram, weight, memory]])

if st.button("🔍 Predict Price"):
    model_file_mapping = {
        "Linear Regression": "model/Linear_model.pkl",
        "Decision Tree": "model/Decision_tree_model.pkl",
        "Random Forest": "model/Random_forest_model.pkl",
        "Support Vector": "model/Support_vector_md.pkl",
        "KNN": "model/Knn_Model.pkl",
        "XGBoost Regression":"model/XGBR_Model.pkl"
    }

    model = joblib.load(model_file_mapping[selected_model])
    prediction = model.predict(test_data)
    
    st.write(f"## 💰 Predicted Price: ₹{prediction[0]:.2f}")

    try:
        y_test = joblib.load("model/y_test.pkl")
        X_test = joblib.load("model/X_test.pkl")
        r2 = r2_score(y_test, model.predict(X_test))
        st.write(f"### 📊 Model Performance (R² Score): {r2:.4f}")
    except FileNotFoundError:
        st.write("⚠️ R² Score unavailable (test data not found)")

    fig, ax = plt.subplots(figsize=(10, 5))
    models = list(model_file_mapping.keys())
    predictions = [joblib.load(model_file_mapping[m]).predict(test_data)[0] for m in models]

    ax.bar(models, predictions, color="skyblue")
    ax.axhline(prediction[0], color="red", linestyle="--", label=f"{selected_model}: ₹{prediction[0]:.2f}")
    ax.set_ylabel("Predicted Price")
    ax.set_title("Price Predictions Across Models")
    ax.legend()

    st.pyplot(fig)