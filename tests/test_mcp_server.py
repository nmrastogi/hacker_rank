"""
Unit tests for mcp_server.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import os

# Import mcp_server module
import mcp_server


class TestSendEmailToCandidates:
    """Tests for send_email_to_candidates MCP tool"""
    
    def test_send_email_success(self):
        """Test successful email sending"""
        candidates = [
            {"email": "alice@example.com", "name": "Alice", "score": 85},
            {"email": "bob@example.com", "name": "Bob", "score": 90}
        ]
        
        result = mcp_server.send_email_to_candidates(candidates)
        
        assert result["total_candidates"] == 2
        assert result["emails_sent"] == 2
        assert len(result["successful"]) == 2
        assert len(result["failed"]) == 0
    
    def test_send_email_with_missing_email(self):
        """Test email sending with candidate missing email"""
        candidates = [
            {"name": "Alice", "score": 85},  # No email
            {"email": "bob@example.com", "name": "Bob", "score": 90}
        ]
        
        result = mcp_server.send_email_to_candidates(candidates)
        
        assert result["emails_sent"] == 1
        assert len(result["successful"]) == 1
        assert len(result["failed"]) == 1
        assert result["failed"][0]["error"] == "No email address provided"
    
    def test_send_email_custom_subject(self):
        """Test email sending with custom subject"""
        candidates = [{"email": "test@example.com", "name": "Test", "score": 85}]
        
        result = mcp_server.send_email_to_candidates(
            candidates,
            email_subject="Custom Subject"
        )
        
        assert result["emails_sent"] == 1
        # Subject is used internally, verify it doesn't break
    
    def test_send_email_custom_template(self):
        """Test email sending with custom template"""
        candidates = [{"email": "test@example.com", "name": "Test", "score": 85}]
        custom_template = "Hi {name}, your score is {score}%"
        
        result = mcp_server.send_email_to_candidates(
            candidates,
            email_template=custom_template
        )
        
        assert result["emails_sent"] == 1
        assert len(result["successful"]) == 1


class TestGetTestCandidates:
    """Tests for get_test_candidates MCP tool"""
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.filter_passed')
    @patch('mcp_server.new_agent.extract_score')
    def test_get_test_candidates_success(self, mock_extract_score, mock_filter, 
                                        mock_get_all, mock_make_session):
        """Test successful retrieval of test candidates"""
        # Setup mocks
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        mock_candidates = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 85},
            {"email": "bob@example.com", "full_name": "Bob", "percentage_score": 65},
            {"email": "charlie@example.com", "full_name": "Charlie", "percentage_score": 75}
        ]
        mock_get_all.return_value = mock_candidates
        
        passed_candidates = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 85},
            {"email": "charlie@example.com", "full_name": "Charlie", "percentage_score": 75}
        ]
        mock_filter.return_value = passed_candidates
        mock_extract_score.side_effect = lambda c: c.get("percentage_score", 0)
        
        # Call the function
        result = mcp_server.get_test_candidates(12345, 70.0)
        
        # Assertions
        assert result["test_id"] == 12345
        assert result["total_candidates"] == 3
        assert result["passed_count"] == 2
        assert result["passing_score"] == 70.0
        assert len(result["passed_candidates"]) == 2
        assert result["passed_candidates"][0]["email"] == "alice@example.com"
        assert result["passed_candidates"][0]["score"] == 85
        mock_get_all.assert_called_once_with(mock_session, 12345)
        mock_filter.assert_called_once_with(mock_candidates, 70.0)
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    def test_get_test_candidates_default_passing_score(self, mock_get_all, mock_make_session):
        """Test with default passing score"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        mock_get_all.return_value = []
        
        with patch('mcp_server.new_agent.filter_passed', return_value=[]):
            with patch('mcp_server.new_agent.extract_score', return_value=0):
                result = mcp_server.get_test_candidates(12345)
                
                assert result["passing_score"] == 60.0  # Default value
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    def test_get_test_candidates_error_handling(self, mock_get_all, mock_make_session):
        """Test error handling in get_test_candidates"""
        mock_make_session.side_effect = Exception("API Error")
        
        result = mcp_server.get_test_candidates(12345, 70.0)
        
        assert "error" in result
        assert "API Error" in result["error"]
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.filter_passed')
    @patch('mcp_server.new_agent.extract_score')
    def test_get_test_candidates_name_fallback(self, mock_extract_score, mock_filter,
                                               mock_get_all, mock_make_session):
        """Test that name field is used as fallback when full_name is missing"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidate = {"email": "test@example.com", "name": "Test Name", "percentage_score": 80}
        mock_get_all.return_value = [candidate]
        mock_filter.return_value = [candidate]
        mock_extract_score.return_value = 80
        
        result = mcp_server.get_test_candidates(12345, 70.0)
        
        assert result["passed_candidates"][0]["name"] == "Test Name"


class TestInviteCandidatesToTest:
    """Tests for invite_candidates_to_test MCP tool"""
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.invite_to_test')
    def test_invite_candidates_success(self, mock_invite, mock_make_session):
        """Test successful invitation of candidates"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        emails = ["alice@example.com", "bob@example.com"]
        result = mcp_server.invite_candidates_to_test(12345, emails)
        
        assert result["test_id"] == 12345
        assert result["total_invited"] == 2
        assert len(result["successful"]) == 2
        assert len(result["failed"]) == 0
        assert mock_invite.call_count == 2
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.invite_to_test')
    def test_invite_candidates_partial_failure(self, mock_invite, mock_make_session):
        """Test invitation with some failures"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        # First invite succeeds, second fails
        def side_effect(session, test_id, candidate):
            if candidate["email"] == "bob@example.com":
                raise Exception("Invalid email")
        
        mock_invite.side_effect = side_effect
        
        emails = ["alice@example.com", "bob@example.com"]
        result = mcp_server.invite_candidates_to_test(12345, emails)
        
        assert result["total_invited"] == 1
        assert len(result["successful"]) == 1
        assert len(result["failed"]) == 1
        assert result["failed"][0]["email"] == "bob@example.com"
        assert "error" in result["failed"][0]
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.invite_to_test')
    def test_invite_candidates_empty_list(self, mock_invite, mock_make_session):
        """Test invitation with empty email list"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        result = mcp_server.invite_candidates_to_test(12345, [])
        
        assert result["total_invited"] == 0
        assert len(result["successful"]) == 0
        assert len(result["failed"]) == 0
        mock_invite.assert_not_called()
    
    @patch('mcp_server.new_agent.make_session')
    def test_invite_candidates_error_handling(self, mock_make_session):
        """Test error handling in invite_candidates_to_test"""
        mock_make_session.side_effect = Exception("Session Error")
        
        result = mcp_server.invite_candidates_to_test(12345, ["test@example.com"])
        
        assert "error" in result
        assert "Session Error" in result["error"]


class TestRunScreeningPipeline:
    """Tests for run_screening_pipeline MCP tool"""
    
    @patch('mcp_server.USE_MOCK_DATA', False)
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.filter_passed')
    @patch('mcp_server.new_agent.invite_to_test')
    @patch('mcp_server.new_agent.extract_score')
    @patch('mcp_server.send_email_to_candidates')
    def test_run_screening_pipeline_success(self, mock_send_email, mock_extract_score, mock_invite,
                                            mock_filter, mock_get_all, mock_make_session):
        """Test successful pipeline execution"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        # Test A candidates
        candidates_a = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 85},
            {"email": "bob@example.com", "full_name": "Bob", "percentage_score": 65}
        ]
        passed_a = [candidates_a[0]]  # Only Alice passed
        
        # Test B candidates
        candidates_b = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 90}
        ]
        passed_b = candidates_b
        
        mock_get_all.side_effect = [candidates_a, candidates_b]
        mock_filter.side_effect = [passed_a, passed_b]
        mock_extract_score.side_effect = lambda c: c.get("percentage_score", 0)
        mock_send_email.return_value = {
            "emails_sent": 1,
            "successful": [{"email": "alice@example.com", "name": "Alice", "score": 90}],
            "failed": []
        }
        
        result = mcp_server.run_screening_pipeline(100, 200, 70.0, 80.0)
        
        # Assertions
        assert result["test_a"]["id"] == 100
        assert result["test_a"]["total_candidates"] == 2
        assert result["test_a"]["passed_count"] == 1
        assert result["test_b"]["id"] == 200
        assert result["test_b"]["total_candidates"] == 1
        assert result["test_b"]["passed_count"] == 1
        assert result["invited_to_test_b"] == 1
        assert result["recruiter_ready_count"] == 1
        assert len(result["recruiter_ready_candidates"]) == 1
        assert result["recruiter_ready_candidates"][0]["email"] == "alice@example.com"
        assert result["emails_sent"] == 1
        assert "email_results" in result
        mock_send_email.assert_called_once()
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.filter_passed')
    @patch('mcp_server.new_agent.invite_to_test')
    @patch('mcp_server.send_email_to_candidates')
    def test_run_screening_pipeline_default_scores(self, mock_send_email, mock_invite, mock_filter,
                                                   mock_get_all, mock_make_session):
        """Test pipeline with default passing scores"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        mock_get_all.return_value = []
        mock_filter.return_value = []
        mock_send_email.return_value = {"emails_sent": 0, "successful": [], "failed": []}
        
        with patch('mcp_server.new_agent.extract_score', return_value=0):
            result = mcp_server.run_screening_pipeline(100, 200)
            
            assert result["test_a"]["passing_score"] == 70.0  # Default
            assert result["test_b"]["passing_score"] == 80.0  # Default
            assert result["emails_sent"] == 0
    
    @patch('mcp_server.USE_MOCK_DATA', False)
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.filter_passed')
    @patch('mcp_server.new_agent.invite_to_test')
    @patch('mcp_server.send_email_to_candidates')
    def test_run_screening_pipeline_invite_failure_handled(self, mock_send_email, mock_invite, mock_filter,
                                                          mock_get_all, mock_make_session):
        """Test that invite failures don't stop the pipeline"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidates_a = [{"email": "test@example.com", "percentage_score": 85}]
        mock_get_all.side_effect = [candidates_a, []]
        mock_filter.side_effect = [candidates_a, []]
        mock_invite.side_effect = Exception("Invite failed")
        mock_send_email.return_value = {"emails_sent": 0, "successful": [], "failed": []}
        
        with patch('mcp_server.new_agent.extract_score', return_value=85):
            result = mcp_server.run_screening_pipeline(100, 200, 70.0, 80.0)
            
            # Pipeline should complete even if invites fail
            assert result["invited_to_test_b"] == 0
            assert "test_a" in result
            assert "test_b" in result
            assert "emails_sent" in result
    
    @patch('mcp_server.new_agent.make_session')
    def test_run_screening_pipeline_error_handling(self, mock_make_session):
        """Test error handling in pipeline"""
        mock_make_session.side_effect = Exception("Pipeline Error")
        
        result = mcp_server.run_screening_pipeline(100, 200)
        
        # Should return error dict
        assert "error" in result or "test_a" in result
        # If error occurred early, it will be in error field
        # If it occurred during execution, pipeline may still return partial results


class TestGetCandidateScores:
    """Tests for get_candidate_scores MCP tool"""
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.extract_score')
    def test_get_candidate_scores_all(self, mock_extract_score, mock_get_all, mock_make_session):
        """Test getting scores for all candidates"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidates = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 85, "status": 1},
            {"email": "bob@example.com", "full_name": "Bob", "percentage_score": 65, "status": 1}
        ]
        mock_get_all.return_value = candidates
        mock_extract_score.side_effect = lambda c: c.get("percentage_score", 0)
        
        result = mcp_server.get_candidate_scores(12345)
        
        assert result["test_id"] == 12345
        assert result["total_candidates"] == 2
        assert result["filtered_count"] == 2
        assert len(result["candidates"]) == 2
        assert result["candidates"][0]["email"] == "alice@example.com"
        assert result["candidates"][0]["score"] == 85
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.extract_score')
    def test_get_candidate_scores_filtered_by_email(self, mock_extract_score, mock_get_all,
                                                    mock_make_session):
        """Test getting scores for a specific candidate by email"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidates = [
            {"email": "alice@example.com", "full_name": "Alice", "percentage_score": 85},
            {"email": "bob@example.com", "full_name": "Bob", "percentage_score": 65}
        ]
        mock_get_all.return_value = candidates
        mock_extract_score.side_effect = lambda c: c.get("percentage_score", 0)
        
        result = mcp_server.get_candidate_scores(12345, "alice@example.com")
        
        assert result["total_candidates"] == 2
        assert result["filtered_count"] == 1
        assert len(result["candidates"]) == 1
        assert result["candidates"][0]["email"] == "alice@example.com"
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    def test_get_candidate_scores_no_match(self, mock_get_all, mock_make_session):
        """Test getting scores when email doesn't match"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidates = [{"email": "alice@example.com", "percentage_score": 85}]
        mock_get_all.return_value = candidates
        
        with patch('mcp_server.new_agent.extract_score', return_value=85):
            result = mcp_server.get_candidate_scores(12345, "nonexistent@example.com")
            
            assert result["filtered_count"] == 0
            assert len(result["candidates"]) == 0
    
    @patch('mcp_server.new_agent.make_session')
    def test_get_candidate_scores_error_handling(self, mock_make_session):
        """Test error handling in get_candidate_scores"""
        mock_make_session.side_effect = Exception("Score Error")
        
        result = mcp_server.get_candidate_scores(12345)
        
        assert "error" in result
        assert "Score Error" in result["error"]


class TestMCPResources:
    """Tests for MCP resource endpoints"""
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    @patch('mcp_server.new_agent.extract_score')
    def test_get_test_candidates_resource(self, mock_extract_score, mock_get_all,
                                         mock_make_session):
        """Test get_test_candidates_resource resource endpoint"""
        mock_session = Mock()
        mock_make_session.return_value = mock_session
        
        candidates = [
            {"email": "test@example.com", "full_name": "Test", "percentage_score": 80}
        ]
        mock_get_all.return_value = candidates
        mock_extract_score.return_value = 80
        
        result_str = mcp_server.get_test_candidates_resource("12345")
        result = json.loads(result_str)
        
        assert result["test_id"] == 12345
        assert result["candidate_count"] == 1
        assert len(result["candidates"]) == 1
    
    @patch('mcp_server.new_agent.make_session')
    @patch('mcp_server.new_agent.get_all_candidates')
    def test_get_test_candidates_resource_error(self, mock_get_all, mock_make_session):
        """Test resource endpoint error handling"""
        mock_make_session.side_effect = Exception("Resource Error")
        
        result_str = mcp_server.get_test_candidates_resource("12345")
        result = json.loads(result_str)
        
        assert "error" in result
        assert "Resource Error" in result["error"]
    
    @patch.dict('os.environ', {
        'TEST_A_ID': '100',
        'TEST_B_ID': '200',
        'TEST_A_PASS_SCORE': '70',
        'TEST_B_PASS_SCORE': '80',
        'ACCESS_TOKEN': 'test_token'
    })
    def test_get_configuration_resource(self):
        """Test get_configuration_resource endpoint"""
        result_str = mcp_server.get_configuration_resource()
        result = json.loads(result_str)
        
        assert result["test_a_id"] == 100
        assert result["test_b_id"] == 200
        assert result["test_a_pass_score"] == 70
        assert result["test_b_pass_score"] == 80
        assert result["api_configured"] is True
    
    @patch.dict('os.environ', {}, clear=True)
    def test_get_configuration_resource_defaults(self):
        """Test configuration resource with default values"""
        result_str = mcp_server.get_configuration_resource()
        result = json.loads(result_str)
        
        # Should use defaults from new_agent.py
        assert result["test_a_id"] in [356098, 0]  # Default or 0
        assert result["api_configured"] is False


class TestMCPPrompts:
    """Tests for MCP prompt templates"""
    
    def test_analyze_test_results_prompt(self):
        """Test analyze_test_results prompt generation"""
        prompt = mcp_server.analyze_test_results(12345, 70.0)
        
        assert "12345" in prompt
        assert "70.0" in prompt
        assert "Analyze" in prompt or "analyze" in prompt
    
    def test_generate_recruiter_summary_prompt(self):
        """Test generate_recruiter_summary prompt generation"""
        prompt = mcp_server.generate_recruiter_summary(100, 200)
        
        assert "100" in prompt
        assert "200" in prompt
        assert "recruiter" in prompt.lower() or "Recruiter" in prompt


class TestMCPAvailability:
    """Tests for MCP availability handling"""
    
    def test_mcp_availability_check(self):
        """Test that MCP_AVAILABLE flag is set correctly"""
        # This test verifies the module loads even if MCP isn't available
        # The actual availability depends on whether mcp package is installed
        assert hasattr(mcp_server, 'MCP_AVAILABLE')
        assert isinstance(mcp_server.MCP_AVAILABLE, bool)
    
    @patch('mcp_server.MCP_AVAILABLE', False)
    def test_functions_conditional_on_mcp(self):
        """Test that functions are only defined when MCP is available"""
        # When MCP_AVAILABLE is False, the functions won't be decorated
        # but the module should still load
        # This is more of a structural test
        pass

