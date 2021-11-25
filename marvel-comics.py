"""
Requirements
1. Ask for input from the user.
2. Make HTTP requests to the Marvel Comics API. Done
3.Process the JSON response from the API and print out
relevant details. Done
4.Handle the error case where no Marvel character is found
that matches the user input.

"""


import requests, json

class request_handler:

    _url_prefix = "https://gateway.marvel.com:443/v1/public/characters?"


    def api_request(self, requestType, charName, apiKey):

        if requestType == "GET":
            self.url_suffix = "name={}&ts=1&apikey={}&hash=3a0a5532ff049374f793672544269edf".format(charName, apiKey)
            self.url_full = self._url_prefix + self.url_suffix
            
            print("Requesting from URL:" + self.url_full)
            return requests.get(self.url_full)
            
        else:
            # do some stuff with POST / UPDATE / PUT etc. 
            print("Please make a GET call")


class json_parser:

    def parse(self, jsonContent):
        self.parsedContent = json.loads(jsonContent)
        return self.parsedContent


def get_results():

    # instantiate a request_handler object and make the call
    api = request_handler()

    charName = input("Please enter a name of a Marvel character to look up: ")
    if " " in charName:
        charName = charName.replace(" ", "%20")

    publicKey = "0a73c0cb4d1aa96b73be3e13bc98261c"
    response = api.api_request("GET", charName, publicKey )

    # instantiate a json_parser object and produce a dictionary from the api response
    returnedJson = json_parser()
    responseDict = returnedJson.parse(response.text)
    return responseDict


def get_InfoCategory(category: str, responseDictionary):

    results = responseDictionary['data']['results']

    for result in results:
        print (result[category])

def main ():
  
    resultsDictionary = get_results()
    get_InfoCategory("name", resultsDictionary)
    get_InfoCategory("description", resultsDictionary)


if __name__ == "__main__":

    main()