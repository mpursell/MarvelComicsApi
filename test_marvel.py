import pytest
import requests
from marvelComics import *

def stub(url):
    return {'test':'dictionary'}

def test_Api_request(monkeypatch):

    #Arrange
    monkeypatch.setattr(requests, 'get', stub)
    url = 'https:/test/path'

    #Act
    api = Api_request()
    response = api.make_Request(url)

    #Assert
    assert isinstance(response, dict)
    
