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

# -------------------------
# Convertir respuestas a 0 y 1
# -------------------------

def convertir(valor):
    return 1 if valor == "Sí" else 0

genero = 1 if Genero == "Masculino" else 0

datos = pd.DataFrame([{
    "Edad": Edad,
    "Genero": genero,
    "Poliuria": convertir(Poliuria),
    "Polidipsia": convertir(Polidipsia),
    "Perdida_repentina_peso": convertir(Perdida_repentina_peso),
    "Debilidad": convertir(Debilidad),
    "Polifagia": convertir(Polifagia),
    "Candidiasis_genital": convertir(Candidiasis_genital),
    "Vision_borrosa": convertir(Vision_borrosa),
    "Picazon": convertir(Picazon),
    "Irritabilidad": convertir(Irritabilidad),
    "Cicatrizacion_lenta": convertir(Cicatrizacion_lenta),
    "Paresia_parcial": convertir(Paresia_parcial),
    "Rigidez_muscular": convertir(Rigidez_muscular),
    "Alopecia": convertir(Alopecia),
    "Obesidad": convertir(Obesidad)
}])

def generar_pdf(datos, prediccion, probabilidad):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("<b>REPORTE DE PREDICCIÓN DE RIESGO DE DIABETES</b>", estilos["Title"]))
    elementos.append(Paragraph("<br/>", estilos["Normal"]))

    if prediccion == 1:
        resultado = "ALTO RIESGO DE DIABETES"
    else:
        resultado = "BAJO RIESGO DE DIABETES"

    elementos.append(Paragraph(f"<b>Resultado:</b> {resultado}", estilos["Normal"]))
    elementos.append(Paragraph(f"<b>Probabilidad:</b> {probabilidad*100:.2f}%", estilos["Normal"]))
    elementos.append(Paragraph("<br/>", estilos["Normal"]))

    elementos.append(Paragraph("<b>Datos del paciente</b>", estilos["Heading2"]))

    for columna in datos.columns:
        elementos.append(
            Paragraph(f"{columna}: {datos.iloc[0][columna]}", estilos["Normal"])
        )

    doc.build(elementos)

    buffer.seek(0)
    return buffer
# -------------------------
# Botón de predicción
# -------------------------

if st.button("🔍 Predecir riesgo de diabetes", use_container_width=True):

    prediccion = modelo.predict(datos)[0]
    probabilidad = modelo.predict_proba(datos)[0][1]

    st.divider()

    st.subheader("📊 Resultado")

    if prediccion == 1:
        st.error("⚠️ El paciente presenta ALTO RIESGO de diabetes.")
    else:
        st.success("✅ El paciente presenta BAJO RIESGO de diabetes.")

    st.metric(
        label="Probabilidad estimada",
        value=f"{probabilidad*100:.2f}%"
    )

    st.progress(float(probabilidad))

    st.subheader("📋 Datos evaluados")
    st.dataframe(datos, use_container_width=True)

    # ---- PDF ----
    pdf = generar_pdf(datos, prediccion, probabilidad)

    st.download_button(
        "📄 Descargar reporte PDF",
        pdf,
        file_name="Reporte_Diabetes.pdf",
        mime="application/pdf"
    )

from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
