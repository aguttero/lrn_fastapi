from fastapi.testclient import TestClient
import main # loads main.py file
from fastapi import status

client = TestClient(main.app)

def test_return_health_check():
    response = client.get("/healthy")
    print(f"status message= {response.raise_for_status()}")
    print(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'OK Healthy'}
