import address_parser, location, yaml, csv
from geocoding_clients import positionstack_client 

with open("src/resources/configuration.yaml") as config_file:
  config_data = yaml.safe_load(config_file)

API_ENDPOINT = config_data["api_endpoint"]
ACCESS_KEY = config_data["access_key"]
FORWARD_GEOCODE_PATH = config_data["forward_geocode_path"]

ADDRESS_FILEPATH = config_data["address_file"]
CSV_FILEPATH = config_data["csv_file"]

def query_addresses() -> list[dict]:
    address_list: list[str] = address_parser.parse_file(ADDRESS_FILEPATH)
    positionstack = positionstack_client.PositionstackClient(API_ENDPOINT, ACCESS_KEY) 
    geolocation_list = []
    for address in address_list:
        split_address_and_name = address_parser.split_address(address, " - ")
        split_address = split_address_and_name[1] if split_address_and_name[1] != "" else split_address_and_name[0]
        geolocation_list += positionstack.forward_geocoding_address(FORWARD_GEOCODE_PATH, split_address).get("data")
    return geolocation_list

def format_geolocations(geolocation_list: list[dict]) -> list[location.location]:
    locations = []
    for entry in geolocation_list:
        loc = location.location(entry.get("name"), entry.get("label"), entry.get("latitude"), entry.get("longitude"))
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

# # ADDRESS_1 = "Adchieve HQ - Sint Janssingel 92, 5211 DA 's-Hertogenbosch, The Netherlands"

# positionstackClient = positionstack_client.PositionstackClient(API_ENDPOINT, ACCESS_KEY)
# # address_location_split = address_parser.split_address(ADDRESS_1, " - ")

# list_of_addresses: list[str] = address_parser.parse_file(ADDRESS_FILEPATH)
# # print(list_of_addresses)

# list_geolocations = []
# for address in list_of_addresses:
#     #TODO only use latter part of address for query
#     # list_geolocations += positionstackClient.forward_geocoding(FORWARD_GEOCODE_PATH, address_location_split[0], address_location_split[1]).get("data")
#     # geolocation = positionstackClient.forward_geocoding(FORWARD_GEOCODE_PATH, address_location_split[0], address_location_split[1]).get("data")
#     print(address)
#     split_address_and_name = address_parser.split_address(address, " - ")
#     split_address = split_address_and_name[1] if split_address_and_name[1] != "" else split_address_and_name[0]
#     list_geolocations += positionstackClient.forward_geocoding_query(FORWARD_GEOCODE_PATH, split_address).get("data")
#     # print(address)
  
#     # print(geolocation)
#     # loc = location.location(geolocation.get("name"), geolocation.get("label"), geolocation.get("latitude"), geolocation.get("longitude"))
#     # list_geolocations.append(loc)

# # print(list_geolocations)



# locations = []
# for entry in list_geolocations:
#     # print(geolocation)

#         loc = location.location(entry.get("name"), entry.get("label"), entry.get("latitude"), entry.get("longitude"))
#         locations.append(loc)
#     #TODO use first part of address for "name"
#     # for entry in geolocation[1]:
#     #     print(entry)
#     #     loc = location.location(geolocation[0], entry.get("label"), entry.get("latitude"), entry.get("longitude"))
#     #     locations.append(loc)

# # print(locations)
# def sort_by_km(loc: location):
#      return loc.distance

# locations.sort(key=sort_by_km)
# # sort(locations)       
# for loc in locations:
#     print(loc)
# print(locations)







# print(list_geolocations)
# print(positionstackClient.forward_geocoding(FORWARD_GEOCODE_PATH, address_location_split[0], address_location_split[1]))

# positionstack_client.



# print("Hello world")

# import http.client, urllib.parse

# conn = http.client.HTTPConnection('api.positionstack.com')

# params = urllib.parse.urlencode({
#     'access_key': '9eb61b6aa98a57d4201f19b0253c92aa',
#     'query': "Adchieve HQ - Sint Janssingel 92, 5211 DA 's-Hertogenbosch",
#     'region': 'The Netherlands',
#     'limit': 1,
#     })

# conn.request('GET', '/v1/forward?{}'.format(params))

# res = conn.getresponse()
# data = res.read()

# print(data.decode('utf-8'))






# API_ENDPOINT = 'api.positionstack.com'
# ACCESS_KEY = '9eb61b6aa98a57d4201f19b0253c92aa'

# import http.client, urllib.parse

# conn = http.client.HTTPConnection(API_ENDPOINT)

# params = urllib.parse.urlencode({
#     'access_key': ACCESS_KEY,
#     'query': 'Eastern Enterprise B.V.',
#     'region': 'Hengelo, The Netherlands',
#     })

# conn.request('GET', '/v1/forward?{}'.format(params))

# res = conn.getresponse()
# data = res.read()

# print(data.decode('utf-8'))