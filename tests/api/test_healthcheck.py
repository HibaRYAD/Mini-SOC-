import requests

def test_wazuh_manager_health():
    url = "https://wazuh.lab:55000"
    try:
        r = requests.get(url, verify=False, timeout=5)
        assert r.status_code in [200, 401]  # 401 = expected if auth required
    except Exception as e:
        raise AssertionError(f"Healthcheck failed: {e}")
