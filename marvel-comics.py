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


from typing import List
import requests, json

# Class to handle requests to the Marvel API
class Request_handler:

    def __init__(self, apiTarget: str, query: str):
        self.apiTarget = apiTarget
        self.query = query
        
    
    def character_request(self, requestType, charName, apiKey):

        # url suffix and prefix generalised so that the api endpoint to query can be 
        # given at the time the object is instantiated.  
        __url_prefix = "https://gateway.marvel.com:443/v1/public/{}".format(self.apiTarget)

        if requestType == "GET":
            self.__url_suffix = "{}={}&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(self.query, charName, apiKey)
            self.__url_full = __url_prefix + self.__url_suffix
            
            print("Requesting from URL:" + self.__url_full)
            return requests.get(self.__url_full)
            
        else:
            # do some stuff with POST / UPDATE / PUT etc. 
            print("Please make a GET call")

    def comics_request(self, apiKey, comicURL):

        __url_prefix = comicURL

        self.__url_suffix = "?&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(apiKey)
        self.__url_full = __url_prefix + self.__url_suffix
        
        print("Requesting from URL:" + self.__url_full)
        return requests.get(self.__url_full)
            

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

        


# method to get a dictionary of character attributes given a character name
def get_character(public_key: str) -> dict:

    # instantiate a request_handler object and make the call
    characterLookup = Request_handler("characters?", "nameStartsWith")

    charName = input("Please enter a name of a Marvel character to look up: ")
    if " " in charName:
        charName = charName.replace(" ", "%20")

    
    response = characterLookup.character_request("GET", charName, public_key )

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict


# method to get a dictionary of comic attributes given a comic URL
def get_comic(publicKey: str, comicURL: str) -> dict:

    # instantiate a request_handler object and make the api call
    comicLookup = Request_handler("comics/?", " ")
    response  =  comicLookup.comics_request(publicKey, comicURL)

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict
    


def main ():
    
    publicKey = "0a73c0cb4d1aa96b73be3e13bc98261c"
    character_Dictionary = get_character(publicKey)

    # key into the dictionary to produce a list
    char_results = character_Dictionary['data']['results']
    count = character_Dictionary['data']['count']

    # iterate over the list, which is a list of dicts
    if count != 0:
        for result in char_results:
            # key into the dict as required
            name = result['name']
            description = result['description']
            comics = result['comics']['items']

            # instantiate a Character object and pass some attributes to it
            char = Character()
            char.name = name
            char.description = description
            char.comics = comics

            print(char.name)
            print(char.description)

            for comic in char.comics:
                comic_URL = comic['resourceURI']
                comic_dict = get_comic(publicKey, comic_URL)
                individualComicList = comic_dict['data']['results']
                for individualComic in individualComicList:
                    print(individualComic['title'])
                    if individualComic['description'] == "":
                        print('No summary available for this comic')
                    else:
                        print(individualComic['description'])
    else:   
        print("No results found")


if __name__ == "__main__":

    main()