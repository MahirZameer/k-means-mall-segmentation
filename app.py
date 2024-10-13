import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Custom CSS to enhance the visual look of the app
st.markdown("""
    <style>
    body {
        background-color: #2F4F4F;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #FFA500;
        color: white;
        font-size: 18px;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #F0F8FF;
        color: black;
        font-size: 16px;
    }
    .title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #00FA9A;
    }
    .header {
        font-size: 25px;
        color: #00CED1;
        font-weight: bold;
    }
    .subheader {
        font-size: 20px;
        color: #FFF8DC;
    }
    .stSelectbox>div>div>div {
        background-color: #FFE4B5;
        color: black;
    }
    .cluster-result {
        background-color: #708090;
        color: white;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Load the dataset
df = pd.read_csv('Mall.csv')

# Data Preprocessing
X = df[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Scale Annual Income differently to give it more weight
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Apply custom scaling to the 'Annual Income' feature to weight it more
X_scaled[:, 0] = X_scaled[:, 0] * 1.5  # Increase weight of Annual Income

# Train the K-Means model with 6 clusters
kmeans = KMeans(n_clusters=6, init='k-means++', random_state=42)
labels = kmeans.fit_predict(X_scaled)

# Add the cluster labels to the dataframe
df['Cluster'] = labels

# Function to adjust clusters based on thresholds
def adjust_cluster(row):
    income = row['Annual Income (k$)']
    spending = row['Spending Score (1-100)']
    
    # Adjust Cluster 4 for low-income high-spenders
    if row['Cluster'] == 4:
        if spending < 60:
            return 3  # Re-assign to Cluster 3 if spending doesn't match high-spender description
    return row['Cluster']

# Apply the adjustment function
df['Cluster'] = df.apply(adjust_cluster, axis=1)

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
    elif cluster == 5:
        return "New Cluster - investigate further."

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
        customer_scaled[:, 0] = customer_scaled[:, 0] * 1.5
        customer_cluster = kmeans.predict(customer_scaled)[0]

        # Apply adjustment to the cluster if needed
        customer_cluster = adjust_cluster(pd.Series({'Annual Income (k$)': annual_income, 'Spending Score (1-100)': spending_score, 'Cluster': customer_cluster}))

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
