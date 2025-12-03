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
    """Fixture for a list of mock candidates with test scores"""
    return [
        {
            "email": "alice@example.com",
            "full_name": "Alice Wonderland",
            "name": "Alice Wonderland",
            "percentage_score": 85,
            "score": 85,
            "test_id": 356098,
            "status": 2,  # Completed
            "completed_at": "2024-01-15T10:30:00Z"
        },
        {
            "email": "bob@example.com",
            "full_name": "Bob Builder",
            "name": "Bob Builder",
            "percentage_score": 65,
            "score": 65,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:00:00Z"
        },
        {
            "email": "charlie@example.com",
            "full_name": "Charlie Brown",
            "name": "Charlie Brown",
            "percentage_score": 75,
            "score": 75,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:30:00Z"
        },
        {
            "email": "diana@example.com",
            "full_name": "Diana Prince",
            "name": "Diana Prince",
            "percentage_score": 90,
            "score": 90,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T12:00:00Z"
        }
    ]


@pytest.fixture
def mock_candidates_with_advanced_scores():
    """Fixture for candidates who took both initial and advanced tests"""
    return [
        {
            "email": "alice@example.com",
            "full_name": "Alice Wonderland",
            "name": "Alice Wonderland",
            "percentage_score": 92,  # Advanced test score
            "score": 92,
            "test_id": 2263157,  # Advanced test ID
            "status": 2,
            "completed_at": "2024-01-16T10:00:00Z",
            "initial_test_score": 85  # Score from initial test
        },
        {
            "email": "charlie@example.com",
            "full_name": "Charlie Brown",
            "name": "Charlie Brown",
            "percentage_score": 78,  # Advanced test score
            "score": 78,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T11:00:00Z",
            "initial_test_score": 75
        },
        {
            "email": "diana@example.com",
            "full_name": "Diana Prince",
            "name": "Diana Prince",
            "percentage_score": 95,  # Advanced test score
            "score": 95,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T12:00:00Z",
            "initial_test_score": 90
        }
    ]


@pytest.fixture
def mock_candidates_with_various_scores():
    """Fixture for candidates with a wide range of test scores"""
    return [
        {
            "email": "excellent@example.com",
            "full_name": "Excellent Candidate",
            "name": "Excellent Candidate",
            "percentage_score": 98,
            "score": 98,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T09:00:00Z"
        },
        {
            "email": "good@example.com",
            "full_name": "Good Candidate",
            "name": "Good Candidate",
            "percentage_score": 82,
            "score": 82,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T09:30:00Z"
        },
        {
            "email": "average@example.com",
            "full_name": "Average Candidate",
            "name": "Average Candidate",
            "percentage_score": 72,
            "score": 72,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T10:00:00Z"
        },
        {
            "email": "borderline@example.com",
            "full_name": "Borderline Candidate",
            "name": "Borderline Candidate",
            "percentage_score": 69,
            "score": 69,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T10:30:00Z"
        },
        {
            "email": "poor@example.com",
            "full_name": "Poor Candidate",
            "name": "Poor Candidate",
            "percentage_score": 45,
            "score": 45,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:00:00Z"
        },
        {
            "email": "failed@example.com",
            "full_name": "Failed Candidate",
            "name": "Failed Candidate",
            "percentage_score": 35,
            "score": 35,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:30:00Z"
        }
    ]


@pytest.fixture
def mock_candidates_with_statuses():
    """Fixture for candidates with different test statuses"""
    return [
        {
            "email": "completed@example.com",
            "full_name": "Completed Test",
            "name": "Completed Test",
            "percentage_score": 85,
            "score": 85,
            "test_id": 356098,
            "status": 2,  # Completed
            "completed_at": "2024-01-15T10:00:00Z"
        },
        {
            "email": "in_progress@example.com",
            "full_name": "In Progress",
            "name": "In Progress",
            "percentage_score": None,
            "score": None,
            "test_id": 356098,
            "status": 1,  # In progress
            "completed_at": None
        },
        {
            "email": "not_started@example.com",
            "full_name": "Not Started",
            "name": "Not Started",
            "percentage_score": None,
            "score": None,
            "test_id": 356098,
            "status": 0,  # Not started
            "completed_at": None
        },
        {
            "email": "expired@example.com",
            "full_name": "Expired Test",
            "name": "Expired Test",
            "percentage_score": None,
            "score": None,
            "test_id": 356098,
            "status": -1,  # Expired
            "completed_at": None
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

