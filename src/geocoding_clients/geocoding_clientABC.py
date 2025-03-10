from abc import ABC, abstractmethod

class GeocodingClient(ABC):

    """Interface for forward geocoding using only address as query"""
    @abstractmethod
    def forward_geocoding_address(self, address: str) -> dict:
        pass

    """Interface for forward geocoding where both name and associated address are given"""
    @abstractmethod
    def forward_geocoding_name_and_region(self, location_name: str, region: str) -> dict:
        pass

        