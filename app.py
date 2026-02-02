import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data(csv_path="data/water_potability.csv"):
    """
    Load water quality dataset from CSV and clean it.
    Fills missing numeric values with the column median.
    """
    try:
        df = pd.read_csv(csv_path)
        # Fill missing numeric values with median
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        return df
    except FileNotFoundError:
        st.error(f"File not found: {csv_path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
data = load_data()

    



# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Dataset Overview", "Parameter Trends", "Distribution", "Potability", "About"]
)

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":
    st.title("💧 Water Quality Dashboard")
    st.subheader("Exploratory Analysis of Water Quality Parameters")
    st.markdown("""
    This dashboard analyzes water quality data including parameters such as:
    - pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, trihalomethanes, Turbidity, Potability
    """)
    st.image("assets/cover.jpg", caption="Water Quality Overview")

# -------------------------------
# Dataset Overview
# -------------------------------
elif page == "Dataset Overview":
    st.title("📁 Dataset Overview")
    if data is not None:
        st.write("### Sample Records")
        st.dataframe(data.head(50))

        st.write("### Dataset Shape")
        st.write(f"Rows: {data.shape[0]}")
        st.write(f"Columns: {data.shape[1]}")

        st.write("### Column Names")
        st.write(list(data.columns))

        st.write("### Missing Values")
        st.dataframe(data.isnull().sum())

        st.write("### Basic Statistics")
        st.dataframe(data.describe())
    else:
        st.warning("Dataset not found. Please add your CSV in the data folder.")

# -------------------------------
# Parameter Trends
# -------------------------------
elif page == "Parameter Trends":
    st.title("📈 Parameter Trends Over Samples")
    if data is not None:
        parameters = [col for col in data.columns if col != "Potability"]
        selected_param = st.selectbox("Select Parameter", parameters)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data[selected_param], marker='o', linestyle='-', color='teal')
        ax.set_xlabel("Sample Index")
        ax.set_ylabel(selected_param)
        ax.set_title(f"{selected_param} Trend Over Samples")
        st.pyplot(fig)
    else:
        st.warning("No data available for trends.")

# -------------------------------
# Parameter Distribution
# -------------------------------
elif page == "Distribution":
    st.title("📊 Parameter Distribution")
    if data is not None:
        parameters = [col for col in data.columns if col != "Potability"]
        selected_param = st.selectbox("Select Parameter for Distribution", parameters)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(data[selected_param], bins=20, color='skyblue', edgecolor='black')
        ax.set_xlabel(selected_param)
        ax.set_ylabel("Frequency")
        ax.set_title(f"{selected_param} Distribution")
        st.pyplot(fig)
    else:
        st.warning("No data available for distribution.")

# -------------------------------
# Potability Summary
# -------------------------------
elif page == "Potability":
    st.title("💧 Water Potability Summary")
    if data is not None:
        if "Potability" in data.columns:
            pot_counts = data["Potability"].value_counts()
            st.write("### Potability Counts")
            st.dataframe(pot_counts)

            # Pie chart
            fig, ax = plt.subplots()
            ax.pie(
                pot_counts,
                labels=pot_counts.index.map({0: "Not Potable", 1: "Potable"}),
                autopct="%1.1f%%",
                colors=["salmon", "lightgreen"],
                startangle=90
            )
            ax.set_title("Water Potability Distribution")
            st.pyplot(fig)
        else:
            st.warning("No 'Potability' column found in dataset.")
    else:
        st.warning("No data available for Potability analysis.")

# -------------------------------
# About
# -------------------------------
elif page == "About":
    st.title("📚 About This Dashboard")
    st.markdown("""
    **Water Quality Dashboard**  
    This dashboard provides exploratory analysis of water quality parameters using Python, Pandas, Matplotlib, and Streamlit.  

    **Parameters included:**
    - pH, Hardness, Solids, Chloramines, Sulfate
    - Conductivity, Organic Carbon, Trihalomethanes, Turbidity, Potability

    **Author:** Qiniso Ntshingila
 
    **Purpose:** Explore parameter trends, distributions, and potability of water samples.
    """)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("© 2026 | Water Quality Dashboard")
