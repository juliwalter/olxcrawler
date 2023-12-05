"""
backend/validator.py

Contains the apps model validators
"""
from django.core.exceptions import ValidationError

import re

OLX_SEARCH_BASE_URL = "https://www.olx.pt/carros-motos-e-barcos/carros/"
PATTERN_MANUFACTURER = "([a-z]/){0,1}"


def validate_olx_url(url):
    """
    This validator validates whether the url follows the pattern for expected car search request on olx
    :param str url: the url to validate
    :rtype: None
    """
    olx_pattern = re.compile(OLX_SEARCH_BASE_URL + PATTERN_MANUFACTURER)
    if not olx_pattern.match(url):
        raise ValidationError(f"'{url}' does not follow the pattern of the OLX car search pattern.")
