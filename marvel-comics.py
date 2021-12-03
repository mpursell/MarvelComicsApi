"""
Requirements
1. Ask for input from the user. DONE
2. Make HTTP requests to the Marvel Comics API. DONE
3.Process the JSON response from the API and print out
relevant details. DONE
4.Handle the error case where no Marvel character is found
that matches the user input. DONE
5. Allow "starts with" or "fuzzy"
searches. DONE
6. Provide summaries of all comics that
the character appears in. DONE

"""

from abc import ABC, abstractmethod
import requests 
import json

# Abstract class to base subclass Api_request on
# uneccesary for app, but testing out syntax and concept
class Request_handler(ABC):

    @abstractmethod
    def make_Request(self):
        pass

# Class to handle requests to the Marvel API
class Api_request(Request_handler):

    def __init__(self):

        @property
        def url(self):
            return self._url
        
        @url.setter
        def url(self, value:str):
            return self._url

    def make_Request(self, url: str) -> json:
        return requests.get(url)
    
# Class to parse the JSON returned from the API into a dictionary
class Json_parser:

    def parse(self, jsonContent: json) -> dict:
        self.parsedContent = json.loads(jsonContent)
        return self.parsedContent

# Class for a character creation
class Character:

    def __init__(self):

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, value: str):
            self._name = self._value

        @property
        def description(self):
            return self._description

        @description.setter
        def description(self, value: str):
            self._description = self._value

        @property 
        def comics(self):
            return self._comics

        @comics.setter
        def comics(self, value: list):
            self._comics = self._value

        

# function to get a dictionary of character attributes given a character name
def get_Character(publicKey: str) -> dict:

    charName = input("Please enter a name of a Marvel character to look up: ")
    if " " in charName:
        charName = charName.replace(" ", "%20")

    # capitalise the first letter of the string to make sure API call works
    charNameFormatted = charName[0].upper() + charName[1:]

    urlPrefix = "https://gateway.marvel.com:443/v1/public/characters?nameStartsWith"
    urlSuffix = "={}&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(charNameFormatted, publicKey)
    url = urlPrefix + urlSuffix

    # instantiate a request_handler object and make the call
    characterLookup = Api_request()
    response = characterLookup.make_Request(url)

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)

    if len(responseDict) == 0:
        print("get_character - nothing in the response body")
    else:
        return responseDict


# function to get a dictionary of comic attributes given a comic URL
def get_Comic(publicKey: str, comicURL: str) -> dict:

    urlPrefix = comicURL
    urlSuffix = "?&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(publicKey)
    url = urlPrefix + urlSuffix


    # instantiate a request_handler object and make the api call
    comicLookup = Api_request()
    response = comicLookup.make_Request(url)


    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict
    


def main ():
    
    publicKey = "0a73c0cb4d1aa96b73be3e13bc98261c"
    characterDictionary = get_Character(publicKey)

    try:
        # key into the dictionary to produce a list
        char_results = characterDictionary['data']['results']
        count = characterDictionary['data']['count']
    except TypeError:
        # will throw a TypeError if the repsonse body is empty for the 
        # given character
        print("Possible problem with the response dictionary from the API")

    # iterate over the list, which is a list of dicts
    if count != 0:
        for result in char_results:
            # key into the dict as required
            name = result['name']
            description = result['description']
            comics = result['comics']['items']

            # instantiate a Character object and set some attributes
            char = Character()
            char.name = name
            char.description = description
            char.comics = comics

            # output to host as per the exercise requirements
            print(char.name)
            print(char.description)

            # get the comic titles and summary / description
            for comic in char.comics:
                comic_URL = comic['resourceURI']
                comic_dict = get_Comic(publicKey, comic_URL)

                try:
                    individualComicList = comic_dict['data']['results']
                

                    for individualComic in individualComicList:
                        if individualComic['title'] == "" or individualComic['title'] == None:
                            print('No comic available')
                        else:
                            print(individualComic['title'])
                        if individualComic['description'] == "" or individualComic['description'] == None:
                            print('No summary available for this comic')
                        else:
                            print(individualComic['description'])

                except TypeError:
                    # will throw a TypeError if the repsonse body is empty for the 
                    # given comic
                    continue
    else:   
        print("No results found")


if __name__ == "__main__":

    main()