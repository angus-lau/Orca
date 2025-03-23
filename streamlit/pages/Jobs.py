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

# def jobs():
#     st.markdown(
#     "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Jobs</div>",
#     unsafe_allow_html=True)
    
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

if st.button("View Details", key=f"view_{job['id']}"):
  st.success(f"You clicked to view job: {job['prompt']} (ID: {job['id']})")

def jobs():
    st.markdown(
        "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Jobs</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.jobs:
        st.info("No jobs submitted yet.")
        return

    for job in st.session_state.jobs:
        with st.container():
            progress_percent = int(job["progress"] * 100)

            st.markdown(f"""
            <div style='
                border: 2px solid #868686;
                border-radius: 10px;
                padding: 16px;
                margin-bottom: 8px;
                background-color: #818181;
            '>
                <div style='font-size: 24px; font-weight: 600;'>{job['prompt']}</div>
                <div style='color: #ccc; font-size: 14px; margin-top: 4px;'>
                    Job ID: <code>{job['id']}</code> | Dataset: {job['dataset']}
                </div>
                <div style='margin-top: 8px; font-weight: 500;'>Status: {job['status']}</div>
                <div style='margin-top: 12px;'>
                    <div style='height: 14px; width: 100%; background-color: #e0e0e0; border-radius: 7px; overflow: hidden;'>
                        <div style='height: 100%; width: {progress_percent}%; background-color: #4CAF50;'></div>
                    </div>
                    <div style='font-size: 12px; color: #333; margin-top: 4px;'>{progress_percent}% complete</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ✅ This line must stay inside the loop
            if st.button("View Details", key=f"view_{job['id']}"):
                st.success(f"You clicked on job: {job['prompt']} (ID: {job['id']})")

# def jobs():
#     st.markdown(
#         "<div style='font-size: 40px; font-weight: bold; margin-bottom: 16px;'>Jobs</div>",
#         unsafe_allow_html=True
#     )

#     if not st.session_state.jobs:
#         st.info("No jobs submitted yet.")
#         return

#     for job in st.session_state.jobs:
#         with st.container():
#             progress_percent = int(job["progress"] * 100)

#             # Unique identifier for each button (so you can detect it later)
#             button_key = f"view_{job['id']}"

#             st.markdown(f"""
#             <form action="" method="post">
#             <div style='
#                 border: 2px solid #868686;
#                 border-radius: 10px;
#                 padding: 16px;
#                 margin-bottom: 16px;
#                 background-color: #818181;
#             '>
#                 <div style='font-size: 24px; font-weight: 600;'>{job['prompt']}</div>
#                 <div style='color: #ccc; font-size: 14px; margin-top: 4px;'>
#                     Job ID: <code>{job['id']}</code> | Dataset: {job['dataset']}
#                 </div>
#                 <div style='margin-top: 8px; font-weight: 500;'>Status: {job['status']}</div>
#                 <div style='margin-top: 12px;'>
#                     <div style='height: 14px; width: 100%; background-color: #e0e0e0; border-radius: 7px; overflow: hidden;'>
#                         <div style='height: 100%; width: {progress_percent}%; background-color: #4CAF50;'></div>
#                     </div>
#                     <div style='font-size: 12px; color: #333; margin-top: 4px;'>{progress_percent}% complete</div>
#                 </div>
#                 <button type="submit" name="job_button" value="{button_key}" style='
#                     margin-top: 12px;
#                     padding: 6px 12px;
#                     background-color: #4A90E2;
#                     color: white;
#                     border: none;
#                     border-radius: 6px;
#                     cursor: pointer;
#                     font-weight: bold;
#                 '>View Details</button>
#             </div>
#             </form>
#             """, unsafe_allow_html=True)

#             # 👇 Detect which button was clicked
#             if st.session_state.get("job_button_clicked") == button_key:
#                 st.success(f"Viewing details for job: {job['prompt']}")

#     # 👇 JavaScript to detect which button was clicked (must go once per page)
#     st.markdown("""
#         <script>
#         const forms = window.parent.document.querySelectorAll('form');
#         forms.forEach(form => {
#             form.addEventListener('submit', e => {
#                 const button = form.querySelector('button[name="job_button"]');
#                 if (button) {
#                     window.parent.postMessage({ type: 'streamlit:setComponentValue', value: button.value }, '*');
#                 }
#             });
#         });
#         </script>
#     """, unsafe_allow_html=True)

jobs()