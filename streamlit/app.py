import streamlit as st
import pandas as pd
import uuid
import os
import json
import sys
from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.dataset import Dataset
from agents.task_classifier_agent import TaskClassifierAgent
from agents.model_executor_agent import ModelExecutorAgent
from agents.feature_mapper_agent import FeatureMapperAgent

# Initialize session state
if "jobs" not in st.session_state:
    st.session_state.jobs = []

if "datasets" not in st.session_state:
    if os.path.exists("datasets.json"):
        with open("datasets.json", "r") as f:
            st.session_state.datasets = json.load(f)
    else:
        st.session_state.datasets = {}

if "page" not in st.session_state:
    st.session_state.page = "Playground"

# Sidebar with GitHub-style nav menu
st.sidebar.markdown("""
    <style>
        .sidebar-content a {
            display: block;
            padding: 0.6rem 1rem;
            margin: 0.25rem 0;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.2s ease;
        }
        .sidebar-content a:hover {
            background-color: #2a2a2a;
        }
        .sidebar-content a.active {
            background-color: #3f51b5;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='margin-bottom: 1rem;'>ORCA AI</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
for page_name in ["Playground", "Data", "Jobs"]:
    active_class = "active" if st.session_state.page == page_name else ""
    if st.sidebar.button(page_name, key=f"tab-{page_name}"):
        st.session_state.page = page_name
        st.rerun()
    # st.sidebar.markdown(f"<a class='{active_class}'>{page_name}</a>", unsafe_allow_html=True)
# st.sidebar.markdown("</div>", unsafe_allow_html=True)

def playground():
    st.title("Playground")
    prompt = st.text_area("Enter your prediction prompt here:")

    dataset_names = list(st.session_state.datasets.keys())

    if not dataset_names:
        st.warning("⚠️ No datasets uploaded yet. Please upload a dataset from the **Data** tab.")
        return

    selected_data = st.selectbox("Select relevant data", dataset_names)

    if st.button("Submit"):
        if prompt.strip() == "":
            st.warning("Please enter a prompt before submitting.")
        else:
            job_id = str(uuid.uuid4())[:8]
            job = {
                "id": job_id,
                "prompt": prompt,
                "status": "Starting...",
                "progress": 10,
                "dataset": selected_data,
                "prediction": "",
                "explanation": ""
            }
            st.session_state.jobs.append(job)

            job_ref = next(j for j in st.session_state.jobs if j["id"] == job_id)
            job_ref["status"] = "Loading dataset..."
            job_ref["progress"] = 20
            dataset = Dataset(file_path=st.session_state.datasets[selected_data])

            job_ref["status"] = "Classifying task..."
            job_ref["progress"] = 40
            task_agent = TaskClassifierAgent(prompt, dataset.columns())
            task_info = task_agent.run()
            task_type = task_info["task_type"]
            target_column = task_info["target_column"]

            job_ref["status"] = "Mapping features..."
            job_ref["progress"] = 60
            feature_agent = FeatureMapperAgent(prompt, dataset.columns(), target_column=target_column)
            features_info = feature_agent.run()
            features = features_info["features"]

            job_ref["status"] = "Training model..."
            job_ref["progress"] = 80
            executor = ModelExecutorAgent(
                dataset=dataset,
                task_type=task_type,
                target_column=target_column,
                features=features
            )
            model_path = executor.run()

            job_ref["status"] = "Making prediction..."
            job_ref["progress"] = 90
            pred, explanation = executor.predict_from_query(prompt)

            job_ref["prediction"] = str(pred)
            job_ref["explanation"] = explanation
            job_ref["status"] = "Completed"
            job_ref["progress"] = 100

            st.success("✅ Prediction complete! View the report in the Jobs tab.")

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

    st.markdown("""
    <style>
        .job-card {
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-left: 6px solid #007bff;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .job-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
        }
        .job-meta {
            font-size: 0.9rem;
            color: #888;
            margin-top: 0.25rem;
            margin-bottom: 0.75rem;
        }
        .job-status {
            font-size: 1rem;
            color: #00cc66;
            font-weight: bold;
        }
        .job-report {
            font-size: 1rem;
            color: white;
            margin-bottom: 1rem;
        }
        .back-button {
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    if "selected_job_id" in st.session_state:
        job = next((j for j in st.session_state.jobs if j["id"] == st.session_state.selected_job_id), None)
        if job:
            st.header("📄 Job Report")
            st.markdown(f"<div class='job-report'><strong>Question:</strong> {job['prompt']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='job-report'><strong>Answer:</strong> {job.get('prediction', 'Pending...')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='job-report'><strong>Reason:</strong> {job.get('explanation', 'Awaiting model response...')}</div>", unsafe_allow_html=True)

            if st.button("🔙 Back to Jobs", key="back-button"):
                del st.session_state.selected_job_id
            return

    for job in st.session_state.jobs:
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <div class="job-title">{job['prompt']}</div>
                <div class="job-meta">Job ID: <code>{job['id']}</code> | Dataset: <strong>{job['dataset']}</strong></div>
                <div class="job-status">Status: {job['status']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(job["progress"])

            if st.button("🔍 View Report", key=f"view-{job['id']}"):
                st.session_state.selected_job_id = job["id"]
                st.rerun()

# Page routing
if st.session_state.page == "Playground":
    playground()
elif st.session_state.page == "Data":
    data()
elif st.session_state.page == "Jobs":
    jobs()