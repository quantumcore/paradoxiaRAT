"""

Have a good time reading the source. You are an amazing person.

"""
import geoip2.database
import socket
database_path = "GeoLite2-City.mmdb"

def scan_ip(IP_ADDR):

    try:
        database = geoip2.database.Reader(database_path)
        ip_info = database.city(IP_ADDR)
        ISO_CODE = ip_info.country.iso_code
        country = ip_info.country.name
        pstlcode = ip_info.postal.code
        reigon = ip_info.subdivisions.most_specific.name
        city = ip_info.city.name
    # location = str(ip_info.location.latitude) + " " + str(ip_info.location.longitude)
        location = "https://www.google.com/maps?q="+str(ip_info.location.latitude)+","+str(ip_info.location.longitude)
    
        print("[+] IP               : " + str(IP_ADDR))
        print(" |_ ISO Code          : " + str(ISO_CODE))
        print(" |_ Country           : " + str(country))
        print(" |_ Postal Code       : "+str(pstlcode))
        print(" |_ Reigon            : " + str(reigon))
        print(" |_ City              : " + str(city))
        print(" |_ Location          : " + str(location))
        

    except Exception as ERROR:
        print("[SCANNER ERROR] : {error}".format(error = ERROR))
        print("[+] IP               : " + str(IP_ADDR))
        print(" |_ Do further scanning with nmap and / or Blacklist.")

    