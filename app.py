import streamlit as st
import pandas as pd
import joblib

# -------------------------
# Configuración de la página
# -------------------------
st.set_page_config(
    page_title="Predicción de Riesgo de Diabetes",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Sistema de Predicción Temprana de Riesgo de Diabetes")
st.write("Complete la información del paciente y presione **Predecir**.")

# -------------------------
# Cargar modelo
# -------------------------
modelo = joblib.load("modelo_rf_final.pkl")

st.header("Datos del paciente")

col1, col2 = st.columns(2)

with col1:
    Edad = st.number_input("Edad", 1, 120, 30)
    Genero = st.selectbox("Género", ["Femenino", "Masculino"])
    Poliuria = st.selectbox("Poliuria", ["No", "Sí"])
    Polidipsia = st.selectbox("Polidipsia", ["No", "Sí"])
    Perdida_repentina_peso = st.selectbox("Pérdida repentina de peso", ["No", "Sí"])
    Debilidad = st.selectbox("Debilidad", ["No", "Sí"])
    Polifagia = st.selectbox("Polifagia", ["No", "Sí"])
    Candidiasis_genital = st.selectbox("Candidiasis genital", ["No", "Sí"])

with col2:
    Vision_borrosa = st.selectbox("Visión borrosa", ["No", "Sí"])
    Picazon = st.selectbox("Picazón", ["No", "Sí"])
    Irritabilidad = st.selectbox("Irritabilidad", ["No", "Sí"])
    Cicatrizacion_lenta = st.selectbox("Cicatrización lenta", ["No", "Sí"])
    Paresia_parcial = st.selectbox("Paresia parcial", ["No", "Sí"])
    Rigidez_muscular = st.selectbox("Rigidez muscular", ["No", "Sí"])
    Alopecia = st.selectbox("Alopecia", ["No", "Sí"])
    Obesidad = st.selectbox("Obesidad", ["No", "Sí"])
