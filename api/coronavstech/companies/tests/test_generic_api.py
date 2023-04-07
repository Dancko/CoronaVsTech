import requests
import json
import pytest


url = 'http://127.0.0.1:8000/companies/'


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
    res = requests.delete(url + f'{id}')
    assert res.status_code == 204
