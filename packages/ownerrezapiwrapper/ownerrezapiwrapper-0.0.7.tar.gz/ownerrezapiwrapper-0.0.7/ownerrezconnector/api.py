import requests
from typing import List, Dict
import logging
from ownerrezconnector.constants import BASEURL as hosturl
from ownerrezconnector.model import *
from ownerrezconnector.restAdapter import RestAdapter
import datetime


log = logging.getLogger(__name__)
headers = {'User-Agent':'My App','Content-Type':'application/json'}
log.setLevel(logging.DEBUG)

class Ownerrezapi(object):
    """
    OwnerRez API wrapper class
    """

    def __init__(self,username, token):
        """
        Initialize the OwnerRez API wrapper with the OwnerRez username and token
        :param username: OwnerRez username
        :param token: OwnerRez token
        """
        self.username = username
        self.token = token
    
    def getproperties(self) -> list:
        """
        Get a list of properties.
        """
        restAdapt = RestAdapter(self.username,self.token)
        results = []
        property_list = restAdapt.get(endpoint='properties')
        for prop in property_list.data['items']:
            prop = Property(**prop)
            results.append(prop)
        return results

    def getbookings(self, property_id: int, since_utc: datetime) -> List[Booking]:
        """
        Get a list of bookings for a property since a given date.
        """
        restAdapt = RestAdapter(self.username,self.token)
        results = []
        params = {'since_utc': since_utc, 'property_id': property_id}
        booking_list = restAdapt.get(endpoint='bookings', ep_params=params)

        for booking in booking_list.data['items']:
            booking = Booking(**booking)
            results.append(booking)
        return results
    
    def getbooking(self, booking_id: int) -> Booking:
        """
        Get a single booking by ID.
        """
        restAdapt = RestAdapter(self.username,self.token)
        booking = restAdapt.get(endpoint=f'bookings/{booking_id}')
        return Booking(**booking.data)
    
    def getguest(self, guest_id: int) -> Guest:
        """
        Get a single guest by ID.
        """
        restAdapt = RestAdapter(self.username,self.token)
        guest = restAdapt.get(endpoint=f'guests/{guest_id}')
        return Guest(**guest.data)
    
    def isunitbooked(self, property_id: int) -> bool:
        """
        Check if a unit is booked today.
        """
        today = datetime.datetime.today()
        bookings = self.getbookings(property_id=property_id, since_utc=today)
        for booking in bookings:
            arrival = datetime.datetime.strptime(booking.arrival, "%Y-%m-%d")
            departure = datetime.datetime.strptime(booking.departure, "%Y-%m-%d")
            if arrival <= today and departure >= today:
                return True
        return False