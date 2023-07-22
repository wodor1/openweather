import requests
import datetime
from cachetools import cached, TTLCache

x = True
cache = TTLCache(maxsize=10000, ttl=1200)

while x == True:
    api_key = "PLEASE ENTER YOUR API KEY HERE"
    location = input("Please enter the location or type exit: ")
    if location == "exit":
        print("Goodbye!")
        exit()

    @cached(cache)
    def get_location(location):
        print("Getting location from API...")
        response_location = requests.get(
            "http://api.openweathermap.org/geo/1.0/direct?q=" + location + "&limit=5&appid=" + api_key)
        latitude = str(response_location.json()[0]["lat"])
        longitude = str(response_location.json()[0]["lon"])
        return latitude, longitude

    @cached(cache)
    def get_precipitation(latitude, longitude):
        print("Getting precipitation from API...")
        response = requests.get(
            "https://api.openweathermap.org/data/3.0/onecall?lat=" + latitude + "&lon=" + longitude + "&exclude=current,hourly,daily,alerts&units=metric&appid=" + api_key)
        return response.json()

    latitude, longitude = get_location(location)
    response = get_precipitation(latitude, longitude)
    prec_list = response['minutely']
    first = round((((sum([float(i['precipitation'])
                    for i in prec_list[0:15]]))/60))*15, 2)
    second = round((((sum([float(i['precipitation'])
                    for i in prec_list[15:30]]))/60)*15), 2)
    third = round((((sum([float(i['precipitation'])
                    for i in prec_list[30:45]]))/60)*15), 2)
    fourth = round((((sum([float(i['precipitation'])
                    for i in prec_list[45:60]]))/60)*15), 2)

    first_quarter = str(first)
    second_quarter = str(second)
    third_quarter = str(third)
    fourth_quarter = str(fourth)
    print("The precipitation in the first quarter is: " +
          first_quarter + " mm")
    print("The precipitation in the second quarter is: " +
          second_quarter + " mm")
    print("The precipitation in the third quarter is: " +
          third_quarter + " mm")
    print("The precipitation in the fourth quarter is: " +
          fourth_quarter + " mm")

    f = open("api_answer.csv", "a")
    f.write("The date and time of the request: " +
            str(datetime.datetime.now()) + "\n")
    f.write("The location is: " + location + "\n")
    f.write("The precipitation in the first quarter is: " +
            first_quarter + " mm\n")
    f.write("The precipitation in the second quarter is: " +
            second_quarter + " mm\n")
    f.write("The precipitation in the third quarter is: " +
            third_quarter + " mm\n")
    f.write("The precipitation in the fourth quarter is: " +
            fourth_quarter + " mm\n")
    f.write(" " + "\n")
    f.close()
