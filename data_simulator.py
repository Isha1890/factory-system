import pandas as pd
import numpy as np
import os

def generate_factory_data(output_file='data/factory_data.csv'):
    # ... (Copy the factory data generation logic for PUMP-101 from the previous guide) ...
    records = 200
    time = pd.to_datetime(np.arange(records), unit='m', origin=pd.Timestamp('2023-10-26 08:00:00'))
    vibration = np.random.normal(loc=2.5, scale=0.5, size=records)
    vibration[100:110] = np.random.normal(loc=6.5, scale=0.8, size=10)
    df = pd.DataFrame({'timestamp': time, 'equipment_id': 'PUMP-101', 'metric_name': 'vibration_mm_s', 'value': vibration})
    df.to_csv(output_file, index=False)
    print(f"Factory sensor data saved to {output_file}")

def generate_employee_location_data(output_file='data/employee_locations.csv'):
    # Simulate Kiana-like location data for our 3 employees
    num_records = 300
    timestamps = pd.to_datetime(np.arange(num_records), unit='s', origin=pd.Timestamp('2023-10-26 08:00:00'))
    
    # Base location within the Kiana data range
    base_lat, base_lon = 51.4605, -0.9328
    
    dfs = []
    for emp_id in [1, 2, 3]: # Corresponds to John, Jane, Peter
        lat_walk = base_lat + np.random.randn(num_records) * 0.0001
        lon_walk = base_lon + np.random.randn(num_records) * 0.0001
        df = pd.DataFrame({
            'timestamp': timestamps,
            'employee_id': emp_id,
            'latitude': lat_walk,
            'longitude': lon_walk
        })
        dfs.append(df)
        
    final_df = pd.concat(dfs).sort_values(by='timestamp')
    final_df.to_csv(output_file, index=False)
    print(f"Simulated employee location data saved to {output_file}")

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    generate_factory_data()
    generate_employee_location_data()