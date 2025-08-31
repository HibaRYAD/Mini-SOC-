import os
import requests
import pytest

BASE_URL = os.environ.get("BASE_URL", "https://wazuh.lab")
API_URL = f"{BASE_URL}:55000"

@pytest.mark.timeout(10)
def test_wazuh_manager_api_reachable():
    try:
        resp = requests.get(API_URL, verify=False, timeout=8)
        assert resp.status_code in (200, 401)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Manager API unreachable: {e}")

