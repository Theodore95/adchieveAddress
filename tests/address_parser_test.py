import unittest 
import sys

sys.path.append("..")
from src.address_parser import parse_file, split_address


ADDRESS_1 = "Adchieve HQ - Sint Janssingel 92, 5211 DA 's-Hertogenbosch, The Netherlands"
ADDRESS_2 = "Eastern Enterprise - 46/1 Office no 1 Ground Floor , Dada House , Inside dada silk mills"
ADDRESS_WITHOUT_HYPHEN = "Neverland, 5225 Figueroa Mountain Road, Los Olivos, Calif. 93441, USA"

ADDRESS_LIST = ["Adchieve HQ - Sint Janssingel 92, 5211 DA 's-Hertogenbosch, The Netherlands", 
                "Eastern Enterprise - 46/1 Office no 1 Ground Floor , Dada House , Inside dada silk mills"]
ADDRESSES_FILEPATH = "tests/resources/addresses_reduced.txt"

class TestAddressParsing(unittest.TestCase):
    """
    Tests the parse_file and split_string functions in address_parser.
    """
    def test_parse_file(self):
        res = parse_file(ADDRESSES_FILEPATH)
        self.assertEqual(ADDRESS_LIST, res)

    def test_split_string(self):
       res = split_address(ADDRESS_1, " - ")
       print(res)
       self.assertEqual(("Adchieve HQ", "Sint Janssingel 92, 5211 DA 's-Hertogenbosch, The Netherlands"), res)

    def test_split_string_without_hyphen(self):
       res = split_address(ADDRESS_WITHOUT_HYPHEN, " - ")
       self.assertEqual(("Neverland, 5225 Figueroa Mountain Road, Los Olivos, Calif. 93441, USA", ""), res)


if __name__ == "__main__":
  unittest.main()