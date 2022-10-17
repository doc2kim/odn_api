# import geopy


import os
import sys

from geopy.geocoders import Nominatim


def test():

    sys.path.append(
        "/var/app/venv/staging-LQM1lest/lib/python3.8/site-packages")
    sys.path.append("../")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()

    # from buoy.models import Location

    # location = Location.objects.all()
    # print(dir(location[0].address))
    # print(location[0].address.raw)
    geo_locator = Nominatim(user_agent='odn')

    location = geo_locator.reverse(
        "%f, %f" % (35.0966, 129.081))
    results = location.raw.get('address')
    # addresses = results.get('address_components')
    country = results.get('country')
    # province = results.get('province', None)
    # city = results.get('city', None)
    # borough = results.get('borough', None)
    # county = results.get('county', None)
    # village = results.get('village', None)
    # town = results.get('town', None)
    print(results)
    if 'province' in results and 'city' in results:
        state = "%s %s" % (results['province'], results['city'])
    elif 'province' in results:
        state = results['province']
    else:
        state = results['city']

    if 'county' in results or 'borough' in results:
        if 'county' in results:
            locality = results['county']
        else:
            locality = results['borough']
    else:
        locality = None

    if 'village' in results and 'town' in results:
        address = "%s, %s" % (results['town'], results['village'])
    elif 'village' in results:
        address = results['village']
    elif 'town' in results:
        address = results['town']
    else:
        address = None

    print(country, state, locality, address)
    # for i in addresses:
    #     if "country" in i.get('types'):
    #         country = i['long_name']
    #         country_code = i['short_name']
    #     elif "administrative_area_level_1" in i.get('types') or "city" in i.get('types'):
    #         state = i['long_name']
    #         state_code = i['short_name']

    #     if "locality" in i.get('types') or 'sublocality_level_1' in i.get('types'):
    #         locality = i['long_name']
    #     else:
    #         locality = None

    #     if "postal_code" in i.get('types'):
    #         postal_code = i['long_name']
    #     else:
    #         postal_code = None

    #     print(locality)
    # address = {
    #     'raw': results.get('formatted_address', None),
    #     'locality': locality,
    #     'postal_code': postal_code,
    #     'state': state,
    #     'state_code': state_code,
    #     'country': country,
    #     'country_code': country_code
    # }

    # print(address)
# lat = "33.54943"
# lon = "126.64993"

# lat2 = "34.44"
# lon2 = "127.011"

# locator = GoogleV3(api_key="odn_api")


# location = locator.reverse('{},{}'.format(lat2, lon2))

# # print(dir(location))
# print(location.address)

test()
