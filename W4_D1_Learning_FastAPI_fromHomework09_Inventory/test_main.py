#pytest

from fastapi.testclient import TestClient 
from main import app #we are referring to the app that we define in the main.py 


def test_basic_example():
    assert True #or you can use "pass", by default our test is gonna pass and does not test anything.
#assert can be called with function () eg. assert (True) or just space.
#If it does not work or command is not found, try to install pip with: pip install pytest



client = TestClient(app) #introducing a new test client from the app that we already defined.
#If we do that, we can finally do the unit testing on the API.

def test_put_api():
    response = client.put("/inventoryitems/02BR", json={
        "name": "coffee",
        "quantity": 100,
        "serial_number": "2BeachRoad",
        "origin": {
            "country": "Ethiopia",
            "production_date": "2023"
        }
    })
    #print(response.json()) #print out to see the body of json if you have problem, json as a function to return
    assert response.status_code == 200

