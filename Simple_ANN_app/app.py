import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import tensorflow as tf
import pickle
import streamlit as st

## Loading the trained model
model = tf.keras.models.load_model("model.h5")

## loading the encoders and scalers
with open("label_encoder_gender.pkl", "rb") as file:
    label_encoder_gender = pickle.load(file)

with open("one_hot_encoder_gro.pkl", "rb") as file:
    one_hot_encoder_geo = pickle.load(file)

with open("standard_scaler.pkl", "rb") as file:
    stand_scaler = pickle.load(file)

### Streamlit app
st.title("Customer Churn prediction")

## user input
geography = st.selectbox("Geography", one_hot_encoder_geo.categories_[0])
gender = st.selectbox("Gender", label_encoder_gender.classes_)
age = st.slider("Age", 18, 92)
balance = st.number_input("Balance")
credit_score = st.number_input("credit_score")
estimated_salary = st.number_input("Estimated Salary")
tenure = st.slider("Tenure", 0, 10)
num_of_products = st.slider("Number of Products", 1, 4)
has_cr_card = st.selectbox("Has Credit Card", [0,1])
is_active_number = st.selectbox("Is Active Member", [0,1])

## Prepare the input_data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]], 
    'Age': [age], 
    'Tenure': [tenure], 
    'Balance': [balance], 
    'NumOfProducts': [num_of_products], 
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_number], 
    'EstimatedSalary': [estimated_salary]
})

## One-hot encode "Geography"
geo_encoded = one_hot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns = one_hot_encoder_geo.get_feature_names_out(["Geography"]))

## combine one hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop = True), geo_encoded_df], axis = 1)

## Scale the input data
input_data_scaled = stand_scaler.transform(input_data)

## prediction churn
prediction = model.predict(input_data_scaled)
prediction_prob = prediction[0][0]
st.write(f"Churn probalility: {prediction_prob:.2f}")

if prediction_prob > 0.5:
    st.write("The Customer is likely to churn.")
else:
    st.write("The Customer is not likely to churn.")

