readme.txt

I will be explaining what exactly I refactored from my previous a4 program. 

    1. I changed the way I inherited the WebAPI class from the WebAPI.py module into all of my other
    API classes (OpenWeather, LastFM, ExtraCreditAPI). I did so because of the feedback I recieved on 
    my a4 submission. I realised that I wasn't inheriting the WebAPI module into any of my child classes
    correctly, that I was forced to use the name of the parent and only inheriting stuff from WebAPI. So,
    I decided to change it to super(), so that I could also inherit everything that the WebAPI class was inheriting, 
    so that I could inherit the parent's ancestors as well, (ABC class) into my own created child classes.

    