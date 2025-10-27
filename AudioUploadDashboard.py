import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import random
from io import BytesIO
import soundfile as sf

from audio_data_utils import load_audio_metadata

def downloadFilesToServer():
    # Download Button
    st.subheader("Download Filtered Dataset")
    csv_buffer = BytesIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="filtered_dataset.csv",
        mime="text/csv"
    )

    # Remote Copy Simulation
    st.header("📡 Remote Server File Copy (Demo)")
    with st.form("remote_server_form"):
        st.subheader("Connect to Remote Server")
        server = st.text_input("Server Address")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        destination_dir = st.text_input("Destination Directory")
        submitted = st.form_submit_button("Connect")

    if submitted:
        if server and username and password:
            st.success(f"✅ Connected to {server} as {username} (demo mode)")
        else:
            st.error("⚠️ Please fill in all connection fields.")

    if st.button("Copy Matching Files (Demo)"):
        if not (server and username and password):
            st.warning("Please connect to the remote server first.")
        elif not destination_dir:
            st.warning("Please specify a destination directory.")
        else:
            st.info(f"Starting copy to {destination_dir} on {server}...")
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.03)
                progress_bar.progress(percent_complete + 1)
            st.success("✅ Files copied successfully (demo only)")

def uploadSideBar(st):
    st.sidebar.header("Upload Metadata")
    project = st.sidebar.text_input("Project Name selection", st.session_state.upload_metadata.get("project", ""))
    owner = st.sidebar.text_input("Owner", st.session_state.upload_metadata.get("owner", ""))
    date = st.sidebar.date_input("Date", st.session_state.upload_metadata.get("date", datetime.date.today()))
    st.session_state.upload_metadata.update({"project": project, "owner": owner, "date": date})

def sideBar(st):
    search_term = st.sidebar.text_input("Search by filename")
    hearing_filter = st.sidebar.selectbox("Hearing Aid", options=['yes', 'no'], index=1)
    if hearing_filter == 'yes':
        ha_type_filter = st.sidebar.multiselect("Hearing Aid HW", options=df['ha_type'].unique(),
                                                default=df['ha_type'].unique())
        mic_position_filter = st.sidebar.multiselect("Microphone", options=df['mic_position'].unique(),
                                                     default=df['mic_position'].unique())
        rec_position_filter = st.sidebar.multiselect("Receiver", options=df['Receiver'].unique(),
                                                     default=df['Receiver'].unique())
    else:
        ha_type_filter = df['ha_type'].unique()
        mic_position_filter = df['mic_position'].unique()
        rec_position_filter = df['Receiver'].unique()
        cchannel_filter = df['channel'].unique()

    duration_range = st.sidebar.slider("Duration (sec)", 0, 60, (0, 60))
    volume_range = st.sidebar.slider("Volume (dB)", float(df['volume_db'].min()), float(df['volume_db'].max()),
                                     (float(df['volume_db'].min()), float(df['volume_db'].max())))
    file_type_filter = st.sidebar.multiselect("File Type", options=df['file_type'].unique(),
                                              default=df['file_type'].unique())

    wola_type_filter = st.sidebar.multiselect("WOLA Type", options=df['wola_type'].unique(),
                                              default=df['wola_type'].unique())

    # Apply filters
    filtered_df = df[
        (df['hearing_aid'].isin(['yes'])) &
        (df['duration_sec'] >= duration_range[0]) & (df['duration_sec'] <= duration_range[1]) &
        (df['volume_db'] >= volume_range[0]) & (df['volume_db'] <= volume_range[1]) &
        (df['file_type'].isin(file_type_filter)) &
        (df['ha_type'].isin(ha_type_filter)) &
        (df['mic_position'].isin(mic_position_filter)) &
        (df['wola_type'].isin(wola_type_filter)) &
        (df['Receiver'].isin(rec_position_filter))
        ]

    return filtered_df
# -----------------------------
# Initialize Session State
# -----------------------------
if "projects" not in st.session_state:
    st.session_state.projects = {
        "Project Alpha": {"owner": "Simona Lisker", "date": datetime.date(2025, 10, 20)},
        "Project Beta": {"owner": "John Doe", "date": datetime.date(2025, 10, 21)}
    }
if "upload_metadata" not in st.session_state:
    st.session_state.upload_metadata = {"project": "", "owner": "", "date": datetime.date.today()}
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "download_filters" not in st.session_state:
    st.session_state.download_filters = {
        # "search_term": "",
        # "hearing_filter": "all",
        # "ha_type_filter": [],
        # "mic_position_filter": [],
        # "rec_position_filter": [],
        # "duration_range": (0, 60),
        # "volume_range": (-48.0, -13.0),
        # "file_type_filter": [],
        # "wola_type_filter": []
    }


# -----------------------------
# Simulated Metadata
# -----------------------------
# data = {
#     'filename': [f"audio_{i}.wav" for i in range(1, 21)],
#     'duration_sec': np.random.randint(0, 61, 20),
#     'channel': np.random.choice(['RIC Micro', 'RIC Macro', 'ITE', 'ITC', 'CIC'], 20),
#     'hearing_aid': np.random.choice(['yes', 'no'], 20),
#     'volume_db': np.random.uniform(-48, -13, 20),
#     'upload_date': [datetime.date.today() - datetime.timedelta(days=i) for i in range(20)],
#     'audiogram_gains': [np.random.randint(-97, 32, 24).tolist() for _ in range(20)],
#     'file_type': np.random.choice(['pcm', 'wav'], 20),
#     'ha_type': np.random.choice(['Blane', 'Genesis', 'Afton'], 20),
#     'mic_position': np.random.choice(['front', 'rear', 'inward'], 20),
#     'Receiver': np.random.choice(['yes', 'no'], 20),
#     'wola_type': np.random.choice([64, 16], 20)
# }
#df = pd.DataFrame(data)
df = load_audio_metadata("audio_metadata_updated.csv")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Audio Dataset Management", layout="wide")
st.title("🎵 Audio Dataset Management System")


# Update upload metadata
#st.session_state.upload_metadata.update({"project": selected_project, "owner": owner_display, "date": date_display})

# -----------------------------
# Tabs
# -----------------------------
tab_project, tab_upload, tab_download = st.tabs(["📂 Project Management", "📤 Upload Audio Files", "📥 Build & Export Dataset"])
# Initialize filtered_df as an empty DataFrame with the same columns as df
filtered_df = pd.DataFrame(columns=df.columns)
# Ensure `active_tab` is set in session state
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "📁 Project Management"  # Default tab

# Sidebar filters
if st.session_state.get("active_tab") != "📤 Build & Export Dataset":
    st.sidebar.header("Project Selection")
    selected_project = st.sidebar.selectbox("Select Project", list(st.session_state.projects.keys()))
    owner_display = st.session_state.projects[selected_project]["owner"]
    date_display = st.session_state.projects[selected_project]["date"]
    st.sidebar.write(f"Owner: {owner_display}")
    st.sidebar.write(f"Date: {date_display}")
    filtered_df = sideBar(st)

# -----------------------------
# Project Management Tab
# -----------------------------
with tab_project:
    st.session_state["active_tab"] = "📁 Project Management"
    st.header("Manage Projects")

    st.subheader("Add New Project")
    st.markdown("Use this section to add a new project to the system.")
    new_name = st.text_input("Project Name", key="new_project_name")
    new_owner = st.text_input("Owner", key="new_project_owner")
    new_date = st.date_input("Date", datetime.date.today(), key="new_project_date")
    if st.button("Add Project"):
        if new_name and new_owner:
            st.session_state.projects[new_name] = {"owner": new_owner, "date": new_date}
            st.success(f"✅ Project '{new_name}' added successfully!")
        else:
            st.error("⚠️ Please provide both Project Name and Owner.")

    # System Design Image
    st.sidebar.header("System Architecture")
    st.sidebar.image("Architecture.png", caption="System Architecture Overview", width=400)
    st.subheader("Existing Projects")
    for name, info in st.session_state.projects.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{name}** | Owner: {info['owner']} | Date: {info['date']}")
        with col2:
            if st.button("Delete", key=f"delete_{name}"):
                #del st.session_state.projects[name]
                #st.experimental_rerun()
                st.warning("⚠️ Project deletion is disabled in this demo.")

# -----------------------------
# Upload Tab
# -----------------------------
with tab_upload:
    st.header("Upload Audio Files")
    st.session_state["active_tab"] = "📤 Upload Audio Files"

    st.write(f"Selected Project: **{selected_project}** | Owner: {owner_display} | Date: {date_display}")

    uploaded_files = st.file_uploader("Upload audio files (WAV/PCM)", type=["wav", "pcm"], accept_multiple_files=True)

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

        # Progress bar simulation
        st.info("Processing files...")
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1)

        # Audio preview
        st.subheader("🎧 Preview Uploaded Files")
        for file in uploaded_files:
            st.audio(file, format="audio/wav")


# -----------------------------
# Download Tab
# -----------------------------
with tab_download:
    st.header("Build & Export Dataset")
    st.session_state["active_tab"] = "📥 Build & Export Dataset"
    st.markdown(f"**Project Info:** {selected_project} | Owner: {owner_display} | Date: {date_display}")
    # Sidebar filters
    #filtered_df = sideBar(st)
    # Filters
    #st.sidebar.header("Filter Options")
    f = st.session_state.download_filters
    # Audiogram Gain Selector inside an expander
    with st.expander("🎚️ Audiogram Gain Selector", expanded=False):
        st.markdown("Adjust 24 frequency band gains:")
        cols = st.columns(24)
        audiogram_gains = []
        for i in range(24):
            with cols[i]:
                default_value = random.randint(-97, 31)
                gain = st.slider(f"{i + 1}", -97, 31, default_value)
                audiogram_gains.append(gain)
        st.write(f"Selected Gains: {audiogram_gains}")
    # Summary Card
    st.subheader("📊 Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", len(filtered_df))
    col2.metric("Avg Duration (sec)", round(filtered_df['duration_sec'].mean(), 2))
    col3.metric("Avg Volume (dB)", round(filtered_df['volume_db'].mean(), 2))

    # Charts
    st.subheader("Category Distributions")
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        st.write("Channel Distribution")
        st.bar_chart(filtered_df['channel'].value_counts())
    with chart_col2:
        st.write("Hearing Aid Distribution")
        st.bar_chart(filtered_df['hearing_aid'].value_counts())
    with chart_col3:
        st.write("Duration Distribution")
        st.bar_chart(filtered_df['duration_sec'].value_counts().sort_index())
    downloadFilesToServer()
    # Matching Files with Audio Icon
    st.subheader("Matching Files")
    for _, row in filtered_df.iterrows():
        col_file, col_icon = st.columns([4, 1])
        with col_file:
            st.write(f"**{row['filename']}** - Duration: {row['duration_sec']} sec, Volume: {row['volume_db']:.1f} dB")
        with col_icon:
            if st.button("▶", key=row['filename']):
                sr = 16000
                t = np.linspace(0, 5, sr * 5)
                tone = 0.5 * np.sin(2 * np.pi * random.randint(200, 800) * t)
                buffer = BytesIO()
                sf.write(buffer, tone, sr, format='WAV')
                st.audio(buffer.getvalue(), format="audio/wav")

