import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Mall.csv')

# Data Preprocessing
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Scale Annual Income and Spending Score without additional custom scaling
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train the K-Means model
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
labels = kmeans.fit_predict(X_scaled)

# Add the cluster labels to the dataframe
df['Cluster'] = labels

# Suggested actions based on clusters
def get_action(cluster):
    if cluster == 0:
        return "Average income, average spender. Cautious with spending. Suggest limited-time discounts."
    elif cluster == 1:
        return "High-income, high-spender. Suggest VIP offers or exclusive deals to increase spending."
    elif cluster == 2:
        return "Higher income, low spender. Target with improved store services or offers."
    elif cluster == 3:
        return "Low-income, low-spender. Suggest budget-friendly deals and value-for-money products."
    elif cluster == 4:
        return "Low-income, high-spender. Suggest customer loyalty programs."

# Streamlit app interface
st.markdown("<div class='title'>Mall Customer Segmentation</div>", unsafe_allow_html=True)

# Option for customer or mall owner
user_type = st.selectbox("Are you a Customer or Mall Owner?", ["Customer", "Mall Owner"])

if user_type == "Customer":
    st.markdown("<div class='header'>Customer Input</div>", unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email")
    annual_income = st.slider("Annual Income (k$)", 0, 150, 50)
    spending_score = st.slider("Spending Score (1-100)", 0, 100, 50)

    if st.button("Submit"):
        customer_data = pd.DataFrame([[annual_income, spending_score]], columns=['Annual Income (k$)', 'Spending Score (1-100)'])
        customer_scaled = scaler.transform(customer_data)
        customer_cluster = kmeans.predict(customer_scaled)[0]

        st.success(f"Thank you, {name}! Your response has been recorded.")
        st.write(f"You belong to Cluster {customer_cluster}. You will receive marketing emails accordingly.")
        
        # Save customer info
        new_customer = pd.DataFrame([[name, email, annual_income, spending_score, customer_cluster]], 
                                    columns=['Name', 'Email', 'Annual Income', 'Spending Score', 'Cluster'])
        if 'customers' not in st.session_state:
            st.session_state.customers = new_customer
        else:
            st.session_state.customers = pd.concat([st.session_state.customers, new_customer], ignore_index=True)

elif user_type == "Mall Owner":
    st.markdown("<div class='header'>Mall Owner Login</div>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if username == "mallowner" and password == "password":
        st.success("Logged in successfully!")
        
        if 'customers' in st.session_state:
            st.markdown("<div class='subheader'>Customer Data and Segmentation</div>", unsafe_allow_html=True)
            st.dataframe(st.session_state.customers)

            # Display suggested actions for each customer
            for idx, row in st.session_state.customers.iterrows():
                st.markdown(f"<div class='cluster-result'>Customer: {row['Name']} (Cluster {row['Cluster']}) - Action: {get_action(row['Cluster'])}</div>", unsafe_allow_html=True)
        else:
            st.write("No customer data available.")
    else:
        if st.button("Login"):
            st.error("Invalid credentials. Please try again.")
