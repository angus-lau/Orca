import streamlit as st
import pandas as pd
import uuid
import os  # Add this to the top of the file
import json

# Initialize session state
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "datasets" not in st.session_state:
        if os.path.exists("datasets.json"):
            with open("datasets.json", "r") as f:
                st.session_state.datasets = json.load(f)
        else:
            st.session_state.datasets = {}  # {filename: filepath}

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
    st.markdown("""
    <style>
    ::selection {
        background: #d7d7d7 !important;
        color: #000000 !important;
    }

    ::-moz-selection {
        background: #d7d7d7 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your data", type=["csv", "xlsx"])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        upload_dir = "uploaded_data"

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        save_path = os.path.join(upload_dir, file_name)

        if file_name not in st.session_state.datasets:
            try:
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.session_state.datasets[file_name] = save_path
                with open("datasets.json", "w") as f:
                    json.dump(st.session_state.datasets, f, indent=4)
                st.success(f"'{file_name}' uploaded and saved to '{save_path}'!")
            except Exception as e:
                st.error(f"Error saving file: {e}")

    st.subheader("📂 Uploaded Datasets")

    for name, path in st.session_state.datasets.items():
        with st.container():
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; background-color: #f9f9f9; color: #000;">
                    <h4>{name}</h4>
                    <p>Path: {path}</p>
            """, unsafe_allow_html=True)

            if st.button(f"Preview {name}"):
                try:
                    if name.endswith(".csv"):
                        df = pd.read_csv(path)
                    elif name.endswith(".xlsx"):
                        df = pd.read_excel(path)
                    st.write(df.head())
                except Exception as e:
                    st.error(f"Error loading preview: {e}")

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