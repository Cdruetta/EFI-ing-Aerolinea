import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fixture simple que devuelve un APIClient de DRF"""
    return APIClient()
