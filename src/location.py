
import yaml
from geopy.distance import geodesic

with open("src/resources/configuration.yaml") as config_file:
  config_data = yaml.safe_load(config_file)

ADCHIEVE_LATITUDE = config_data["epicenter"]["latitude"]
ADCHIEVE_LONGITUDE = config_data["epicenter"]["longitude"]

class location():
    def __init__ (self, name: str, address: str, latitude: float, longitude: float):
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.coord = (latitude, longitude)
        self.distance = self.distance_from_epicenter()

    
    def distance_from_epicenter(self) -> float:
        adchieve_coord = (ADCHIEVE_LATITUDE, ADCHIEVE_LONGITUDE)
        return geodesic(adchieve_coord, self.coord).km
    
    def to_list(self) -> list:
        return [f"{self.distance_from_epicenter():.2f} km", f"{self.name}", f"{self.address}"]  
    

    def __str__(self):
        return f"{self.distance_from_epicenter():.2f} km, {self.name}, {self.address}"

    
