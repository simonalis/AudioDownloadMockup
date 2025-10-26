import pandas as pd

def load_audio_metadata(csv_path="audio_metadata.csv"):
    df = pd.read_csv(csv_path)
    return df

def filter_audio_metadata(
    df,
    hearing_filter,
    duration_range,
    volume_range,
    file_type_filter,
    ha_type_filter,
    mic_position_filter,
    rec_position_filter,
    wola_type_filter,
    channel_filter
):
    filtered_df = df[
        (df['hearing_aid'].isin([hearing_filter])) &
        (df['duration_sec'] >= duration_range[0]) & (df['duration_sec'] <= duration_range[1]) &
        (df['volume_db'] >= volume_range[0]) & (df['volume_db'] <= volume_range[1]) &
        (df['file_type'].isin(file_type_filter)) &
        (df['ha_type'].isin(ha_type_filter)) &
        (df['mic_position'].isin(mic_position_filter)) &
        (df['Receiver'].isin(rec_position_filter)) &
        (df['wola_type'].isin(wola_type_filter)) &
        (df['channel'].isin(channel_filter))
    ]
    return filtered_df
