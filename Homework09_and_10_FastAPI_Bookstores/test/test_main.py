from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

test_data = {
    "name": "The Sky is Blue",
    "author": {
        "name": "John Doe",
        "author_id": "JODO-1234"
    },
    "year_published": 2023
}

test_data_1 = {
    "name": "What to eat today?",
    "author": {
        "name": "Alana Grey",
        "author_id": "ALGR-1234"
    },
    "year_published": 2020
}

# PUT API with correct body input => 200
def test_put_correct_api():
    response_put = client.put("books/TheSkyIsBlue", json = test_data)
    assert response_put.status_code == 200



# PUT API with wrong body input => 404
def test_put_wrong_api():
    response_put_wrong = client.put("books/TheSkyIsBlue", json = {
    "name": "The Sky is Blue",
    "author": {
        "name": "John Doe",
        "author_id": "JODO-12345"
    },
    "year_published": 2023
    })
    assert response_put_wrong.status_code == 422



# GET API and return a correct body => 200: Option 1:
def test_get_api():
    response_put = client.put("books/TheSkyIsBlue", json = test_data)
    assert response_put.status_code == 200

    response_get = client.get("books/TheSkyIsBlue")
    assert response_get.status_code == 200

    response_put_data, response_get_data = json.loads(response_put.text), json.loads(response_get.text)
    assert response_put_data == response_get_data
# json.loads() method to convert the JSON-formatted string from the response_put.text into a Python object.
# This assumes that the content of response_put.text is a valid JSON-formatted string.

# GET API and return a correct body => 200: Option 2:
def test_get_api_1():
    response_put = client.put("books/TheSkyIsBlue", json = test_data)
    assert response_put.status_code == 200

    response_get = client.get("books/TheSkyIsBlue")
    assert response_get.status_code == 200 

    # uses .json() to parses the response content (assumed to be in JSON format) and returns a Python object.
    response_put_api = response_put.json()
    response_get_api = response_get.json()
    assert response_put_api == response_get_api



# DELETE API:
def test_delete_api():
    response_delete = client.delete("books/TheSkyIsBlue")
    assert response_delete.status_code == 200
    response_get_1 = client.get("books/TheSkyIsBlue")
    assert response_get_1.status_code == 404



# GET all API
def test_get_all_api():
    response_put = client.put("books/TheSkyIsBlue", json = test_data)
    assert response_put.status_code == 200
    
    response_put_1 = client.put("books/Whattoeattoday?", json = test_data_1)
    assert response_put_1.status_code == 200

    response_get_2 = client.get("books")
    assert response_get_2.status_code == 200

    response_get_data_2 = json.loads(response_get_2.text)
    assert response_get_data_2 == [test_data, test_data_1]

