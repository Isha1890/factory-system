import streamlit as st
import pandas as pd
import time
from config import ANOMALY_THRESHOLDS
from database import init_connection, get_equipment_locations
from rag_core import initialize_rag_pipeline, get_rag_solution
from personnel_finder import find_nearest_eligible_employee

st.set_page_config(layout="wide")

# --- INITIALIZATION ---
db_client = init_connection()
rag_chain = initialize_rag_pipeline()
equipment_locations = get_equipment_locations(db_client)
factory_df = pd.read_csv('data/factory_data.csv', parse_dates=['timestamp'])

# --- LIVE LOCATION SIMULATOR ---
# In a real app, this would be a separate microservice.
# Here, we'll simulate it by updating the DB every few seconds.
location_df = pd.read_csv('data/employee_locations.csv', parse_dates=['timestamp'])
if 'location_index' not in st.session_state:
    st.session_state.location_index = 0

def update_live_locations():
    idx = st.session_state.location_index
    # Push next 5 location updates to DB
    for _, row in location_df.iloc[idx:idx+5].iterrows():
        db_client.table('employee_locations').insert({
            'employee_id': row['employee_id'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'timestamp': row['timestamp'].isoformat()
        }).execute()
    st.session_state.location_index = (idx + 5) % len(location_df)

# --- UI ---
st.title("🛡️ Capstone: Intelligent Factory Operations Dashboard")
st.sidebar.success("Connected to Supabase DB ✅")
st.sidebar.info("Running Ollama LLM locally 🧠")

selected_equipment = "PUMP-101" # Hardcoded for this specific project
st.header(f"Live Status: {selected_equipment}")

# Chart and Alert placeholders
chart = st.line_chart()
alert_placeholder = st.empty()
tech_placeholder = st.empty()
solution_placeholder = st.empty()

# Simulation loop
for i in range(1, len(factory_df)):
    live_df = factory_df.iloc[0:i]
    latest_value = live_df['value'].iloc[-1]
    
    chart.add_rows(live_df.set_index('timestamp').iloc[i-1:i])
    
    threshold = ANOMALY_THRESHOLDS[selected_equipment]['vibration_mm_s']
    
    if latest_value > threshold:
        problem_desc = f"Critical vibration on {selected_equipment} ({latest_value:.2f} mm/s)."
        alert_placeholder.error(problem_desc)
        
        with tech_placeholder.container():
            with st.spinner("Anomaly detected! Finding nearest certified technician..."):
                update_live_locations() # Ensure latest location data is in DB
                time.sleep(2) # Dramatic pause
                technician, message = find_nearest_eligible_employee(
                    db_client,
                    equipment_locations[selected_equipment],
                    "Pump Maintenance"
                )
                if technician:
                    st.success(f"✅ **Technician Found:** {technician['name']} is approx. **{technician['distance_meters']}m** away.")
                else:
                    st.warning(f"⚠️ {message}")
        
        with solution_placeholder.container():
            if st.button("Generate AI-Powered Solution"):
                with st.spinner("Consulting manuals..."):
                    solution = get_rag_solution(rag_chain, problem_desc)
                    st.subheader("🔧 Recommended Action Plan")
                    st.markdown(solution)
        st.stop()
            
    else:
        alert_placeholder.info(f"Monitoring... Current vibration: {latest_value:.2f} mm/s")

    # Update live locations in the background
    if i % 10 == 0:
        update_live_locations()

    time.sleep(0.05)