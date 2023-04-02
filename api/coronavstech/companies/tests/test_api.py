from django.test import Client
from unittest import TestCase
import pytest
from django.shortcuts import reverse
from rest_framework import status

from companies.models import Company


company_list_url = reverse("companies-list")


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    """Base class for all the TestCases."""

    def setUp(self) -> None:
        self.client = Client()
        self.company_list_url = reverse("companies-list")


@pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    """Test companies list view returns empty json when no companies are added."""
    res = client.get(company_list_url)

    assert res.status_code == 200
    assert res.data == []


@pytest.mark.django_db
def test_one_company_exists_should_succeed(client) -> None:
    """Test returning one company if it exists in db."""
    amazon = Company.objects.create(name="Amazon")
    res = client.get(company_list_url)

    assert res.status_code == 200
    assert res.data[0]["name"] == amazon.name
    assert res.data[0]["company_status"] == amazon.company_status
    assert res.data[0]["note"] == amazon.note
    assert res.data[0]["link"] == amazon.link

    amazon.delete()


@pytest.mark.django_db
def test_create_company_with_empty_payload_should_fail(client) -> None:
    """Test creating a company with no name will raise an error."""
    res = client.post(company_list_url)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_create_existing_company_should_fail(client) -> None:
    """Test creating a company which already exists will raise an error."""
    Company.objects.create(name="Amazon")
    payload = {"name": "Amazon"}
    res = client.post(company_list_url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data == {"name": ["company with this name already exists."]}


@pytest.mark.django_db
def test_create_company_with_only_name_success(client) -> None:
    """Test creating a company providing only its name succeed."""
    payload = {"name": "Amazon"}
    res = client.post(company_list_url, payload)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == "Amazon"
    assert res.data["company_status"] == "Hiring"
    assert res.data["link"] == ""
    assert res.data["note"] == ""


@pytest.mark.django_db
def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    """Test creating company with layoffs status should succeed."""
    payload = {"name": "Amazon", "company_status": "Layoffs"}
    res = client.post(company_list_url, payload)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["name"] == "Amazon"
    assert res.data["company_status"] == "Layoffs"
    assert res.data["link"] == ""
    assert res.data["note"] == ""


@pytest.mark.django_db
def test_create_company_with_wrong_status_should_fail(client) -> None:
    """Test creating company with the wrong status will raise an error."""
    payload = {"name": "Amazon", "company_status": "Layoff"}
    res = client.post(company_list_url, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert "is not a valid choice." in str(res.data)
    assert "Layoff" in str(res.data)


def raise_covid19_exception() -> None:
    raise ValueError("Coronavirus Exception")


def test_raise_covid_exception_should_succeed() -> None:
    """Test the exception was raised."""
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "Coronavirus Exception" == str(e.value)


@pytest.mark.xfail
def test_xfail() -> None:
    assert 1 == 2


import logging


logger = logging.getLogger("CORONA_LOGS")


def funcion_that_logs_something() -> None:
    try:
        raise ValueError("Coronavirus Exception")
    except ValueError as e:
        logger.warning(f"I'm logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    funcion_that_logs_something()
    assert "I'm logging Coronavirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I'm logging info level.")
    assert "I'm logging info level." in caplog.text
