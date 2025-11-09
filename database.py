# database.py
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import streamlit as st

@st.cache_resource
def init_connection() -> Client:
    """Initializes a connection to the Supabase client."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_equipment_locations(db_client: Client):
    """Fetches equipment and their static locations."""
    try:
        response = db_client.table('equipment').select('id, latitude, longitude').execute()
        return {item['id']: {'lat': item['latitude'], 'lon': item['longitude']} for item in response.data}
    except Exception as e:
        st.error(f"Error fetching equipment locations: {e}")
        return {}

def get_certified_employees(db_client: Client, certification: str):
    """Finds employees with a specific certification."""
    try:
        response = db_client.table('employees').select('id, name').filter('certifications', 'cs', f"{{{certification}}}").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching employees: {e}")
        return []

def get_latest_employee_location(db_client: Client, employee_id: int):
    """Gets the most recent known location for a single employee."""
    try:
        response = db_client.table('employee_locations') \
            .select('latitude, longitude') \
            .eq('employee_id', employee_id) \
            .order('timestamp', desc=True) \
            .limit(1) \
            .single() \
            .execute()
        return response.data
    except Exception as e:
        # This can fail if no location data exists yet, which is fine
        return None