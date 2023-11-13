# lastfm.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yash Pathak
# pathaky@uci.edu
# 51317074

# api_key : 080bc3102eb83b87ddeb7f80699c145d

import urllib, json
from urllib import request,error
from WebAPI import WebAPI

class LastFM(WebAPI):
    '''
    LastFM Class. Instantiates the class and it's attrbutes. Inherits from WebAPI.
    '''

    def __init__(self):
        '''
        Constructor for LastFM class, with default artist as 'cher'.

        '''
        super().__init__(apikey = '080bc3102eb83b87ddeb7f80699c145d')
        self.artist = 'cher'
        self.toptrackname = None
        self.toptrackplaycount = None
        self.toptracklisteners = None
        self.error = False


    def set_artist(self, artist: str) -> None:
        '''
        Sets the artist based on user input.

        '''
        self.artist = artist


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        if self.apikey == None:
            print("apikey does not exist. Please set apikey first.")

        else:
            # try creating a dicitonary, throw excpetion based on error.
            try:
                self.url = f"https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={self.artist}&api_key={self.apikey}&format=json"
                # self.url = f"httpstat.us/200"

                r_obj = self._download_url(self.url)

                if 'error' in r_obj:
                    print(r_obj['message'])
                    self.error = True
                
                else:
                    self.toptrackname = r_obj['toptracks']['track'][0]['name']
                    self.toptrackplaycount = r_obj['toptracks']['track'][0]['playcount']
                    self.toptracklisteners = r_obj['toptracks']['track'][0]['listeners']

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
        if '@lastfm' in message:
            message = message.replace('@lastfm', str(self.toptrackname))
        
        return message
