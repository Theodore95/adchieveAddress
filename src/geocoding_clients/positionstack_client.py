import http.client, urllib.parse, json
from geocoding_clients import geocoding_clientABC

# The http path for the "forward" operation of stackpoint API
FORWARD_PATH = "/v1/forward?"

class PositionstackClient(geocoding_clientABC.GeocodingClient):

  def __init__(self, api_endpoint: str, access_key: str):
    self.api_endpoint = api_endpoint
    self.access_key = access_key
    self.conn = http.client.HTTPConnection(api_endpoint)
  
  def forward_geocoding_address(self, address: str) -> dict:
    params = urllib.parse.urlencode({
      'access_key': self.access_key,
      'query': address,
      'limit': 1,
      })
    self.conn.request('GET', FORWARD_PATH + params)
    
    res = self.conn.getresponse()
    data = res.read().decode('utf-8')
    return json.loads(data)

  def forward_geocoding_name_and_region(self, location_name: str, region: str) -> dict:
    params = urllib.parse.urlencode({
      'access_key': self.access_key,
      'query': location_name,
      'region': region,
      'limit': 1,
      })
    self.conn.request('GET', FORWARD_PATH + params)
    
    res = self.conn.getresponse()
    data = res.read().decode('utf-8')
    return json.loads(data)