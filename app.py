import streamlit as st
import pandas as pd

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

# Function to determine cluster manually based on Annual Income and Spending Score
def determine_cluster(annual_income, spending_score):
    if 40 <= annual_income <= 80 and 40 <= spending_score <= 60:
        return 1  # Cluster 1: Average income, average spender
    elif annual_income > 80 and spending_score > 60:
        return 2  # Cluster 2: High income, high spender
    elif annual_income > 80 and spending_score <= 60:
        return 3  # Cluster 3: High income, low spender
    elif annual_income <= 40 and spending_score <= 40:
        return 4  # Cluster 4: Low income, low spender
    elif annual_income <= 40 and spending_score > 60:
        return 5  # Cluster 5: Low income, high spender
    else:
        return 0  # Default/fallback cluster

# Suggested actions based on clusters
def get_action(cluster):
    if cluster == 1:
        return "Average income, average spender. Cautious with spending. Suggest limited-time discounts."
    elif cluster == 2:
        return "High-income, high-spender. Suggest VIP offers or exclusive deals to increase spending."
    elif cluster == 3:
        return "Higher income, low spender. Target with improved store services or offers."
    elif cluster == 4:
        return "Low-income, low-spender. Suggest budget-friendly deals and value-for-money products."
    elif cluster == 5:
        return "Low-income, high-spender. Suggest customer loyalty programs."
    else:
        return "Spending behavior doesn't fit predefined actions, needs further analysis."

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
        customer_cluster = determine_cluster(annual_income, spending_score)

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
