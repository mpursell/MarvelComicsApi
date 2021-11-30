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

import requests 
import json

# Class to handle requests to the Marvel API
class Request_handler:

    def __init__(self, apiTarget: str, query: str):
        self.apiTarget = apiTarget
        self.query = query
        
    
    def character_Request(self, charName: str, apiKey:str) -> json:

        # url suffix and prefix generalised so that the api endpoint to query can be 
        # given at the time the object is instantiated.  
        __urlPrefix = "https://gateway.marvel.com:443/v1/public/{}".format(self.apiTarget)

    
        self.__urlSuffix = "{}={}&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(self.query, charName, apiKey)
        self.__urlFull = __urlPrefix + self.__urlSuffix
        
        # debugging print statement
        #print("Requesting from URL:" + self.__urlFull)
        
        return requests.get(self.__urlFull)
    

    def comics_Request(self, apiKey: str, comicURL: str) -> json:

        __urlPrefix = comicURL

        self.__urlSuffix = "?&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(apiKey)
        self.__urlFull = __urlPrefix + self.__urlSuffix
        
        # debugging print statement
        #print("Requesting from URL:" + self.__urlFull)
        
        return requests.get(self.__urlFull)
            

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
def get_Character(public_key: str) -> dict:

    # instantiate a request_handler object and make the call
    characterLookup = Request_handler("characters?", "nameStartsWith")

    charName = input("Please enter a name of a Marvel character to look up: ")
    if " " in charName:
        charName = charName.replace(" ", "%20")

    
    response = characterLookup.character_Request(charName, public_key )

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict


# method to get a dictionary of comic attributes given a comic URL
def get_Comic(publicKey: str, comicURL: str) -> dict:

    # instantiate a request_handler object and make the api call
    comicLookup = Request_handler("comics/?", " ")
    response  =  comicLookup.comics_Request(publicKey, comicURL)

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict
    


def main ():
    
    publicKey = "0a73c0cb4d1aa96b73be3e13bc98261c"
    characterDictionary = get_Character(publicKey)

    # key into the dictionary to produce a list
    char_results = characterDictionary['data']['results']
    count = characterDictionary['data']['count']

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
    else:   
        print("No results found")


if __name__ == "__main__":

    main()