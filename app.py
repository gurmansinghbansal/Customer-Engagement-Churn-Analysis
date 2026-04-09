import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("Customer Engagement & Churn Analysis Dashboard")

# Load data
data = pd.read_csv("clean_features.csv")
data.columns = data.columns.str.strip()

def get_country(row):
    if 'Geography_Germany' in row and row['Geography_Germany'] == 1:
        return 'Germany'
    elif 'Geography_Spain' in row and row['Geography_Spain'] == 1:
        return 'Spain'
    else:
        return 'France'

data['Geography'] = data.apply(get_country, axis=1)
# Feature Engineering
# -----------------------------

# Engagement Group
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
        
data['EngagementGroup'] = data.apply(lambda row: classify(row), axis=1)

# Balance Ratio
balance = data.get('Balance', 0)
salary = data.get('EstimatedSalary', 1)

data['BalanceSalaryRatio'] = balance / (salary + 1)

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
churn_col = 'Exited' if 'Exited' in filtered_data.columns else 'target'
churn_rate = filtered_data[churn_col].mean()
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
