import pytest
from django.shortcuts import reverse


url = f'{reverse("fibonacci")}'


def test_get_request_with_args_is_success(client) -> None:
    """Test get request with args returns the nth number of fibs."""
    res = client.get(url + "?n=5")

    assert res.status_code == 200
    assert res.data == {"The 5th fibonacci number": "5"}


def test_get_request_with_no_args_returns_error(client) -> None:
    """Test get request with no args returns response with no data."""
    res = client.get(url)

    assert res.status_code == 400
    assert res.data == {"Error": "No data has been provided."}


@pytest.mark.parametrize("n", ["fibonacci", -1])
def test_get_request_with_invalid_args_returns_error(client, n) -> None:
    """Test get request with invalid args returns an error."""
    res = client.get(url + f"?n={n}")

    assert res.status_code == 400
    assert res.data == {"Error": f"{n} is incorrect data."}


# def test_post_request_should_fail(client):
#     """Test post request should fail."""
#     res = client.post(url + '?n=5')
#
#     assert res.status_code == 405
#     assert res.data["detail"] == 'Method "POST" not allowed.'


@pytest.mark.skip
@pytest.mark.parametrize("n", [i for i in range(1, 1000)])
def test_stress(client, n: int) -> None:
    """Stress test for fibonacci endpoint."""
    res = client.get(url + f"?n={n}")

    assert res.status_code == 200
