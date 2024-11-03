import datetime
import os 
import dotenv
from pprint import pprint

from ownerrezconnector import api

dotenv.load_dotenv()
username = os.getenv("USERNAME")
token = os.getenv("TOKEN")

def test_guest():
    orapi = api.Ownerrezapi(username, token)
    guest = orapi.getguest(612693599)
    guestname = guest.first_name + " " + guest.last_name
  
    print(guestname)


# def main():
    # print("Hello World")
    # orapi = api.Ownerrezapi(username, token)
    # propid = 7599858

    # booking = orapi.getbooking(propid)
    
    # pprint(booking)
    # print(booking.guest.first_name + " " + booking.guest.last_name)
    
    # events = []
    # for booking in bookings:
    #     print(booking.id)
    #     print(booking.title)
    #     print(booking.arrival)
    #     print(booking.departure)
    #     print(booking.adults)
    #     print(booking.children)
    #     print(booking.type)
    #     print("")

    #     if booking.type == "block":
    #         title = "Block"
    #     else:

    #         guest = orapi.getguest(booking.guest_id)
    #         guestname = guest.first_name + " " + guest.last_name
    #         title = guestname

    #     event = {
    #         "title": title,
    #         "id": booking.id,
    #         "start": booking.arrival,
    #         "end": booking.departure,
    #         "adults": booking.adults,
    #         "children": booking.children
    #     }
    #     events.append(event)
    #     print(event)
    # print(events)
def test_getproperties():
    orapi = api.Ownerrezapi(username, token)
    properties = orapi.getproperties()
    assert len(properties) > 0

def test_getbookings():
    orapi = api.Ownerrezapi(username, token)
    properties = orapi.getproperties()
    bookings = orapi.getbookings(property_id=properties[0].id, since_utc="2024-01-01")
    assert len(bookings) > 0

def test_getbooking():
    orapi = api.Ownerrezapi(username, token)
    properties = orapi.getproperties()
    bookings = orapi.getbookings(property_id=properties[0].id, since_utc="2024-01-01")
    booking = orapi.getbooking(booking_id=bookings[0].id)
    assert booking is not None

def test_getguest():
    orapi = api.Ownerrezapi(username, token)
    properties = orapi.getproperties()
    bookings = orapi.getbookings(property_id=properties[0].id, since_utc="2024-01-01")
    booking = orapi.getbooking(booking_id=bookings[0].id)
    guest = orapi.getguest(booking.guest.id)
    assert guest is not None

# print (username)

# api = api.Ownerrezapi(username, token)

# print(api.getproperties())
# propdata = api.getproperties()

# pprint(propdata)

# print(propdata[0].id)
# print(propdata[0].name)


# reservations = api.getbookings(property_id=propdata[0].id, since_utc="2024-01-01")

# pprint(reservations)
# envents = []



# for booking in reservations:
#     print(booking.id)
#     print(booking.title)
#     print(booking.arrival)
#     print(booking.departure)
   
#     print(booking.adults)
#     print(booking.children)
#     print("")
#     if booking.guest is not None:
#         title = api.getguest
#             title = api.getguest(booking.guest.id).first_name + " " + api.getguest(booking.guest.id).last_name
#     else:
#         title =  "Guest"
#     event = {
#         "title": title,
#         "id": booking.id,
#         "title": booking.title,
#         "start": booking.arrival,
#         "end": booking.departure,
#         "adults": booking.adults,
#         "children": booking.children
#     }
#     print(event)




# props = api.getproperties()
# for prop in props:
#     print(prop.id)
#     print(prop.name)
#     print(prop.thumbnail_url_large)


# api = Ownerrezapi(username, token)

# print(api.isunitbooked(357991))

# bookings = api.getbookings(property_id=357991, since_utc="2024-01-01")
# today = datetime.datetime.today()
# for booking in bookings:
#     arrival = datetime.datetime.strptime(booking.arrival, "%Y-%m-%d")
#     departure = datetime.datetime.strptime(booking.departure, "%Y-%m-%d")
    
#     if arrival <= today and departure >= today:
#         print("Unit is booked today")
#         print(booking.id)
#         print(booking.title)
#         continue

#booking = api.getbooking(booking_id=9732833)



#print(booking.guest.last_name)


if __name__ == "__main__":
  #  test_guest()
    main()
    