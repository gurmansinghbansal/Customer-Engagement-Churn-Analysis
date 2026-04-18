import streamlit as st
import pandas as pd

st.title("Customer Engagement & Churn Analysis Dashboard")

# Load data
data = pd.read_csv("European_Bank.csv", sep=None, engine='python')
data.columns = data.columns.str.strip()

st.write(data.columns)

# Sidebar filter
st.sidebar.header("Filters")

geo_options = ["All", "France", "Germany", "Spain"]
selected_geo = st.sidebar.selectbox("Select Geography", geo_options)

filtered_data = data.copy()

if selected_geo != "All":
    col_name = f"Geography_{selected_geo}"
    if col_name in data.columns:
        filtered_data = data[data[col_name] == 1]

st.subheader(f"Data for: {selected_geo}")

# Detect churn column
churn_col = 'Exited'

# ----------------------------
# FEATURE ENGINEERING
# ----------------------------

# Engagement Group (SAFE)
def classify(row):
    active = row.get('IsActiveMember', 0)
    products = row.get('NumOfProducts', 0)

    if active == 1 and products > 1:
        return "Active_Engaged"
    elif active == 0 and products == 1:
        return "Inactive_LowProduct"
    elif active == 1:
        return "Active_LowProduct"
    else:
        return "Inactive_HighValue"

filtered_data['EngagementGroup'] = filtered_data.apply(classify, axis=1)

# Balance Ratio (SAFE)
if 'Balance' in filtered_data.columns and 'EstimatedSalary' in filtered_data.columns:
    filtered_data['BalanceSalaryRatio'] = (
        filtered_data['Balance'] / (filtered_data['EstimatedSalary'] + 1)
    )

# ----------------------------
# KPI
# ----------------------------
if churn_col:
    st.subheader("Overall Churn Rate")
    churn_rate = filtered_data[churn_col].mean()
    st.metric("Churn Rate", f"{churn_rate:.2%}")

# ----------------------------
# 4 GRAPHS
# ----------------------------
if churn_col:

    # 1️⃣ Active Membership
    if 'IsActiveMember' in filtered_data.columns:
        st.subheader("Churn by Active Membership")
        st.bar_chart(filtered_data.groupby('IsActiveMember')[churn_col].mean())

    # 2️⃣ Number of Products
    if 'NumOfProducts' in filtered_data.columns:
        st.subheader("Churn by Number of Products")
        st.bar_chart(filtered_data.groupby('NumOfProducts')[churn_col].mean())

    # 3️⃣ Engagement Group
    st.subheader("Churn by Engagement Group")
    st.bar_chart(filtered_data.groupby('EngagementGroup')[churn_col].mean())

    # 4️⃣ Balance Ratio
    if 'BalanceSalaryRatio' in filtered_data.columns:
        st.subheader("Balance to Salary Ratio")
        st.line_chart(filtered_data['BalanceSalaryRatio'])
