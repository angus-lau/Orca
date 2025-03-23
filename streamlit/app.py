import streamlit as st
import pandas as pd
import uuid

# Initialize session state
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "datasets" not in st.session_state:
    st.session_state.datasets = {}  # {filename: dataframe}

def playground():
    st.title("Playground")
    prompt = st.text_area("Enter your prediction prompt here:")

    dataset_names = list(st.session_state.datasets.keys())
    selected_data = st.selectbox("Select relevant data", dataset_names or ["No datasets uploaded yet"])
    
    if st.button("Submit"):
        if prompt.strip() == "":
            st.warning("Please enter a prompt before submitting.")
        else:
            job_id = str(uuid.uuid4())[:8]
            job = {
                "id": job_id,
                "prompt": prompt,
                "status": "Queued",
                "progress": 0,
                "dataset": selected_data
            }
            st.session_state.jobs.append(job)
            st.success(f"Job '{prompt}' submitted! Check Jobs tab for progress.")

def data():
    st.title("Data")
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

    st.subheader("📂 Uploaded Datasets")

    for name, df in st.session_state.datasets.items():
        with st.container():
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; background-color: #f9f9f9;">
                    <h4>{name}</h4>
            """, unsafe_allow_html=True)

            if st.button(f"Preview {name}"):
                st.write(df.head())

            st.markdown("</div>", unsafe_allow_html=True)



def jobs():
    st.title("Jobs")
    
    if not st.session_state.jobs:
        st.info("No jobs submitted yet.")
        return

    for job in st.session_state.jobs:
        with st.container():
            st.subheader(f"🔹 {job['prompt']}")
            st.caption(f"Job ID: `{job['id']}` | Dataset: {job['dataset']}")
            st.text(f"Status: {job['status']}")
            st.progress(job['progress'])

# Sidebar navigation
st.sidebar.title("ORCA AI")
page = st.sidebar.radio("Navigate", ["Playground", "Data", "Jobs"])

if page == "Playground":
    playground()
elif page == "Data":
    data()
elif page == "Jobs":
    jobs()