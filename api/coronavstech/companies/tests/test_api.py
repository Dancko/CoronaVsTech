from django.test import Client
from unittest import TestCase
import pytest
from django.shortcuts import reverse
from rest_framework import status

from companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    """Base class for all the TestCases."""

    def setUp(self) -> None:
        self.client = Client()
        self.company_list_url = reverse("companies-list")


class TestGetCompanies(BasicCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        """Test companies list view returns empty json when no companies are added."""
        res = self.client.get(self.company_list_url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 0)

    def test_one_company_exists_should_succeed(self) -> None:
        """Test returning one company if it exists in db."""
        amazon = Company.objects.create(name="Amazon")
        res = self.client.get(self.company_list_url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]["name"], amazon.name)
        self.assertEqual(res.data[0]["company_status"], amazon.company_status)
        self.assertEqual(res.data[0]["note"], amazon.note)
        self.assertEqual(res.data[0]["link"], amazon.link)

        amazon.delete()


class TestPostCompaniesBasicAPIs(BasicCompanyAPITestCase):
    def test_create_company_with_empty_payload_should_fail(self) -> None:
        """Test creating a company with no name will raise an error."""
        res = self.client.post(self.company_list_url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"name": ["This field is required."]})

    def test_create_existing_company_should_fail(self) -> None:
        """Test creating a company which already exists will raise an error."""
        amazon = Company.objects.create(name="Amazon")
        payload = {"name": "Amazon"}

        res = self.client.post(self.company_list_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"name": ["company with this name already exists."]})

    def test_create_company_with_only_name_success(self) -> None:
        """Test creating a company providing only its name succeed."""
        payload = {"name": "Amazon"}
        res = self.client.post(self.company_list_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Amazon")
        self.assertEqual(res.data["company_status"], "Hiring")
        self.assertEqual(res.data["link"], "")
        self.assertEqual(res.data["note"], "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        """Test creating company with layoffs status should succeed."""
        payload = {"name": "Amazon", "company_status": "Layoffs"}
        res = self.client.post(self.company_list_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "Amazon")
        self.assertEqual(res.data["company_status"], "Layoffs")
        self.assertEqual(res.data["link"], "")
        self.assertEqual(res.data["note"], "")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        """Test creating company with the wrong status will raise an error."""
        payload = {"name": "Amazon", "company_status": "Layoff"}
        res = self.client.post(self.company_list_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid choice.", str(res.data))
        self.assertIn("Layoff", str(res.data))


def raise_covid19_exception() -> None:
    raise ValueError("Coronavirus Exception")


def test_raise_covid_exception_should_succeed() -> None:
    """Test the exception was raised."""
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "Coronavirus Exception" == str(e.value)


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
