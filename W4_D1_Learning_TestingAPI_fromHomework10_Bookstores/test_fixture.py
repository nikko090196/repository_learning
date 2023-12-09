from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture
def client():
    yield TestClient(app)


# We are gonna create a test client object every single time we run a test function.
# Everytime we finish using the fixture, it is gonna be removed.
# yield comes from the concept "generator". yield refers to "return except some differences".


# Put a first API (a obj) -> Tear down the object -> Use it to test our Get and Delete API


# no need to define the @pytest.fixture function because we are happy to go with default scope of pytest fixture.
@pytest.fixture
def good_payload():
    return {
        "name": "The Sky is Blue",
        "author": {"name": "John Doe", "author_id": "JODO-1234"},
        "year_published": 2023,
    }


@pytest.fixture
def bad_payload():
    return {
        "name": "What to eat today?",
        "author": {"name": "Alana Grey", "author_id": "ALGR-1234"},
        "year_published": 2024,
    }


def test_put_wrong_api(client, bad_payload):
    # When you refer to an argument to your test function with the same name as the test fixture you created,
    # you are basically calling to the feature's function), you get back the exactly the return of the feature in line 21-28.
    response_put_wrong = client.put("books/TheSkyIsBlue", json=bad_payload)
    assert response_put_wrong.status_code == 422


# Test case is passed because pytest can figure out the input argument in line 32 is corresponding to the fixture that we defined.

# How it can get access to the data in the bad_payload function?
# pytest is a test framework so it can figure it out if you have defined something as test fixture. That is why you can make it available to your other test function's input argument.


def test_get_api(client, good_payload):
    response_get = client.get("books/TheSkyIsBlue")
    assert response_get.status_code == 404


def test_put_then_get_api(client, good_payload):
    response = client.put("books/TheSkyIsBlue", json=good_payload)
    assert response.status_code == 200
    response = client.get("books/TheSkyIsBlue")
    assert response.status_code == 200 and response.json() == good_payload


@pytest.mark.parametrize(
    "a, b, expected",
    [(1, 2, 3), (5, -1, 4), (3, 6, 9)],
)
def test_addition(
    a, b, expected
):  # In these line 70 and 71, you can do whatever you want here
    assert a + b == expected


# @pytest.mark.parametrize is a quick way for you to create a lot of test cases, a few tests input and output.
# First input argument inside parametrize decorator to provie what the input and output are, and provide them as strings.
# eg. "a, b, expected" -> create pre-test fixture on the fly with the parametrize helper.
# In the first test case, we have "a" as 1, "b" as 2, and "expected" as 3.
# What we try to test here whether "a" + "b" is equal to "expect".


@pytest.mark.parametrize(
    "payload, http_code",
    [
        (
            {
                "name": "The Sky is Blue",
                "author": {"name": "John Doe", "author_id": "JODO-1234"},
                "year_published": 2023,
            },
            200,
        ),
        (
            {
                "name": "What to eat today?",
                "author": {"name": "Alana Grey", "author_id": "ALGR-1234"},
                "year_published": 2024,
            },
            422,
        ),
    ]
    # ,
    # indirect=[
    #     "payload"
    # ],  # Tell us that we should be indirectly evaluating the good and bad payload because they are fixture themselves.
)
def test_many_put_api(payload, http_code, client):
    assert client.put("books/TheSkyIsBlue", json=payload).status_code == http_code
