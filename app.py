import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Churn Dashboard", layout="wide")

st.title("Customer Engagement & Churn Analysis Dashboard")

data = pd.read_csv("European_Bank.csv", header=None)

data = data.iloc[:, 0].str.split(",", expand=True)

data.columns = data.iloc[0]
data = data[1:]

data.columns = data.columns.str.strip()

# Convert types safely
numeric_cols = [
    'CreditScore','Age','Tenure','Balance',
    'NumOfProducts','HasCrCard','IsActiveMember',
    'EstimatedSalary','Exited'
]

for col in numeric_cols:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Restore Geography as string
data['Geography'] = data['Geography'].astype(str).str.strip()

data.reset_index(drop=True, inplace=True)


required_cols = ['Geography', 'Exited']
for col in required_cols:
    if col not in data.columns:
        st.error(f"Column '{col}' not found in dataset")
        st.stop()

# Sidebar filter
st.sidebar.header("Filters")

geo_options = ["All"] + sorted(data['Geography'].dropna().unique().tolist())
selected_geo = st.sidebar.selectbox("Select Geography", geo_options)

if selected_geo == "All":
    filtered_data = data.copy()
else:
    filtered_data = data[data['Geography'] == selected_geo].copy()

st.subheader(f"Data for: {selected_geo}")

# KPI
st.subheader("Overall Churn Rate")
churn_rate = filtered_data['Exited'].mean()
st.write(f"Churn Rate: {churn_rate:.2%}")

# Feature Engineering

if 'Balance' in filtered_data.columns and 'EstimatedSalary' in filtered_data.columns:
    filtered_data['BalanceSalaryRatio'] = (
        filtered_data['Balance'] / (filtered_data['EstimatedSalary'] + 1)
    )

    # Create groups
    filtered_data['BalanceGroup'] = pd.cut(
        filtered_data['BalanceSalaryRatio'],
        bins=[-1, 1, 2, 100],
        labels=['Low', 'Medium', 'High']
    )
def classify(row):
    active = row['IsActiveMember'] if 'IsActiveMember' in row else 0
    products = row['NumOfProducts'] if 'NumOfProducts' in row else 0

    if active == 1 and products > 1:
        return "Active_Engaged"
    elif active == 0 and products == 1:
        return "Inactive_LowProduct"
    elif active == 1:
        return "Active_LowProduct"
    else:
        return "Inactive_HighValue"

if 'IsActiveMember' in filtered_data.columns and 'NumOfProducts' in filtered_data.columns:
    filtered_data['EngagementGroup'] = filtered_data.apply(classify, axis=1)

# Graph 1
if 'IsActiveMember' in filtered_data.columns:
    st.subheader("Churn by Active Membership")
    fig2, ax2 = plt.subplots()
    sns.barplot(x='IsActiveMember', y='Exited', data=filtered_data, ax=ax2)
    st.pyplot(fig2)

# Graph 2
if 'NumOfProducts' in filtered_data.columns:
    st.subheader("Churn by Number of Products")
    fig3, ax3 = plt.subplots()
    sns.barplot(x='NumOfProducts', y='Exited', data=filtered_data, ax=ax3)
    st.pyplot(fig3)

# Graph 3
if 'EngagementGroup' in filtered_data.columns:
    st.subheader("Churn by Engagement Group")
    fig4, ax4 = plt.subplots()
    sns.barplot(x='EngagementGroup', y='Exited', data=filtered_data, ax=ax4)
    st.pyplot(fig4)

# Graph 4
if 'BalanceGroup' in filtered_data.columns:
    st.subheader("Churn Rate by Balance-Salary Group")

    fig, ax = plt.subplots()
    sns.barplot(
        data=filtered_data,
        x='BalanceGroup',
        y='Exited',
        ax=ax
    )

    ax.set_ylabel("Churn Rate")
    ax.set_xlabel("Balance-Salary Group")

    st.pyplot(fig)
