import requests
import json
import pytest
import responses


url = "http://127.0.0.1:8000/companies/"


@pytest.mark.skip_ci
def test_zero_companies_agnostic() -> None:
    """Test companies list view returns empty json when no companies are added."""
    res = requests.get(url)

    assert res.status_code == 200
    assert json.loads(res.content) == []


@pytest.mark.skip_ci
def test_create_company_with_layoffs_agnostic() -> None:
    """Test creating company with layoffs status should succeed."""
    payload = {"name": "Amazon", "company_status": "Layoffs"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json=payload)

    res_content = json.loads(res.content)
    assert res.status_code == 201
    assert res_content.get("name") == "Amazon"
    assert res_content.get("company_status") == "Layoffs"

    clear_up_company(res_content["id"])


@pytest.mark.skip_ci
def clear_up_company(id: str) -> None:
    res = requests.delete(url + f"{id}")
    assert res.status_code == 204


COIN_API_KEY = (
    "7CF29EF2-BC24-4C4B-9103-2923CA9F98307CF29EF2-BC24-4C4B-9103-2923CA9F9830"
)


@pytest.mark.crypto
def test_check_price_doge() -> None:
    url = "https://api.coincap.io/v2/assets/dogecoin/"
    res = requests.get(url)
    res_data = json.loads(res.content)

    assert res.status_code == 200
    assert res_data["data"]["symbol"] == "DOGE"


@responses.activate
@pytest.mark.crypto
def test_check_price_doge_mock() -> None:
    url = "https://api.coincap.io/v2/assets/dogecoin/"
    responses.add(
        responses.GET,
        url=url,
        json={
            "data": {
                "id": "dogecoin",
                "rank": "8",
                "symbol": "DOGEDAN",
                "name": "Dogecoin",
                "supply": "138844516383.7052000000000000",
                "maxSupply": None,
                "marketCapUsd": "11423172486.7701807498868509",
                "volumeUsd24Hr": "417118872.5474328686758504",
                "priceUsd": "0.0822731266908774",
                "changePercent24Hr": "-4.6580842498944429",
                "vwap24Hr": "0.0839690210168146",
                "explorer": "http://dogechain.info/chain/Dogecoin",
            },
            "timestamp": 1680903045237,
        },
        status=200,
    )
    assert process_crypto() == 29

def process_crypto() -> int:
    url = "https://api.coincap.io/v2/assets/dogecoin/"
    res = requests.get(url)
    res_content = json.loads(res.content)

    if res.status_code != 200:
        raise ValueError('The website cannot be reached')

    if res_content['data']['symbol'] == "DOGEDAN":
        return 29
    return 42
