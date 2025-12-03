"""
Shared pytest fixtures for testing
"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_candidate():
    """Fixture for a mock candidate with all fields"""
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "name": "Test User",
        "percentage_score": 85.5,
        "score": 85
    }


@pytest.fixture
def mock_candidate_no_email():
    """Fixture for a candidate without email"""
    return {
        "full_name": "Test User",
        "percentage_score": 80
    }


@pytest.fixture
def mock_candidate_no_score():
    """Fixture for a candidate without score"""
    return {
        "email": "test@example.com",
        "full_name": "Test User"
    }


@pytest.fixture
def mock_candidates_list():
    """Fixture for a list of mock candidates"""
    return [
        {
            "email": "alice@example.com",
            "full_name": "Alice Wonderland",
            "percentage_score": 85
        },
        {
            "email": "bob@example.com",
            "full_name": "Bob Builder",
            "percentage_score": 65
        },
        {
            "email": "charlie@example.com",
            "full_name": "Charlie Brown",
            "percentage_score": 75
        },
        {
            "email": "diana@example.com",
            "full_name": "Diana Prince",
            "percentage_score": 90
        }
    ]


@pytest.fixture
def mock_session():
    """Fixture for a mock requests session"""
    session = Mock()
    return session


@pytest.fixture
def mock_api_response_success():
    """Fixture for a successful API response"""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "data": [
            {"email": "test@example.com", "percentage_score": 80}
        ],
        "next": None
    }
    response.text = '{"data": [], "next": null}'
    return response


@pytest.fixture
def mock_api_response_error():
    """Fixture for an error API response"""
    response = Mock()
    response.status_code = 401
    response.text = "Unauthorized"
    return response


@pytest.fixture
def mock_api_response_paginated():
    """Fixture for a paginated API response"""
    response_page1 = Mock()
    response_page1.status_code = 200
    response_page1.json.return_value = {
        "data": [{"email": f"user{i}@example.com", "percentage_score": 70 + i} for i in range(3)],
        "next": "offset=3"
    }
    
    response_page2 = Mock()
    response_page2.status_code = 200
    response_page2.json.return_value = {
        "data": [{"email": f"user{i}@example.com", "percentage_score": 70 + i} for i in range(3, 5)],
        "next": None
    }
    
    return [response_page1, response_page2]

