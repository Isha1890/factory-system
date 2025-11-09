# personnel_finder.py
from database import get_certified_employees, get_latest_employee_location
from haversine import haversine, Unit

def find_nearest_eligible_employee(db_client, equipment_location, required_certification):
    """
    Finds the closest employee who is certified to handle the job.
    1. Gets all employees with the right certification.
    2. For each, gets their latest known location.
    3. Calculates distance and finds the minimum.
    """
    certified_employees = get_certified_employees(db_client, required_certification)
    if not certified_employees:
        return None, "No employees found with the required certification."

    closest_employee = None
    min_distance = float('inf')

    for emp in certified_employees:
        location_data = get_latest_employee_location(db_client, emp['id'])
        if location_data:
            emp_location = (location_data['latitude'], location_data['longitude'])
            equipment_coords = (equipment_location['lat'], equipment_location['lon'])
            
            distance = haversine(emp_location, equipment_coords, unit=Unit.METERS)
            
            if distance < min_distance:
                min_distance = distance
                closest_employee = {
                    "name": emp['name'],
                    "distance_meters": round(distance)
                }

    if closest_employee:
        return closest_employee, f"Found {closest_employee['name']} approximately {closest_employee['distance_meters']}m away."
    else:
        return None, "Certified employees found, but no location data is available for them."