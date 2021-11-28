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
the character appears in. 

"""


import requests, json

class Request_handler:

    def __init__(self, apiTarget: str, query: str):
        self.apiTarget = apiTarget
        self.query = query
    
    def api_request(self, requestType, charName, apiKey):

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


class Json_parser:

    def parse(self, jsonContent):
        self.parsedContent = json.loads(jsonContent)
        return self.parsedContent

####################################
class Character:

    #name = ""
    #description = ""
    #comics = []

    def __init__(self, name, description):

        self.name = name
        self.description = description

        



def get_character():

    # instantiate a request_handler object and make the call
    characterLookup = Request_handler("characters?", "nameStartsWith")

    charName = input("Please enter a name of a Marvel character to look up: ")
    if " " in charName:
        charName = charName.replace(" ", "%20")

    publicKey = "0a73c0cb4d1aa96b73be3e13bc98261c"
    response = characterLookup.api_request("GET", charName, publicKey )

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = Json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict



def get_comic(comicNumber):

    comicNumber = comicNumber + "?"
    comicLookup = Request_handler("comics/", comicNumber )
    

# take the dictionary from the Json repsonse and a category name
# find the the category name as a slice of the results: list inside the dict. 
def get_InfoCategory(category: str, responseDictionary):

    results = responseDictionary['data']['results']
    count = responseDictionary['data']['count']

    if count != 0:
        for result in results:
            print (result[category])
    else:
        print("No results for {} found".format(category))
  

def main ():
    
    character_Dictionary = get_character()

    results = character_Dictionary['data']['results']
    count = character_Dictionary['data']['count']

    if count != 0:
        for result in results:
            name = result['name']
            description = result['description']
            char = Character(name, description)
            print(char.name)
            print(char.description)
    else:
        print("No results found")


if __name__ == "__main__":

    main()