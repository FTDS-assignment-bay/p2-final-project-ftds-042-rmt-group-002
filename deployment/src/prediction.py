import pickle
import streamlit as st
import numpy as np
import os
import pandas as pd


def run():
    current_dir = os.path.dirname(__file__)

    with open(os.path.join(current_dir, "churn_model.pkl"), "rb") as f:
        churn_model = pickle.load(f)

    with open(os.path.join(current_dir, "kproto_bundle.pkl"), "rb") as f:
        cluster_bundle = pickle.load(f)

    st.title("📲 Churn Prediction + Customer Clustering")

    st.write("### Input Customer Data")

    complains_input = st.selectbox(
        "Has the customer ever filed a complaint?",
        ["No", "Yes"],
    )
    complains = 1 if complains_input == "Yes" else 0

    subscription_length = st.number_input(
        "Subscription Length (months)",
        min_value=1,
        help="Customer's subscription duration."
    )

    charge_amount = st.selectbox(
        "Charge Amount (monthly range)",
        list(range(0, 11)),
        help="Monthly charge level, ranging from 0 (lowest) to 10 (highest)"
    )

    seconds_of_use = st.number_input(
        "Total Seconds of Use",
        min_value=0.0,
        help="Sum of total time the customer has spent on calls."
    )

    call_failure = st.number_input(
    "Number of Call Failures",
    min_value=0,
    help="How many times the customer attempted a call but failed."
    )

    frequency_of_use = st.number_input(
        "Call Frequency",
        min_value=0.0,
        help="Total number of calls made"
    )

    distinct_called_numbers = st.number_input(
        "Distinct Called Numbers",
        min_value=0,
        help="Unique phone numbers the customer has reached out to"
    )

    age = st.number_input(
        "Your Age",
        min_value=18,
        help="Customer's age"
    )

    if age <= 24:
        age_group = 1
    elif age <= 29:
        age_group = 2
    elif age <= 44:
        age_group = 3
    elif age <= 54:
        age_group = 4
    else:
        age_group = 5

    tariff_plan_input = st.selectbox(
        "Tariff Plan",
        ["Prepaid", "Postpaid"],
    )
    tariff_plan = 1 if tariff_plan_input == "Postpaid" else 0

    status_input = st.selectbox(
        "Account Status",
        ["Inactive", "Active"],
    )
    status = 1 if status_input == "Active" else 0

    customer_value = st.number_input(
        "Customer Value",
        min_value=0.0,
        help="Average monthly payment × number of months subscribed"
    )

    frequency_of_sms = 0

    full_data = pd.DataFrame([{
    'call_failure': call_failure,
    'complains': complains,
    'subscription_length': subscription_length,
    'charge_amount': charge_amount,
    'seconds_of_use': seconds_of_use,
    'frequency_of_use': frequency_of_use,
    'distinct_called_numbers': distinct_called_numbers,
    'age_group': age_group,
    'frequency_of_sms': frequency_of_sms,
    'tariff_plan': tariff_plan,
    'status': status,
    'age': age,
    'customer_value': customer_value
    }])


    # churn pred prep
    churn_input = full_data.drop(columns=['call_failure', 'frequency_of_sms', 'age', 'frequency_of_use'])
    churn_pred = churn_model.predict(churn_input)[0]

    cluster_descriptions = {
        0: {
            "Activity Level": "High",
            "Subscription Duration": "Long",
            "Cost (Charge)": "Low",
            "Technical Complaints": "High",
            "Potential Reason for Churn": "Technical issues"
        },
        1: {
            "Activity Level": "Low",
            "Subscription Duration": "Long",
            "Cost (Charge)": "Very Low",
            "Technical Complaints": "Low",
            "Potential Reason for Churn": "Not seeing the benefits"
        },
        2: {
            "Activity Level": "Medium",
            "Subscription Duration": "Short",
            "Cost (Charge)": "High",
            "Technical Complaints": "Medium",
            "Potential Reason for Churn": "High initial cost burden"
        }
    }

    if st.button("Predict Churn and Cluster"):
        if churn_pred == 1:
            st.warning("⚠️ Churn Predicted!")

            # Do clustering only for churn-predicted customers
            df_cluster_input = full_data[cluster_bundle['final_columns_order']]
            numerical_data = df_cluster_input[cluster_bundle['numerical_cols']]
            categorical_data = df_cluster_input[cluster_bundle['categorical_cols']].astype(str)

            # preprocess
            num_scaled = cluster_bundle['scaler'].transform(numerical_data)
            num_pca = cluster_bundle['pca_model'].transform(num_scaled)
            final_input = np.hstack([num_pca, categorical_data.to_numpy()])
            cluster_pred = cluster_bundle['kproto_model'].predict(
                final_input,
                categorical=cluster_bundle['categorical_indices']
            )[0]

            # Show cluster description
            st.subheader(f"🧩 Cluster: {cluster_pred}")
            desc = cluster_descriptions.get(cluster_pred, {})
            st.markdown(f"""
            **Cluster Description (for churned customer):**
            - **Activity Level:** {desc.get("Activity Level", "-")}
            - **Subscription Duration:** {desc.get("Subscription Duration", "-")}
            - **Cost (Charge):** {desc.get("Cost (Charge)", "-")}
            - **Technical Complaints:** {desc.get("Technical Complaints", "-")}
            - **Potential Reason for Churn:** {desc.get("Potential Reason for Churn", "-")}
            """)
        else:
            st.success("✅ No Churn Predicted.")
            st.info("ℹ️ Clustering is only applied to churn-predicted customers.")


if __name__ == '__main__':
    run()
