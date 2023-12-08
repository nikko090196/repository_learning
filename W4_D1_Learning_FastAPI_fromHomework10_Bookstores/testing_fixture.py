from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

#Put a first API (a obj) -> Tear down the object -> Use it to test our Get and Delete API



#no need to define the @pytest.fixture function because we are happy to go with default scope of pytest fixture.
@pytest.fixture
def good_payload():
    