from geopy.distance import geodesic

def is_within_radius(job_location, user_coords, radius_km=20):
    job_coords = (job_location.latitude, job_location.longitude)
    return geodesic(user_coords, job_coords).km <= radius_km
