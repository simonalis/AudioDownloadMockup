
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time  # <-- add this line

from audio_data_utils import load_audio_metadata

# Simulated metadata for demonstration
data = {
    'filename': [f"audio_{i}.wav" for i in range(1, 21)],
    'duration_sec': np.random.randint(0, 61, 20),
    'channel': np.random.choice(['RIC Micro', 'RIC Macro', 'ITE', 'ITC','CIC'], 20),
    'hearing_aid': np.random.choice(['yes', 'no'], 20),
    'volume_db': np.random.uniform(-48, -13, 20),
    'upload_date': [datetime.date.today() - datetime.timedelta(days=i) for i in range(20)],
    'audiogram_gains': [np.random.randint(-97, 32, 24).tolist() for _ in range(20)],
    'file_type': np.random.choice(['pcm', 'wav'], 20),
    'ha_type': np.random.choice(['Blane', 'Genesis', 'Afton'], 20),
    'mic_position': np.random.choice(['front', 'rear', 'inward'], 20),
    'Receiver': np.random.choice(['yes', 'no'], 20),
    'wola_type': np.random.choice([64, 16], 20)
}
df = pd.DataFrame(data)
df = load_audio_metadata("audio_metadata_updated.csv")

st.set_page_config(page_title="Audio Dataset Dashboard", layout="wide")
st.title("Audio Dataset Dashboard")

st.sidebar.header("Filter Options")
search_term = st.sidebar.text_input("Search by filename")
hearing_filter = st.sidebar.selectbox("Hearing Aid", options=['yes', 'no'], index=1)
if hearing_filter == 'yes':
    ha_type_filter = st.sidebar.multiselect("Hearing Aid HW", options=df['ha_type'].unique(), default=df['ha_type'].unique())
    mic_position_filter = st.sidebar.multiselect("Microphone", options=df['mic_position'].unique(), default=df['mic_position'].unique())
    rec_position_filter = st.sidebar.multiselect("Receiver", options=df['Receiver'].unique(), default=df['Receiver'].unique())
else:
    ha_type_filter = df['ha_type'].unique()
    mic_position_filter = df['mic_position'].unique()
    rec_position_filter = df['Receiver'].unique()
    cchannel_filter = df['channel'].unique()

duration_range = st.sidebar.slider("Duration (sec)", 0, 60, (0, 60))
volume_range = st.sidebar.slider("Volume (dB)", float(df['volume_db'].min()), float(df['volume_db'].max()), (float(df['volume_db'].min()), float(df['volume_db'].max())))
file_type_filter = st.sidebar.multiselect("File Type", options=df['file_type'].unique(), default=df['file_type'].unique())

wola_type_filter = st.sidebar.multiselect("WOLA Type", options=df['wola_type'].unique(), default=df['wola_type'].unique())
# Audiogram gain filter only if HA is 'yes'
# if hearing_filter == 'yes':
#     st.sidebar.markdown("**Audiogram Gain Selector**")
#     low_gain = st.sidebar.slider("Low Frequency Gain", -97, 31, 0)
#     mid_gain = st.sidebar.slider("Mid Frequency Gain", -97, 31, 0)
#     high_gain = st.sidebar.slider("High Frequency Gain", -97, 31, 0)

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

import random
# Add the architecture image to the Streamlit app
st.sidebar.header("System Architecture")
st.sidebar.image("architecture.jpeg", caption="System Architecture Overview", width=400)

with st.expander("🎚️ Audiogram Gain Selector"):
    st.markdown("Adjust 24 frequency band gains:")

    # Create 24 columns in one horizontal line
    cols = st.columns(24)

    # Store gains in a list
    audiogram_gains = []

    # Loop through 24 sliders, one per column
    for i in range(24):
        with cols[i]:
            default_value = random.randint(-97, 31)
            gain = st.slider(f"{i+1}", -97, 31, default_value)
            audiogram_gains.append(gain)

    st.write(f"Selected Gains: {audiogram_gains}")


# Top distributions
st.subheader("Category Distributions")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Channel Distribution**")
    st.bar_chart(filtered_df['channel'].value_counts())
with col2:
    st.write("**Hearing Aid Distribution**")
    st.bar_chart(filtered_df['hearing_aid'].value_counts())
with col3:
    st.write("**Duration Distribution**")
    st.bar_chart(filtered_df['duration_sec'].value_counts().sort_index())
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 400px;  /* Adjust the width as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.header("📡 Remote Server File Copy (Demo)")

# Connection fields
with st.form("remote_server_form"):
    st.subheader("Connect to Remote Server")
    server = st.text_input("Server Address (e.g., 192.168.1.10 or example.com)")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    destination_dir = st.text_input("Destination Directory (on remote server)")
    submitted = st.form_submit_button("Connect")

if submitted:
    if server and username and password:
        st.success(f"✅ Connected to {server} as {username} (demo mode)")
    else:
        st.error("⚠️ Please fill in all connection fields.")

# Simulate file copying
if st.button("Copy Matching Files (Demo)"):
    if not (server and username and password):
        st.warning("Please connect to the remote server first.")
    elif not destination_dir:
        st.warning("Please specify a destination directory.")
    else:
        st.info(f"Starting copy to {destination_dir} on {server}...")
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.03)  # simulate work
            progress_bar.progress(percent_complete + 1)
        st.success("✅ Files copied successfully (demo only)")
# Summary metrics
st.metric("Total Files", len(filtered_df))
st.metric("Average Duration (sec)", round(filtered_df['duration_sec'].mean(), 2))
st.metric("Average Volume (dB)", round(filtered_df['volume_db'].mean(), 2))

# Matching files
st.subheader("Matching Files")
for _, row in filtered_df.iterrows():
    st.write(f"**{row['filename']}** - Duration: {row['duration_sec']} sec, Volume: {row['volume_db']:.1f} dB")

