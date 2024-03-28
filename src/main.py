import address_parser, location, yaml, csv
from geocoding_clients import positionstack_client, geocoding_clientABC

with open("resources/configuration.yaml") as config_file:
  config_data = yaml.safe_load(config_file)

API_ENDPOINT = config_data["api_endpoint"]
ACCESS_KEY = config_data["access_key"]

ADDRESS_FILEPATH = config_data["address_file"]
NAME_ADDRESS_SEPERATOR = config_data["name_address_seperator"]
CSV_FILEPATH = config_data["csv_file"]

def geocode_provider_factory() -> geocoding_clientABC.GeocodingClient:
    if API_ENDPOINT == "api.positionstack.com":
       return positionstack_client.PositionstackClient(API_ENDPOINT, ACCESS_KEY)
    else:
       raise TypeError("API client for given API provider is not defined")
 

def query_addresses() -> list[tuple[str, list[dict]]]:
    """
    Parses address file and performs query to geocode API providor.

    Returns:
        A list of tuples, with the left indice the name as specified in the address file,
        and the right indice the result of the query. 
    """
    address_list: list[str] = address_parser.parse_file(ADDRESS_FILEPATH)
    positionstack = geocode_provider_factory()
    geolocation_list = []
    for address in address_list:
        split_address_and_name = address_parser.split_address(address, NAME_ADDRESS_SEPERATOR)

        # If address did not contain " - " to seperate name from address, use entire address line to perform query
        split_address = split_address_and_name[1] if split_address_and_name[1] != "" else split_address_and_name[0]
        geocode_data = positionstack.forward_geocoding_address(split_address).get("data")
        
        #if no results from API provider were given do not add to list
        if len(geocode_data) != 0:  
           geolocation_list.append((split_address_and_name[0], positionstack.forward_geocoding_address(split_address).get("data")))
    return geolocation_list

def format_geolocations(geolocation_list: list[tuple[str, list[dict]]]) -> list[location.location]:
    """
    Creates location objects from the results returned by API provider. 

    Returns:
        A list consisting of location objects containing the needed information retrieved from API provider. 
    """
    locations = []
    for address, geocode_data in geolocation_list:
        label = geocode_data[0].get("label")
        latitude = geocode_data[0].get("latitude")
        longitude = geocode_data[0].get("longitude")
        loc = location.location(address, label, latitude, longitude)
        locations.append(loc)
    return locations

def print_locations(locations: list[location.location]):
    locations.sort(key=sort_by_km)
    for loc in locations:
        print(loc)

def sort_by_km(loc: location):
    return loc.distance

def export_csv(locations: list[location.location], filepath: str) -> None:
  with open(filepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    i = 1
    for location in locations:
       writer.writerow([i] + location.to_list())
       i = i + 1

def main():
   geolocation_list = query_addresses()
   location_list = format_geolocations(geolocation_list)
   print_locations(location_list)
   export_csv(location_list, CSV_FILEPATH)

if __name__ == "__main__":
  main()