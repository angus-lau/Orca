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

#st.sidebar.markdown("## ORCA AI")

if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "datasets" not in st.session_state:
    st.session_state.datasets = {}  # {filename: dataframe}

def jobs():
    #st.title("Jobs")
    st.markdown(
    "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Jobs</div>",
    unsafe_allow_html=True)
    
    if not st.session_state.jobs:
        st.info("No jobs submitted yet.")
        return

    # for job in st.session_state.jobs:
    #     with st.container(border=True):
    #         # st.subheader(f" {job['prompt']}")
    #         st.markdown(f"<div style='font-size: 35px; font-weight: 400;'> {job['prompt']}</div>", unsafe_allow_html=True)
    #         st.caption(f"Job ID: `{job['id']}` | Dataset: {job['dataset']}")
    #         st.text(f"Status: {job['status']}")
    #         st.progress(job['progress'])


    for job in st.session_state.jobs:
        with st.container():
            progress_percent = int(job["progress"] * 100)  # assuming 0.0 to 1.0

            st.markdown(f"""
<div style='border: 2px solid #868686; border-radius: 10px; padding: 16px; margin-bottom: 16px; background-color: #818181;'>
  <div style='font-size: 24px; font-weight: 600;'>{job['prompt']}</div>
  <div style='color: #333; font-size: 14px; margin-top: 4px;'>Job ID: <code>{job['id']}</code> | Dataset: {job['dataset']}</div>
  <div style='margin-top: 8px; font-weight: 500;'>Status: {job['status']}</div>
  <div style='margin-top: 12px;'>
    <div style='height: 14px; width: 100%; background-color: #e0e0e0; border-radius: 7px; overflow: hidden;'>
      <div style='height: 100%; width: {int(job["progress"] * 100)}%; background-color: #4CAF50;'></div>
    </div>
    <div style='font-size: 12px; color: #333; margin-top: 4px;'>{int(job["progress"] * 100)}% complete</div>
  </div>
</div>
""", unsafe_allow_html=True)

jobs()