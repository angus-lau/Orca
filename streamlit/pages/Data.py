import streamlit as st

# NAME TAB NAME TO "ORCA AI"
st.set_page_config(page_title="ORCA AI", layout="wide")

# FORCE "ORCA AI" to go above automatic page navigator
st.markdown("""
    <style>
        /* Create a fake top banner inside the sidebar */
        [data-testid="stSidebar"] > div:first-child {
            position: relative;
        }

        [data-testid="stSidebar"]::before {
            content: "ORCA AI";
            display: block;
            font-size: 50px;
            font-weight: bold;
            padding: 1rem 1.5rem 0.5rem 1.5rem;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "datasets" not in st.session_state:
    st.session_state.datasets = {}  # {filename: dataframe}

def data():
    #st.title("Data")
    st.markdown(
    "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Data</div>",
    unsafe_allow_html=True
)
    uploaded_file = st.file_uploader("Upload your data", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_name = uploaded_file.name

        if file_name not in st.session_state.datasets:
            try:
                if file_name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif file_name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Unsupported file format.")
                    return

                st.session_state.datasets[file_name] = df
                st.success(f"'{file_name}' uploaded successfully!")
            except Exception as e:
                st.error(f"Error reading file: {e}")
data()