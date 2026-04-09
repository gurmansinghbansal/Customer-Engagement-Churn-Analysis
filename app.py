import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("Customer Engagement & Churn Analysis Dashboard")

# Load data
data = pd.read_csv("clean_features.csv")

# Feature Engineering
# -----------------------------

# Engagement Group
def classify(row):
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] > 1:
        return "Active_Engaged"
    elif row['IsActiveMember'] == 0 and row['NumOfProducts'] == 1:
        return "Inactive_LowProduct"
    elif row['IsActiveMember'] == 1:
        return "Active_LowProduct"
    else:
        return "Inactive_HighValue"

data['EngagementGroup'] = data.apply(classify, axis=1)

# Balance Ratio
data['BalanceSalaryRatio'] = data['Balance'] / (data['EstimatedSalary'] + 1)

# Balance Group
data['BalanceGroup'] = pd.cut(
    data['BalanceSalaryRatio'],
    bins=[-1, 1, 3, 100],
    labels=['Low', 'Medium', 'High']
)

# -----------------------------
# Sidebar Filter
# -----------------------------

st.sidebar.header("Filters")

selected_geo = st.sidebar.selectbox(
    "Select Geography",
    data['Geography'].unique()
)

filtered_data = data[data['Geography'] == selected_geo]

# -----------------------------
# KPI
# -----------------------------

st.subheader("Overall Churn Rate")
churn_rate = filtered_data['Exited'].mean()
st.metric("Churn Rate", f"{churn_rate:.2f}")

# -----------------------------
# Graph 1: Active Membership
# -----------------------------

st.subheader("Churn by Active Membership")

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x='IsActiveMember', y='Exited', data=filtered_data, ax=ax1)
ax1.set_xlabel("IsActive Member (0 = No, 1 = Yes)")
ax1.set_ylabel("Churn Rate")

st.pyplot(fig1)

# -----------------------------
# Graph 2: Number of Products
# -----------------------------

st.subheader("Churn by Number of Products")

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(x='NumOfProducts', y='Exited', data=filtered_data, ax=ax2)
ax2.set_xlabel("NumberOfProducts")
ax2.set_ylabel("Churn Rate")

st.pyplot(fig2)

# -----------------------------
# Graph 3: Engagement Group
# -----------------------------

st.subheader("Churn by Engagement Group")

fig3, ax3 = plt.subplots(figsize=(8,5))
sns.barplot(x='EngagementGroup', y='Exited', data=filtered_data, ax=ax3)
plt.xticks(rotation=45)
ax3.set_xlabel("Engagement Group")
ax3.set_ylabel("Churn Rate")

st.pyplot(fig3)

# -----------------------------
# Graph 4: Balance Group
# -----------------------------

st.subheader("Churn by Balance-Salary Group")

fig4, ax4 = plt.subplots(figsize=(8,5))
sns.barplot(x='BalanceGroup', y='Exited', data=filtered_data, ax=ax4)
ax4.set_xlabel("Balance Group")
ax4.set_ylabel("Churn Rate")
st.pyplot(fig4)
