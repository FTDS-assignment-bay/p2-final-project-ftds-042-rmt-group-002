import streamlit as st

def run():
    st.title("📊 Welcome to Clusturn")

    st.markdown("""
    ## What is Clusturn?

    **Clusturn** is a customer segmentation application that leverages machine learning to identify distinct customer groups based on behavior and churn risk.

    This tool is built to help businesses:
    - Understand customer patterns more effectively
    - Predict potential churn
    - Cluster customers into meaningful segments
    - Design targeted and impactful retention strategies
    """)

    st.markdown("## How to Use Clusturn")
    st.markdown("""
    Clusturn consists of **two key features**:

    1. **🔍 Prediction Page**  
       - Enter customer data manually.
       - Get an instant churn prediction and cluster classification.
       - Useful for testing individual customer profiles.

    2. **📁 Batch Prediction Page**  
       - Upload a `.csv` or `.xlsx` file with customer data.
       - Automatically generates churn predictions and cluster assignments for each row.
       - Ideal for analyzing multiple customers at once.

    ---
    """)

    st.info("Explore the menu on the left to try Prediction or Batch Prediction!")

if __name__ == '__main__':
    run()
