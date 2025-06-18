import streamlit as st
import prediction
import batch_prediction
import eda

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Select a Page:", ["Main Menu", "Prediction", "Batch Prediction"])

if page == "Main Menu":
    eda.run()
elif page == "Prediction":
    prediction.run()
elif page == "Batch Prediction":
    batch_prediction.run()
