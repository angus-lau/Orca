import streamlit as st
import pandas as pd
import uuid

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

# Initialize session state
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "datasets" not in st.session_state:
    st.session_state.datasets = {}  # {filename: dataframe}

# if "page" not in st.session_state:
#     st.session_state.page = "Playground"

def playground():
    #st.title("Playground")
    st.markdown(
    "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Playground</div>",
    unsafe_allow_html=True
)
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

# def data():
#     st.title("Data")
#     uploaded_file = st.file_uploader("Upload your data", type=["csv", "xlsx"])

#     if uploaded_file is not None:
#         file_name = uploaded_file.name

#         if file_name not in st.session_state.datasets:
#             try:
#                 if file_name.endswith(".csv"):
#                     df = pd.read_csv(uploaded_file)
#                 elif file_name.endswith(".xlsx"):
#                     df = pd.read_excel(uploaded_file)
#                 else:
#                     st.error("Unsupported file format.")
#                     return

#                 st.session_state.datasets[file_name] = df
#                 st.success(f"'{file_name}' uploaded successfully!")
#             except Exception as e:
#                 st.error(f"Error reading file: {e}")

#     st.subheader("📂 Uploaded Datasets")

#     for name, df in st.session_state.datasets.items():
#         with st.container():
#             st.markdown(f"""
#                 <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; background-color: #f9f9f9;">
#                     <h4>{name}</h4>
#             """, unsafe_allow_html=True)

#             if st.button(f"Preview {name}"):
#                 st.write(df.head())

#             st.markdown("</div>", unsafe_allow_html=True)



# def jobs():
#     st.title("Jobs")
    
#     if not st.session_state.jobs:
#         st.info("No jobs submitted yet.")
#         return

#     # for job in st.session_state.jobs:
#     #     with st.container(border=True):
#     #         # st.subheader(f" {job['prompt']}")
#     #         st.markdown(f"<div style='font-size: 35px; font-weight: 400;'> {job['prompt']}</div>", unsafe_allow_html=True)
#     #         st.caption(f"Job ID: `{job['id']}` | Dataset: {job['dataset']}")
#     #         st.text(f"Status: {job['status']}")
#     #         st.progress(job['progress'])


#     for job in st.session_state.jobs:
#         with st.container():
#             progress_percent = int(job["progress"] * 100)  # assuming 0.0 to 1.0

#             st.markdown(f"""
# <div style='border: 2px solid #868686; border-radius: 10px; padding: 16px; margin-bottom: 16px; background-color: #818181;'>
#   <div style='font-size: 24px; font-weight: 600;'>{job['prompt']}</div>
#   <div style='color: #333; font-size: 14px; margin-top: 4px;'>Job ID: <code>{job['id']}</code> | Dataset: {job['dataset']}</div>
#   <div style='margin-top: 8px; font-weight: 500;'>Status: {job['status']}</div>
#   <div style='margin-top: 12px;'>
#     <div style='height: 14px; width: 100%; background-color: #e0e0e0; border-radius: 7px; overflow: hidden;'>
#       <div style='height: 100%; width: {int(job["progress"] * 100)}%; background-color: #4CAF50;'></div>
#     </div>
#     <div style='font-size: 12px; color: #333; margin-top: 4px;'>{int(job["progress"] * 100)}% complete</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)


# st.sidebar.title("ORCA AI")
# playground()

# # Sidebar navigation
# st.sidebar.title("ORCA AI")
# page = st.sidebar.radio("Navigate", ["Playground", "Data", "Jobs"])

# if page == "Playground":
#     playground()
# elif page == "Data":
#     data()
# elif page == "Jobs":
#     jobs()

# # Sidebar with buttons
# st.sidebar.title("ORCA AI")

# if st.sidebar.button("Playground"):
#     st.session_state.page = "Playground"

# if st.sidebar.button("Data"):
#     st.session_state.page = "Data"

# if st.sidebar.button("Jobs"):
#     st.session_state.page = "Jobs"

# # Page routing logic
# if st.session_state.page == "Playground":
#     playground()
# elif st.session_state.page == "Data":
#     data()
# elif st.session_state.page == "Jobs":
#     jobs()

playground()