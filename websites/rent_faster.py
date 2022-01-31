# Python Packages
import os
import math
import json
import requests
import pandas as pd
from enum import Enum
from multiprocessing.dummy import Pool, Manager

MANAGER = Manager()
LISTINGS = MANAGER.list()


def filter_to_json(filter, filename='filter.json'):
    for key, value in filter.items():
        if (value is not None) and (type(value) is not int) and (type(value[0]) is not str):
            filter[key] = [enum.get_formatted() for enum in value]
        elif value is int:
            filter[key] = value
    with open(filename, 'w') as file:
        json.dump(filter, file, indent=4)


def request_properties(search_url, prop_filter, listings, page=0):
    url = search_url + prop_filter + f'cur_page={page}'
    url_response = requests.get(url)
    json_data = url_response.json()
    listings.extend([Listing(**listing) for listing in json_data['listings']])


def make_filter(property_type: list = None,
                beds: list = None,
                baths: list = None,
                utilities_included: list = None,
                furnishing: list = None,
                pet: list = None,
                smoking: list = None,
                parking: list = None,
                price_from: int = 0,
                price_to: int = 10000,
                home_features: list = None,
                availability: list = None,
                neighborhood: list = None,
                save=False,
                filename='filter.json'):
    filter = {
        'property_type': property_type,
        'beds': beds,
        'baths': baths,
        'utilities_included': utilities_included,
        'furnishing': furnishing,
        'pet': pet,
        'smoking': smoking,
        'parking': parking,
        'price_from': price_from,
        'price_to': price_to,
        'home_features': home_features,
        'availability': availability,
        'neighborhood': neighborhood
    }
    if save:
        filter_to_json(filter, filename)
    return filter


class CITY_ID(Enum):
    CALGARY = 1
    AIRDRIE = 8
    RED_DEER = 7458
    EDMONTON = 2
    FORT_MCMURRAY = 3114
    REGINA = 3
    SASKATOON = 4
    WINNIPEG = 5
    TORONTO = 7
    MISSISSAUGA = 139
    OTTAWA = 149
    MONTREAL = 10143
    FREDERICTON = 3191
    HALIFAX = 10140
    CHARLOTTETOWN = 1726
    ST_JOHNS = 8740
    VANCOUVER = 6
    VICTORIA = 97
    KELOWNA = 4435

    def get_formatted(self):
        return self.name.capitalize()

    @classmethod
    def from_formatted(cls, formatted: str):
        return cls[formatted.upper()]


class FilterFields:
    class TYPE(Enum):
        APARTMENT = "Apartment"
        CONDO = "Condo"
        LOFT = "Loft"
        HOUSE = "House"
        TOWNHOUSE = "Townhouse"
        DUPLEX = "Duplex"
        MAIN_FLOOR = "Main Floor"
        BASEMENT = "Basement"
        SHARED = "Shared"
        MOBILE = "Mobile"
        ACREAGE = "Acreage"
        OFFICE_SPACE = "Office Space"
        PARKING_SPOT = "Parking Spot"
        STORAGE = "Storage"
        VACATION = "Vacation"

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((prop_type for prop_type in cls if prop_type.value == formatted), None)

    class BEDS(Enum):
        BACHELOR = 'bachelor'
        ONE = '1'
        ONE_PLUS_DEN = '1 + Den'
        TWO = '2'
        TWO_PLUS_DEN = '2 + Den'
        THREE = '3'
        THREE_PLUS_DEN = '3 + Den'
        FOUR = '4'
        FOUR_PLUS_DEN = '4 + Den'
        SIX = '6'
        SEVEN = '7'
        EIGHT = '8'
        NINE = '9'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((bed for bed in cls if bed.value == formatted), None)

    class BATHS(Enum):
        ONE = '1'
        ONE_AND_HALF = '1.5'
        TWO = '2'
        TWO_AND_HALF = '2.5'
        THREE_PLUS = '3+'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((bath for bath in cls if bath.value == formatted), None)

    class UTILITIES(Enum):
        HEAT = 'Heat'
        ELECTRICITY = 'Electricity'
        WATER = 'Water'
        CABLE = 'Television'
        INTERNET = 'Internet'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((bath for bath in cls if bath.value == formatted), None)

    class FURNISHING(Enum):
        UNFURNISHED = 'Unfurnished'
        FURNISHED = 'Furnished'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((furnishing for furnishing in cls if furnishing.value == formatted), None)

    class PETS(Enum):
        CATS = 'Cats'
        DOGS = 'Dogs'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((pet for pet in cls if pet.value == formatted), None)

    class SMOKING(Enum):
        NON_SMOKING = 'Non-Smoking'
        SMOKING = 'Smoking'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((smoking for smoking in cls if smoking.value == formatted), None)

    class PARKING(Enum):
        GARAGE_SINGLE = 'Garage Single'
        GARAGE_DOUBLE = 'Garage Double'
        GARAGE_TRIPLE = 'Garage Triple'
        UNDERGROUND = 'Underground'
        COVERED = 'Covered'
        OUTDOOR = 'Outdoor'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((parking for parking in cls if parking.value == formatted), None)

    class HOME_FEATURES(Enum):
        RENT_TO_OWN = 'Rent-to-Own'
        CORNER_UNIT = 'Corner Unit'
        PENTHOUSE_UNIT = 'Penthouse Unit'
        DISHWASHER = 'Dishwasher'
        LAUNDRY_IN_SUITE = 'Laundry - In Suite'
        LAUNDRY_COIN_CARD = 'Laundry - Coin/Card'
        LAUNDRY_SHARED = 'Laundry - Shared'
        AIR_CONDITIONING = 'Air Conditioning'
        FIREPLACE = 'Fireplace'
        JETTED_TUB_JACUZZI = 'Jetted Tub/Jacuzzi'
        HARDWOOD_FLOORS = 'Hardwood Floors'
        LAMINATE_FLOORS = 'Laminate Floors'
        TILE_FLOORING = 'Tile Flooring'
        LUXURY_VINYL_PLANK_FLOORING = 'Luxury Vinyl Plank Flooring'
        BALCONY = 'Balcony'
        FENCED_BACKYARD = 'Fenced Backyard'
        FIRE_PIT = 'Fire-Pit'
        OCEAN_VIEWS = 'Ocean views'
        CITY_VIEWS = 'City views'
        MOUNTAIN_VIEWS = 'Mountain views'
        RIVER_VIEWS = 'River Views'
        LAKE_ACCESS = 'Lake Access'
        IN_SUITE_STORAGE = 'In-suite Storage'
        STORAGE_LOCKERS = 'Storage Lockers'
        ELEVATOR = 'Elevator'
        ZERO_STEP_ENTRANCE = 'Zero-Step Entrance'
        EXTRA_WIDE_DOORWAYS = 'Extra-Wide Doorways'
        ROLL_IN_SHOWER = 'Roll-in Shower'
        SWIMMING_POOL = 'Swimming Pool'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((home_features for home_features in cls if home_features.value == formatted), None)

    class AVAILABILITY(Enum):
        IMMEDIATE = 'Immediate',
        JUNE = 'June',
        OCTOBER = 'October',
        NOVEMBER = 'November',
        APRIL = 'April',
        MARCH = 'March',
        DECEMBER = 'December',
        JULY = 'July',
        AUGUST = 'August',
        SEPTEMBER = 'September',
        FEBRUARY = 'February',
        JANUARY = 'January'

        def get_formatted(self):
            return self.value

        @classmethod
        def from_formatted(cls, formatted: str):
            return next((availability for availability in cls if availability.value == formatted), None)


class Listing:

    def __init__(self,
                 ref_id=None,
                 title=None,
                 price=None,
                 type=None,
                 sq_feet=None,
                 availability=None,
                 location=None,
                 rented=None,
                 thumb=None,
                 thumb2=None,
                 slide=None,
                 link=None,
                 latitude=None,
                 longitude=None,
                 address=None,
                 address_hidden=None,
                 city=None,
                 province=None,
                 community=None,
                 quadrant=None,
                 phone=None,
                 preferred_contact=None,
                 website=None,
                 smoking=None,
                 lease_term=None,
                 garage_size=None,
                 bedrooms=None,
                 den=None,
                 baths=None,
                 cats=None,
                 dogs=None,
                 utilities_included=None,
                 **kwargs):
        self.id = ref_id
        self.title = title
        try:
            self.price = int(price)
        except ValueError:
            self.price = int(price.split('-')[0].strip())
        self.type = type
        self.sq_feet = sq_feet
        self.availability = availability
        self.location = location
        self.rented = rented
        self.thumb = thumb
        self.thumb2 = thumb2
        self.slide = slide
        self.link = f'https://www.rentfaster.ca{link}'
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.address_hidden = address_hidden
        self.city = city
        self.province = province
        self.community = community
        self.quadrant = quadrant
        self.phone = phone
        self.preferred_contact = preferred_contact
        self.website = website
        self.smoking = smoking
        self.lease_term = lease_term
        self.parking = garage_size
        self.bedrooms = bedrooms
        self.den = den
        self.baths = baths
        self.cats = cats
        self.dogs = dogs
        self.utilities_included = [] if not utilities_included else utilities_included

    @classmethod
    def from_json(cls, listing_json):
        return cls(**listing_json)

    def to_dict(self):
        return {
            'Price': self.price,
            'Type': self.type,
            'Community': self.community,
            'Parking': self.parking,
            'Utilities': ','.join(self.utilities_included),
            'Square Feet': self.sq_feet,
            'Bedrooms': self.bedrooms,
            'Link': self.link,
            'Thumbnail': self.thumb,
            'Latitude': self.latitude,
            'Longitude': self.longitude
        }


class RentFaster:

    def __init__(self, city_id: CITY_ID = CITY_ID.CALGARY):
        self._city_id = city_id
        self._search_url = f'https://www.rentfaster.ca/api/search.json?city_id={city_id.value}&novacancy=1&'
        fields_url = f'https://www.rentfaster.ca/api/fields.json?city_id={city_id.value}&'
        fields_url_response = requests.get(fields_url)
        fields = fields_url_response.json()
        self.neighborhoods = fields['neighborhood']
        self.filter = ''
        self.properties = None

    def reset_filter(self):
        self.filter = ''

    def set_filter(self,
                   property_type: list = None,
                   beds: list = None,
                   baths: list = None,
                   utilities_included: list = None,
                   furnishing: list = None,
                   pet: list = None,
                   smoking: list = None,
                   parking: list = None,
                   price_from: int = 0,
                   price_to: int = 10000,
                   home_features: list = None,
                   availability: list = None,
                   neighborhood: list = None
                   ):
        self.filter = f'type={self._get_url_formatted(property_type) if property_type else str()}&' \
                      f'beds={self._get_url_formatted(beds) if beds else str()}&' \
                      f'baths={self._get_url_formatted(baths) if baths else str()}&' \
                      f'utilities_included={self._get_url_formatted(utilities_included) if utilities_included else str()}&' \
                      f'garage_size={self._get_url_formatted(parking) if parking else str()}&' \
                      f'furnishing={self._get_url_formatted(furnishing) if furnishing else str()}&' \
                      f'pet={self._get_url_formatted(pet) if pet else str()}&' \
                      f'smoking={self._get_url_formatted(smoking) if smoking else str()}&' \
                      f'price_range_adv%5Bfrom%5D={price_from}&' \
                      f'price_range_adv%5Bto%5D={price_to}&' \
                      f'home_features={self._get_url_formatted(home_features) if home_features else str()}&' \
                      f'availability={self._get_url_formatted(availability) if availability else str()}&' \
                      f'neighborhood={self._get_url_formatted(neighborhood) if neighborhood else str()}&'

    def set_filter_from_json(self, filename='filter.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                filter = json.load(file)
                self.set_filter(**filter)
        else:
            self.set_filter()

    @staticmethod
    def _get_url_formatted(value_list: list):
        if type(value_list[0]) is not str:
            value_list = [value.get_formatted() for value in value_list]
        return ','.join([value.replace(' ', '%20').replace('+', '%2B').replace('/', '%2F') for value in value_list])

    def request_properties(self, dump=False):
        LISTINGS = MANAGER.list()
        url = self._search_url + self.filter + 'cur_page=0'
        url_response = requests.get(url)
        json_data = url_response.json()
        if dump:
            with open('apartments.json', 'w') as file:
                json.dump(json_data, file, indent=4)
        prop_count = int(json_data['total'])
        pages = range(1, math.ceil(prop_count / int(json_data['total2'])))
        print(f'{prop_count} properties found...')
        LISTINGS.extend([Listing(**listing) for listing in json_data['listings']])

        pool = Pool()
        for page in pages:
            r = pool.apply_async(request_properties,
                                 args=(self._search_url, self.filter, LISTINGS),
                                 kwds={'page': page})
        pool.close()
        pool.join()
        self.properties = list(LISTINGS)
        return pd.DataFrame([prop.to_dict() for prop in self.properties], index=[prop.id for prop in self.properties])