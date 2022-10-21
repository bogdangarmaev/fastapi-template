import pytest
from src.shared.api_client_utils import initialize_host


@pytest.mark.parametrize(
    "url_base,secure_connection,expected_url",
    [
        ("test-host", True, "https://test-host/"),
        ("test-host/", False, "http://test-host/"),
        pytest.param(
            "test-host", True, "http://test-host/", marks=pytest.mark.xfail
        ),
        pytest.param(
            "test-host/", False, "https://test-host/", marks=pytest.mark.xfail
        ),
    ],
)
def test_initialize_host(url_base, secure_connection, expected_url):
    host = initialize_host(url_base, secure_connection)
    assert host == expected_url
