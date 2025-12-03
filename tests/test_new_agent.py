"""
Unit tests for new_agent.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import new_agent


class TestExtractScore:
    """Tests for extract_score function"""
    
    def test_extract_percentage_score(self, mock_candidate):
        """Test extracting percentage_score"""
        result = new_agent.extract_score(mock_candidate)
        assert result == 85.5
    
    def test_extract_regular_score(self):
        """Test extracting regular score when percentage_score not available"""
        candidate = {"score": 75, "email": "test@example.com"}
        result = new_agent.extract_score(candidate)
        assert result == 75
    
    def test_extract_no_score(self, mock_candidate_no_score):
        """Test extracting score when no score fields exist"""
        result = new_agent.extract_score(mock_candidate_no_score)
        assert result == 0
    
    def test_extract_score_prefers_percentage(self):
        """Test that percentage_score is preferred over score"""
        candidate = {"percentage_score": 85, "score": 75}
        result = new_agent.extract_score(candidate)
        assert result == 85
    
    def test_extract_score_none_values(self):
        """Test handling of None values"""
        candidate = {"percentage_score": None, "score": None}
        result = new_agent.extract_score(candidate)
        assert result == 0


class TestFilterPassed:
    """Tests for filter_passed function"""
    
    def test_filter_passed_candidates(self, mock_candidates_list):
        """Test filtering candidates above threshold"""
        passed = new_agent.filter_passed(mock_candidates_list, 70)
        assert len(passed) == 3
        assert all(c["percentage_score"] >= 70 for c in passed)
    
    def test_filter_all_passed(self, mock_candidates_list):
        """Test when all candidates pass"""
        passed = new_agent.filter_passed(mock_candidates_list, 60)
        assert len(passed) == 4
    
    def test_filter_none_passed(self, mock_candidates_list):
        """Test when no candidates pass"""
        passed = new_agent.filter_passed(mock_candidates_list, 95)
        assert len(passed) == 0
    
    def test_filter_exact_threshold(self):
        """Test filtering at exact threshold"""
        candidates = [
            {"percentage_score": 70},
            {"percentage_score": 69.9},
            {"percentage_score": 70.1}
        ]
        passed = new_agent.filter_passed(candidates, 70)
        assert len(passed) == 2
        assert passed[0]["percentage_score"] == 70
        assert passed[1]["percentage_score"] == 70.1
    
    def test_filter_empty_list(self):
        """Test filtering empty candidate list"""
        passed = new_agent.filter_passed([], 70)
        assert len(passed) == 0
    
    def test_filter_with_various_scores(self, mock_candidates_with_various_scores):
        """Test filtering with candidates having wide range of scores"""
        # Test with 70% threshold
        passed = new_agent.filter_passed(mock_candidates_with_various_scores, 70)
        assert len(passed) == 3  # excellent (98), good (82), average (72)
        assert all(c["percentage_score"] >= 70 for c in passed)
        
        # Test with 80% threshold
        passed_high = new_agent.filter_passed(mock_candidates_with_various_scores, 80)
        assert len(passed_high) == 2  # excellent (98), good (82)
        
        # Test with 50% threshold
        passed_low = new_agent.filter_passed(mock_candidates_with_various_scores, 50)
        assert len(passed_low) == 4  # All except failed (35)
    
    def test_filter_with_test_ids(self, mock_candidates_list):
        """Test that candidates have test_id information"""
        passed = new_agent.filter_passed(mock_candidates_list, 70)
        # Verify test_id is preserved
        assert all("test_id" in c for c in passed)
        assert all(c["test_id"] == 356098 for c in passed)


class TestGetCandidatesPage:
    """Tests for get_candidates_page function"""
    
    @patch('new_agent.requests.Session')
    def test_get_candidates_page_success(self, mock_session_class, mock_api_response_success):
        """Test successful API call to get candidates page"""
        mock_session = Mock()
        mock_session.get.return_value = mock_api_response_success
        mock_session_class.return_value = mock_session
        
        session = new_agent.make_session()
        result = new_agent.get_candidates_page(session, 12345, offset=0)
        
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["email"] == "test@example.com"
        mock_session.get.assert_called_once()
    
    @patch('new_agent.requests.Session')
    def test_get_candidates_page_failure(self, mock_session_class, mock_api_response_error):
        """Test API call failure handling"""
        mock_session = Mock()
        mock_session.get.return_value = mock_api_response_error
        mock_session_class.return_value = mock_session
        
        session = new_agent.make_session()
        
        with pytest.raises(Exception, match="Failed"):
            new_agent.get_candidates_page(session, 12345)
    
    @patch('new_agent.requests.Session')
    def test_get_candidates_page_with_offset(self, mock_session_class, mock_api_response_success):
        """Test getting candidates page with offset"""
        mock_session = Mock()
        mock_api_response_success.json.return_value = {
            "data": [{"email": "user2@example.com", "percentage_score": 80}],
            "next": None
        }
        mock_session.get.return_value = mock_api_response_success
        mock_session_class.return_value = mock_session
        
        session = new_agent.make_session()
        result = new_agent.get_candidates_page(session, 12345, offset=50)
        
        # Verify offset was passed in params
        call_args = mock_session.get.call_args
        assert call_args[1]["params"]["offset"] == 50
        assert call_args[1]["params"]["limit"] == 50


class TestGetAllCandidates:
    """Tests for get_all_candidates function"""
    
    @patch('new_agent.get_candidates_page')
    def test_get_all_candidates_single_page(self, mock_get_page):
        """Test getting all candidates from single page"""
        mock_get_page.return_value = {
            "data": [
                {"email": "user1@example.com", "percentage_score": 80},
                {"email": "user2@example.com", "percentage_score": 75}
            ],
            "next": None
        }
        
        session = Mock()
        result = new_agent.get_all_candidates(session, 12345)
        
        assert len(result) == 2
        assert mock_get_page.call_count == 1
    
    @patch('new_agent.get_candidates_page')
    def test_get_all_candidates_multiple_pages(self, mock_get_page):
        """Test getting all candidates across multiple pages"""
        # First page
        mock_get_page.side_effect = [
            {
                "data": [
                    {"email": f"user{i}@example.com", "percentage_score": 70 + i}
                    for i in range(3)
                ],
                "next": "offset=3"
            },
            {
                "data": [
                    {"email": f"user{i}@example.com", "percentage_score": 70 + i}
                    for i in range(3, 5)
                ],
                "next": None
            }
        ]
        
        session = Mock()
        result = new_agent.get_all_candidates(session, 12345)
        
        assert len(result) == 5
        assert mock_get_page.call_count == 2
    
    @patch('new_agent.get_candidates_page')
    def test_get_all_candidates_empty(self, mock_get_page):
        """Test getting all candidates when no candidates exist"""
        mock_get_page.return_value = {
            "data": [],
            "next": None
        }
        
        session = Mock()
        result = new_agent.get_all_candidates(session, 12345)
        
        assert len(result) == 0


class TestInviteToTest:
    """Tests for invite_to_test function"""
    
    @patch('new_agent.requests.Session')
    def test_invite_success(self, mock_session_class):
        """Test successful candidate invitation"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        candidate = {"email": "test@example.com", "full_name": "Test User"}
        session = new_agent.make_session()
        
        new_agent.invite_to_test(session, 12345, candidate)
        
        mock_session.post.assert_called_once()
        call_args = mock_session.post.call_args
        assert call_args[0][0] == "https://www.hackerrank.com/x/api/v3/tests/12345/invites"
        assert call_args[1]["json"]["email"] == "test@example.com"
        assert call_args[1]["json"]["send_email"] is True
    
    @patch('new_agent.requests.Session')
    def test_invite_success_201(self, mock_session_class):
        """Test successful invitation with 201 status"""
        mock_response = Mock()
        mock_response.status_code = 201
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        candidate = {"email": "test@example.com", "full_name": "Test User"}
        session = new_agent.make_session()
        
        new_agent.invite_to_test(session, 12345, candidate)
        
        mock_session.post.assert_called_once()
    
    @patch('new_agent.requests.Session')
    def test_invite_failure(self, mock_session_class):
        """Test invitation failure handling"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        candidate = {"email": "test@example.com", "full_name": "Test User"}
        session = new_agent.make_session()
        
        new_agent.invite_to_test(session, 12345, candidate)
        
        # Should not raise, just log error
        mock_session.post.assert_called_once()
    
    def test_invite_no_email(self, mock_candidate_no_email):
        """Test invitation when candidate has no email"""
        session = Mock()
        
        # Should return early without making API call
        new_agent.invite_to_test(session, 12345, mock_candidate_no_email)
        
        session.post.assert_not_called()
    
    @patch('new_agent.requests.Session')
    def test_invite_uses_name_fallback(self, mock_session_class):
        """Test that invite uses name field as fallback"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        candidate = {"email": "test@example.com", "name": "Test Name"}  # No full_name
        session = new_agent.make_session()
        
        new_agent.invite_to_test(session, 12345, candidate)
        
        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["name"] == "Test Name"
    
    @patch('new_agent.requests.Session')
    def test_invite_uses_default_name(self, mock_session_class):
        """Test that invite uses default name when neither full_name nor name exists"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        candidate = {"email": "test@example.com"}  # No name fields
        session = new_agent.make_session()
        
        new_agent.invite_to_test(session, 12345, candidate)
        
        call_args = mock_session.post.call_args
        assert call_args[1]["json"]["name"] == "Candidate"


class TestSendRecruiterInvite:
    """Tests for send_recruiter_invite function"""
    
    def test_send_recruiter_invite(self, mock_candidate):
        """Test sending recruiter invite"""
        # This function just logs, so we test it doesn't crash
        new_agent.send_recruiter_invite(mock_candidate)
        # If we get here without exception, test passes
    
    def test_send_recruiter_invite_no_name(self):
        """Test sending invite when candidate has no name"""
        candidate = {"email": "test@example.com"}
        new_agent.send_recruiter_invite(candidate)
        # Should handle None name gracefully


class TestMakeSession:
    """Tests for make_session function"""
    
    @patch('new_agent.requests.Session')
    @patch('new_agent.ACCESS_TOKEN', 'test_access_token')
    @patch('new_agent.API_TOKEN', 'test_api_token')
    @patch('new_agent.JWT_ACCESS_TOKEN', 'test_jwt_access')
    @patch('new_agent.JWT_REFRESH_TOKEN', 'test_jwt_refresh')
    def test_make_session_headers(self, mock_session_class):
        """Test that session is created with correct headers"""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        session = new_agent.make_session()
        
        assert session is not None
        mock_session.headers.update.assert_called_once()
        call_args = mock_session.headers.update.call_args[0][0]
        
        assert "Authorization" in call_args
        assert call_args["Authorization"] == "Bearer test_access_token"
        assert call_args["X-Auth-Token"] == "test_api_token"
        assert call_args["x-jwt-token"] == "test_jwt_access"
        assert call_args["x-refresh-token"] == "test_jwt_refresh"
        assert call_args["Accept"] == "application/json"
        assert call_args["Content-Type"] == "application/json"

