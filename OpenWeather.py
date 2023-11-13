# openweather.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yash Pathak
# pathaky@uci.edu
# 51317074

# API KEY: acb9858a37fbea9ff876d852b50bb85e

import urllib, json
from urllib import request, error
from WebAPI import WebAPI

class OpenWeather(WebAPI):
    '''
    OpenWeather class. Instantiates the class and it's attrbutes. Inherits from WebAPI.

    '''
    
    def __init__(self, zipcode: int, ccode: str):
        '''
        Constructor for OpenWeather class. Takes zipcode and ccode as default values.

        '''
        super().__init__(apikey = 'acb9858a37fbea9ff876d852b50bb85e')
        self.zipcode = zipcode
        self.ccode = ccode
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.sunset = None
        self.city = None
        self.url = None
        self.error = False


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        if self.apikey == None:
            print("apikey does not exist. Please set apikey first.")

        else:
            self.url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"
            # self.url = f"http://httpstat.us/429"

            # try creating a dicitonary, throw excpetion based on error.
            try:
                r_obj = self._download_url(self.url)

                self.temperature = r_obj['main']['temp']
                self.high_temperature = r_obj['main']['temp_max']
                self.low_temperature = r_obj['main']['temp_min']
                self.longitude = r_obj['coord']['lon']
                self.latitude = r_obj['coord']['lat']
                self.description = r_obj['weather'][0]['description']
                self.humidity = r_obj['main']['humidity']
                self.sunset = r_obj['sys']['sunset']
                self.city = r_obj['name']

            except Exception as e:
                print(e)
                self.error = True

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        if '@weather' in message:
            message = message.replace('@weather', str(self.description))
        
        return message
        