# webapi.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yash Pathak
# pathaky@uci.edu
# 51317074

from abc import ABC, abstractmethod
import urllib, json
from urllib import request, error

class WebAPI(ABC):

  def __init__(self, apikey: str) -> None:
    self.apikey = apikey


  def _download_url(self, url: str) -> dict:
    #TODO: Implement web api request code in a way that supports ALL types of web APIs
    response = None
    r_obj = None

    # Try creating json object and convert it to dictionary using url, if unable to create, throw exception.
    # Based on type or error, print error code and print the reason why that error occurred.
    try:
        response = urllib.request.urlopen(url)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
      if e.code == 403:
         raise Exception(f'Error {e.code}: Forbidden Exception.')
      if e.code == 404:
        self.error = True
        raise Exception(f'Error {e.code}: Server can not found the requested resource.')
      elif e.code == 503:
        self.error = True
        raise Exception(f'Error {e.code}: Service unavailable.')
      elif e.code == 401:
        raise Exception(f'Error {e.code}: Did not specify API key in API Request.')
      elif e.code == 429:
        raise Exception(f'Error {e.code}: Maximum free API calls reached! Please consider upgrading your service.')
      elif e.code in [500, 502, 503, 504]:
        raise Exception(f'Error {e.code}: Please contact OpenWeather API for further assistance.')
      elif e.code == 2:
        raise Exception(f'Error {e.code}: Invalid service - This service does not exist')
      elif e.code == 3:
        raise Exception(f'Error {e.code}:Invalid Method - No method with that name in this package')
      elif e.code == 4:
        raise Exception(f'Error {e.code}: Authentication Failed - You do not have permissions to access the service')
      elif e.code == 5:
        raise Exception(f"Error {e.code}: Invalid format - This service doesn't exist in that format")
      elif e.code == 6:
        raise Exception(f'Error {e.code}: Invalid parameters - Your request is missing a required parameter')
      elif e.code == 7:
        raise Exception(f'Error {e.code}: Invalid resource specified')
      elif e.code == 8:
        raise Exception(f'Error {e.code}: Operation failed - Something else went wrong')
      elif e.code == 10:
        raise Exception(f'Error {e.code}: Invalid API key - You must be granted a valid key by last.fm')
      elif e.code == 11:
        raise Exception(f'Error {e.code}: Service Offline - This service is temporarily offline. Try again later.')
      elif e.code == 13:
        raise Exception(f'Error {e.code}: Invalid method signature supplied')
      elif e.code == 16:
        raise Exception(f'Error {e.code}: There was a temporary error processing your request. Please try again')
      elif e.code == 26:
        raise Exception(f'Error {e.code}: Suspended API key - Access for your account has been suspended, please contact Last.fm')
      elif e.code == 29:
        raise Exception (f'Error {e.code}: Rate limit exceeded - Your IP has made too many requests in a short period')
      else:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        print(e.read())
        self.error = True

    except urllib.error.URLError as e:
        print('Could not connect to the internet!\nCheck your connection.')
        print(e.reason)
        self.error = True

    finally:
        if response != None:
            response.close()

    return r_obj

	
  def set_apikey(self, apikey:str) -> None:
    '''
    Set apikey.

    '''
    self.apikey = apikey

	
  @abstractmethod
  def load_data(self) -> None:
    pass
	

  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
