import pickle
import streamlit as st
import numpy as np
import os
import pandas as pd
from io import BytesIO


def run():
    current_dir = os.path.dirname(__file__)

    with open(os.path.join(current_dir, "churn_model.pkl"), "rb") as f:
        churn_model = pickle.load(f)

    with open(os.path.join(current_dir, "kproto_bundle.pkl"), "rb") as f:
        cluster_bundle = pickle.load(f)

    st.title("📂 Batch Churn Prediction + Customer Clustering")

    st.write("### 📋 Expected Columns Explanation")
    column_descriptions = {
        "call failure": "Number of failed call attempts",
        "complains": "Whether customer has made a complaint (0 = No, 1 = Yes)",
        "subscription length": "How many months the customer has been subscribed",
        "charge amount": "Monthly charge level, from 0 (lowest) to 10 (highest)",
        "seconds of use": "Total seconds of call usage",
        "frequency of use": "Total number of calls",
        "distinct called numbers": "Unique phone numbers contacted",
        "age": "Customer's age in years",
        "tariff plan": "0 = Prepaid, 1 = Postpaid",
        "status": "0 = Inactive, 1 = Active",
        "customer value": "Average monthly payment × number of months",
    }
    desc_df = pd.DataFrame(column_descriptions.items(), columns=["Column", "Description"])
    st.dataframe(desc_df)

    st.write("### 🧩 Cluster Descriptions and Business Recommendations")
    cluster_text = {
        0: [
            "**Cluster 0 – Active, Experienced, but Churn Due to Quality**",
            "- Long subscription (avg. 35 months)",
            "- High usage (seconds_of_use > 2600)",
            "- High call failure (~15)",
            "- Very low charges (avg. 0.18)",
            "- Very high customer value (213.27)",
            "- Younger-mid age (avg. 28.5)",
            " ",
            "**Business Recommendations:**",
            "- Improve technical service quality (network, signal, etc.)",
            "- Implement early-warning system for excessive call failures",
            "- Offer loyalty rewards or service failure compensation"
        ],
        1: [
            "**Cluster 1 – Passive, Rarely Use, Churn Due to Low Perceived Benefit**",
            "- Long subscription (avg. 35.5 months)",
            "- Very low usage (seconds_of_use: 889, frequency_of_use: 13.98)",
            "- Very low charges and customer value",
            "- Slightly older (avg. 30.5)",
            " ",
            "**Business Recommendations:**",
            "- Promote and educate customers about service benefits",
            "- Launch new offerings to reignite interest",
            "- Reevaluate fit; consider downgrade or segmentation"
        ],
        2: [
            "**Cluster 2 – New Customers Disappointed by High Cost**",
            "- Short subscription (avg. 22 months)",
            "- Medium usage, medium complaints",
            "- Highest charge amount (avg. 1.15)",
            "- Low-mid customer value (87.87)",
            "- Young (avg. 28.69)",
            " ",
            "**Business Recommendations:**",
            "- Analyze customer preferences and expectations",
            "- Proactively share personalized service recommendations",
            "- Offer initial discounts or free services to boost engagement"
        ]
    }
    for lines in cluster_text.values():
        st.markdown("\n".join(lines))
        st.markdown("---")

    st.write("### 📤 Upload Your Dataset (.csv or .xlsx)")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("#### 🔍 Preview Uploaded Data")
        st.dataframe(data.head())

        # Clean column names
        data.columns = data.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

        # Compute age group
        data['age_group'] = pd.cut(
            data['age'],
            bins=[0, 24, 29, 44, 54, 200],
            labels=[1, 2, 3, 4, 5],
            right=True
        ).astype(int)

        # Add missing column
        data['frequency_of_sms'] = 0

        # Prepare churn input
        churn_input = data.drop(columns=['call_failure', 'frequency_of_sms', 'age', 'frequency_of_use'])
        churn_preds = churn_model.predict(churn_input)

        # Cluster only churned
        data['churn_prediction'] = churn_preds
        cluster_results = []

        for i, row in data.iterrows():
            if row['churn_prediction'] == 1:
                input_row = row[cluster_bundle['final_columns_order']].to_frame().T
                num_scaled = cluster_bundle['scaler'].transform(input_row[cluster_bundle['numerical_cols']])
                num_pca = cluster_bundle['pca_model'].transform(num_scaled)
                cat = input_row[cluster_bundle['categorical_cols']].astype(str).to_numpy()
                final_input = np.hstack([num_pca, cat])
                cluster = cluster_bundle['kproto_model'].predict(
                    final_input,
                    categorical=cluster_bundle['categorical_indices']
                )[0]
                cluster_results.append(cluster)
            else:
                cluster_results.append("-")

        data['cluster'] = cluster_results

        data = data.sort_values(by="churn_prediction", ascending=False)
        st.write("### ✅ Prediction Results")
        st.dataframe(data)

        st.info("ℹ️ Only customers predicted to churn are clustered. Non-churned rows show '-' in the cluster column.")

        # Download result
        st.write("### 💾 Download Prediction Results")
        download_format = st.selectbox("Choose format", ["CSV", "Excel"])

        if download_format == "CSV":
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="churn_predictions.csv", mime='text/csv')
        else:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Predictions')
            st.download_button("Download Excel", data=output.getvalue(), file_name="churn_predictions.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    run()
