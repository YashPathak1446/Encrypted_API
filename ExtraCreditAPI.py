# extracreditapi.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yash Pathak
# pathaky@uci.edu
# 51317074

# The ExtraCreditAPI, like the other api's, consists of the ExtraCreditAPI class which also inherits from WebAPI.
# The API makes use of urllib, json, request, error, and WebAPI modules.
# The official newapi website is -> https://newsapi.org/
# I initialized the author, the title, and the description of the first news article on the newsapi website.

# The country is fixed to 'US', while the apikey is also hardcoded and basically fixed.
# The API call is of the form "https://newsapi.org/v2/top-headlines?country=us&apiKey={EXTRACREDITAPIKEY}"

# It works pretty much exactly like the other apis, and when the keyword '@extracredit' is used, 
# It is replaced with the news' title.


import urllib, json
from urllib import request, error
from WebAPI import WebAPI

# Global Varible apikey
EXTRACREDITAPIKEY = "4f76ada217d44d5998adf27f69c4d341" 


class ExtraCreditAPI(WebAPI):
    '''
    ExtraCreditAPI Class. Instantiates the class and it's attrbutes. Inherits from WebAPI.
    '''
    
    def __init__(self):
        '''
        Constructor for ExtraCreditAPI class.

        '''
        super().__init__(apikey = EXTRACREDITAPIKEY)
        self.author = None
        self.title = None
        self.description = None
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
            self.url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={EXTRACREDITAPIKEY}"
            # self.url = f"http://httpstat.us/429"

            # try creating a dicitonary, throw excpetion based on error.
            try:
                r_obj = self._download_url(self.url)

                self.author = r_obj['articles'][0]['author']
                self.title = r_obj['articles'][0]['title']
                self.description = r_obj['articles'][0]['description']

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
        if '@extracredit' in message:
            message = message.replace('@extracredit', str(self.title))
        
        return message
        