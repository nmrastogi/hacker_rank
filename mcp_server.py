"""
MCP Server for HackerRank Candidate Screening Agent

This server exposes the agent's functionality as MCP tools that can be called
by AI assistants and other MCP clients.
"""

import os
import json
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agent functions
import new_agent

# ===========================================================
# MOCK CANDIDATES DATA - For testing/demo without real API
# ===========================================================

MOCK_CANDIDATES_DATA = {
    # Initial Test (Test A) - Test ID: 356098
    356098: [
        {
            "email": "alice.wonderland@example.com",
            "full_name": "Alice Wonderland",
            "name": "Alice Wonderland",
            "percentage_score": 85,
            "score": 85,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T10:30:00Z"
        },
        {
            "email": "bob.builder@example.com",
            "full_name": "Bob Builder",
            "name": "Bob Builder",
            "percentage_score": 65,
            "score": 65,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:00:00Z"
        },
        {
            "email": "charlie.brown@example.com",
            "full_name": "Charlie Brown",
            "name": "Charlie Brown",
            "percentage_score": 75,
            "score": 75,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T11:30:00Z"
        },
        {
            "email": "diana.prince@example.com",
            "full_name": "Diana Prince",
            "name": "Diana Prince",
            "percentage_score": 90,
            "score": 90,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T12:00:00Z"
        },
        {
            "email": "emma.watson@example.com",
            "full_name": "Emma Watson",
            "name": "Emma Watson",
            "percentage_score": 88,
            "score": 88,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T12:30:00Z"
        },
        {
            "email": "frank.sinatra@example.com",
            "full_name": "Frank Sinatra",
            "name": "Frank Sinatra",
            "percentage_score": 72,
            "score": 72,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T13:00:00Z"
        },
        {
            "email": "grace.hopper@example.com",
            "full_name": "Grace Hopper",
            "name": "Grace Hopper",
            "percentage_score": 95,
            "score": 95,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T13:30:00Z"
        },
        {
            "email": "henry.ford@example.com",
            "full_name": "Henry Ford",
            "name": "Henry Ford",
            "percentage_score": 68,
            "score": 68,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T14:00:00Z"
        },
        {
            "email": "isabella.swan@example.com",
            "full_name": "Isabella Swan",
            "name": "Isabella Swan",
            "percentage_score": 79,
            "score": 79,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T14:30:00Z"
        },
        {
            "email": "jack.sparrow@example.com",
            "full_name": "Jack Sparrow",
            "name": "Jack Sparrow",
            "percentage_score": 55,
            "score": 55,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T15:00:00Z"
        },
        {
            "email": "katherine.johnson@example.com",
            "full_name": "Katherine Johnson",
            "name": "Katherine Johnson",
            "percentage_score": 92,
            "score": 92,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T15:30:00Z"
        },
        {
            "email": "leonardo.davinci@example.com",
            "full_name": "Leonardo da Vinci",
            "name": "Leonardo da Vinci",
            "percentage_score": 87,
            "score": 87,
            "test_id": 356098,
            "status": 2,
            "completed_at": "2024-01-15T16:00:00Z"
        }
    ],
    
    # Advanced Test (Test B) - Test ID: 2263157
    2263157: [
        {
            "email": "alice.wonderland@example.com",
            "full_name": "Alice Wonderland",
            "name": "Alice Wonderland",
            "percentage_score": 92,
            "score": 92,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T10:00:00Z"
        },
        {
            "email": "charlie.brown@example.com",
            "full_name": "Charlie Brown",
            "name": "Charlie Brown",
            "percentage_score": 78,
            "score": 78,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T11:00:00Z"
        },
        {
            "email": "diana.prince@example.com",
            "full_name": "Diana Prince",
            "name": "Diana Prince",
            "percentage_score": 95,
            "score": 95,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T12:00:00Z"
        },
        {
            "email": "emma.watson@example.com",
            "full_name": "Emma Watson",
            "name": "Emma Watson",
            "percentage_score": 89,
            "score": 89,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T12:30:00Z"
        },
        {
            "email": "grace.hopper@example.com",
            "full_name": "Grace Hopper",
            "name": "Grace Hopper",
            "percentage_score": 98,
            "score": 98,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T13:00:00Z"
        },
        {
            "email": "isabella.swan@example.com",
            "full_name": "Isabella Swan",
            "name": "Isabella Swan",
            "percentage_score": 82,
            "score": 82,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T13:30:00Z"
        },
        {
            "email": "katherine.johnson@example.com",
            "full_name": "Katherine Johnson",
            "name": "Katherine Johnson",
            "percentage_score": 96,
            "score": 96,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T14:00:00Z"
        },
        {
            "email": "leonardo.davinci@example.com",
            "full_name": "Leonardo da Vinci",
            "name": "Leonardo da Vinci",
            "percentage_score": 91,
            "score": 91,
            "test_id": 2263157,
            "status": 2,
            "completed_at": "2024-01-16T14:30:00Z"
        }
    ]
}

# Check if we should use mock data
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"

# Mock test metadata
MOCK_TESTS_INFO = {
    356098: {
        "id": 356098,
        "name": "Initial Screening Test",
        "type": "initial",
        "candidate_count": 12,
        "description": "Initial candidate screening assessment"
    },
    2263157: {
        "id": 2263157,
        "name": "Advanced Technical Test",
        "type": "advanced",
        "candidate_count": 8,
        "description": "Advanced technical assessment for qualified candidates"
    }
}


def get_mock_candidates(test_id: int) -> List[Dict[str, Any]]:
    """Get mock candidates for a test ID"""
    return MOCK_CANDIDATES_DATA.get(test_id, [])


def get_mock_tests() -> List[Dict[str, Any]]:
    """Get list of all mock tests"""
    return list(MOCK_TESTS_INFO.values())


# Try to import MCP
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP package not installed. Install with: pip install 'mcp[cli]'")
    print("The server will not function without MCP installed.")

if MCP_AVAILABLE:
    # Initialize MCP server
    mcp = FastMCP("HackerRank Candidate Screening Agent")

    # ===========================================================
    # MCP TOOLS - Expose agent functions as callable tools
    # ===========================================================

    @mcp.tool()
    def get_test_candidates(test_id: int, passing_score: float = 60.0) -> Dict[str, Any]:
        """
        Get candidates who passed a specific test.
        
        Args:
            test_id: The HackerRank test ID
            passing_score: Minimum score required to pass (default: 60.0)
        
        Returns:
            Dictionary with candidate count and list of passed candidates
        """
        try:
            if USE_MOCK_DATA:
                all_candidates = get_mock_candidates(test_id)
            else:
                session = new_agent.make_session()
                all_candidates = new_agent.get_all_candidates(session, test_id)
            
            passed_candidates = new_agent.filter_passed(all_candidates, passing_score)
            
            return {
                "test_id": test_id,
                "total_candidates": len(all_candidates),
                "passed_count": len(passed_candidates),
                "passing_score": passing_score,
                "passed_candidates": [
                    {
                        "email": c.get("email"),
                        "name": c.get("full_name") or c.get("name"),
                        "score": new_agent.extract_score(c)
                    }
                    for c in passed_candidates
                ],
                "mock_data": USE_MOCK_DATA
            }
        except Exception as e:
            return {"error": str(e)}


    @mcp.tool()
    def invite_candidates_to_test(test_id: int, candidate_emails: List[str]) -> Dict[str, Any]:
        """
        Invite candidates to a test by their email addresses.
        
        Args:
            test_id: The HackerRank test ID to invite candidates to
            candidate_emails: List of candidate email addresses
        
        Returns:
            Dictionary with invitation results
        """
        try:
            if USE_MOCK_DATA:
                # In mock mode, just return success
                results = {
                    "test_id": test_id,
                    "total_invited": len(candidate_emails),
                    "successful": candidate_emails,
                    "failed": [],
                    "mock_data": True
                }
                return results
            
            session = new_agent.make_session()
            results = {
                "test_id": test_id,
                "total_invited": 0,
                "successful": [],
                "failed": [],
                "mock_data": False
            }
            
            for email in candidate_emails:
                candidate = {"email": email, "name": email.split("@")[0]}
                try:
                    new_agent.invite_to_test(session, test_id, candidate)
                    results["successful"].append(email)
                    results["total_invited"] += 1
                except Exception as e:
                    results["failed"].append({"email": email, "error": str(e)})
            
            return results
        except Exception as e:
            return {"error": str(e)}


    @mcp.tool()
    def run_screening_pipeline(
        test_a_id: int,
        test_b_id: int,
        test_a_pass_score: float = 70.0,
        test_b_pass_score: float = 80.0
    ) -> Dict[str, Any]:
        """
        Run the complete candidate screening pipeline.
        
        This tool:
        1. Gets candidates from Test A
        2. Filters those who passed
        3. Invites them to Test B
        4. Gets Test B results
        5. Filters those who passed Test B
        6. Returns list ready for recruiter calls
        
        Args:
            test_a_id: Initial screening test ID
            test_b_id: Advanced test ID
            test_a_pass_score: Minimum score to pass Test A (default: 70.0)
            test_b_pass_score: Minimum score to pass Test B (default: 80.0)
        
        Returns:
            Dictionary with pipeline results
        """
        try:
            if USE_MOCK_DATA:
                # Use mock data
                candidates_a = get_mock_candidates(test_a_id)
                passed_a = new_agent.filter_passed(candidates_a, test_a_pass_score)
                
                # Get Test B candidates (some from Test A may have taken Test B)
                candidates_b = get_mock_candidates(test_b_id)
                passed_b = new_agent.filter_passed(candidates_b, test_b_pass_score)
                
                # Prepare recruiter-ready list
                recruiter_ready = [
                    {
                        "email": c.get("email"),
                        "name": c.get("full_name") or c.get("name"),
                        "score": new_agent.extract_score(c),
                        "test_a_score": next(
                            (new_agent.extract_score(ca) for ca in candidates_a 
                             if ca.get("email") == c.get("email")), 
                            None
                        )
                    }
                    for c in passed_b
                ]
                
                return {
                    "test_a": {
                        "id": test_a_id,
                        "total_candidates": len(candidates_a),
                        "passed_count": len(passed_a),
                        "passing_score": test_a_pass_score
                    },
                    "test_b": {
                        "id": test_b_id,
                        "total_candidates": len(candidates_b),
                        "passed_count": len(passed_b),
                        "passing_score": test_b_pass_score
                    },
                    "invited_to_test_b": len(passed_a),
                    "recruiter_ready_count": len(recruiter_ready),
                    "recruiter_ready_candidates": recruiter_ready,
                    "mock_data": True
                }
            
            session = new_agent.make_session()
            
            # Step 1: Get Test A candidates
            candidates_a = new_agent.get_all_candidates(session, test_a_id)
            passed_a = new_agent.filter_passed(candidates_a, test_a_pass_score)
            
            # Step 2: Invite to Test B
            invited_count = 0
            for candidate in passed_a:
                try:
                    new_agent.invite_to_test(session, test_b_id, candidate)
                    invited_count += 1
                except Exception:
                    pass
            
            # Step 3: Get Test B candidates
            candidates_b = new_agent.get_all_candidates(session, test_b_id)
            passed_b = new_agent.filter_passed(candidates_b, test_b_pass_score)
            
            # Step 4: Prepare recruiter-ready list
            recruiter_ready = [
                {
                    "email": c.get("email"),
                    "name": c.get("full_name") or c.get("name"),
                    "score": new_agent.extract_score(c),
                    "test_a_score": next(
                        (new_agent.extract_score(ca) for ca in candidates_a 
                         if ca.get("email") == c.get("email")), 
                        None
                    )
                }
                for c in passed_b
            ]
            
            return {
                "test_a": {
                    "id": test_a_id,
                    "total_candidates": len(candidates_a),
                    "passed_count": len(passed_a),
                    "passing_score": test_a_pass_score
                },
                "test_b": {
                    "id": test_b_id,
                    "total_candidates": len(candidates_b),
                    "passed_count": len(passed_b),
                    "passing_score": test_b_pass_score
                },
                "invited_to_test_b": invited_count,
                "recruiter_ready_count": len(recruiter_ready),
                "recruiter_ready_candidates": recruiter_ready,
                "mock_data": False
            }
        except Exception as e:
            return {"error": str(e)}


    @mcp.tool()
    def list_all_tests() -> Dict[str, Any]:
        """
        List all available tests in the system.
        
        Returns:
            Dictionary with list of all available tests, including test IDs, names, 
            candidate counts, and descriptions.
        """
        try:
            if USE_MOCK_DATA:
                # Return mock tests
                tests = get_mock_tests()
                # Add candidate counts from actual data
                for test in tests:
                    candidates = get_mock_candidates(test["id"])
                    test["candidate_count"] = len(candidates)
                    # Calculate average score
                    if candidates:
                        scores = [new_agent.extract_score(c) for c in candidates]
                        test["average_score"] = round(sum(scores) / len(scores), 2)
                        test["min_score"] = min(scores)
                        test["max_score"] = max(scores)
                    else:
                        test["average_score"] = None
                        test["min_score"] = None
                        test["max_score"] = None
                
                return {
                    "total_tests": len(tests),
                    "tests": tests,
                    "mock_data": True
                }
            else:
                # Try to get tests from API
                # Note: This requires HackerRank API endpoint for listing tests
                # For now, return configured tests from environment
                test_a_id = int(os.getenv("TEST_A_ID", "0")) or 356098
                test_b_id = int(os.getenv("TEST_B_ID", "0")) or 2263157
                
                session = new_agent.make_session()
                tests = []
                
                # Try to get candidate counts for each test
                for test_id in [test_a_id, test_b_id]:
                    try:
                        candidates = new_agent.get_all_candidates(session, test_id)
                        test_info = {
                            "id": test_id,
                            "name": f"Test {test_id}",
                            "type": "configured",
                            "candidate_count": len(candidates),
                            "description": f"HackerRank test {test_id}"
                        }
                        
                        # Calculate statistics if candidates exist
                        if candidates:
                            scores = [new_agent.extract_score(c) for c in candidates if new_agent.extract_score(c) > 0]
                            if scores:
                                test_info["average_score"] = round(sum(scores) / len(scores), 2)
                                test_info["min_score"] = min(scores)
                                test_info["max_score"] = max(scores)
                        
                        tests.append(test_info)
                    except Exception:
                        # If we can't fetch, just add basic info
                        tests.append({
                            "id": test_id,
                            "name": f"Test {test_id}",
                            "type": "configured",
                            "candidate_count": None,
                            "description": f"HackerRank test {test_id}",
                            "note": "Unable to fetch candidate data"
                        })
                
                return {
                    "total_tests": len(tests),
                    "tests": tests,
                    "mock_data": False
                }
        except Exception as e:
            return {"error": str(e)}


    @mcp.tool()
    def get_candidate_scores(test_id: int, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Get candidate scores for a test. If email is provided, returns that candidate's score.
        Otherwise returns all candidate scores.
        
        Args:
            test_id: The HackerRank test ID
            email: Optional candidate email to filter by
        
        Returns:
            Dictionary with candidate score information
        """
        try:
            if USE_MOCK_DATA:
                all_candidates = get_mock_candidates(test_id)
            else:
                session = new_agent.make_session()
                all_candidates = new_agent.get_all_candidates(session, test_id)
            
            if email:
                candidates = [c for c in all_candidates if c.get("email") == email]
            else:
                candidates = all_candidates
            
            scores = [
                {
                    "email": c.get("email"),
                    "name": c.get("full_name") or c.get("name"),
                    "score": new_agent.extract_score(c),
                    "percentage_score": c.get("percentage_score"),
                    "status": c.get("status")
                }
                for c in candidates
            ]
            
            return {
                "test_id": test_id,
                "total_candidates": len(all_candidates),
                "filtered_count": len(candidates),
                "candidates": scores,
                "mock_data": USE_MOCK_DATA
            }
        except Exception as e:
            return {"error": str(e)}


    # ===========================================================
    # MCP RESOURCES - Expose data as readable resources
    # ===========================================================

    @mcp.resource("hackerrank://test/{test_id}/candidates")
    def get_test_candidates_resource(test_id: str) -> str:
        """
        Resource endpoint to get candidates for a test.
        Access via: hackerrank://test/{test_id}/candidates
        """
        try:
            if USE_MOCK_DATA:
                candidates = get_mock_candidates(int(test_id))
            else:
                session = new_agent.make_session()
                candidates = new_agent.get_all_candidates(session, int(test_id))
            
            result = {
                "test_id": int(test_id),
                "candidate_count": len(candidates),
                "candidates": [
                    {
                        "email": c.get("email"),
                        "name": c.get("full_name") or c.get("name"),
                        "score": new_agent.extract_score(c)
                    }
                    for c in candidates
                ],
                "mock_data": USE_MOCK_DATA
            }
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)


    @mcp.resource("hackerrank://config")
    def get_configuration_resource() -> str:
        """
        Resource endpoint to get current configuration.
        Access via: hackerrank://config
        """
        config = {
            "test_a_id": int(os.getenv("TEST_A_ID", "0")) or 356098,
            "test_b_id": int(os.getenv("TEST_B_ID", "0")) or 2263157,
            "test_a_pass_score": int(os.getenv("TEST_A_PASS_SCORE", "70")),
            "test_b_pass_score": int(os.getenv("TEST_B_PASS_SCORE", "80")),
            "api_configured": bool(os.getenv("ACCESS_TOKEN") or os.getenv("API_TOKEN")),
            "use_mock_data": USE_MOCK_DATA
        }
        return json.dumps(config, indent=2)


    # ===========================================================
    # MCP PROMPTS - Template prompts for common tasks
    # ===========================================================

    @mcp.prompt()
    def analyze_test_results(test_id: int, passing_score: float = 70.0) -> str:
        """
        Generate a prompt to analyze test results.
        
        Args:
            test_id: The test ID to analyze
            passing_score: The passing score threshold
        """
        return f"""Analyze the results for HackerRank test {test_id} with a passing score of {passing_score}.

Please:
1. Get the candidates who took this test
2. Identify how many passed vs failed
3. Calculate the pass rate
4. Identify any patterns in the scores
5. Provide recommendations for next steps"""


    @mcp.prompt()
    def generate_recruiter_summary(test_a_id: int, test_b_id: int) -> str:
        """
        Generate a prompt to create a recruiter summary.
        
        Args:
            test_a_id: Initial test ID
            test_b_id: Advanced test ID
        """
        return f"""Create a summary for recruiters about candidates who passed both tests.

Test A (Initial): {test_a_id}
Test B (Advanced): {test_b_id}

Please:
1. Get candidates who passed Test A
2. Get candidates who passed Test B
3. Identify candidates who passed both
4. Create a summary with candidate names, emails, and scores
5. Format it for easy use by recruiters"""


    # ===========================================================
    # SERVER STARTUP
    # ===========================================================

    if __name__ == "__main__":
        # Run the MCP server
        # Use stdio transport for MCP protocol (standard for MCP clients)
        mcp.run(transport="stdio")
        
        # Alternative: Use HTTP transport for web access
        # Uncomment the line below and comment the stdio line above
        # mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
else:
    if __name__ == "__main__":
        print("Error: MCP package is not installed.")
        print("Install it with: pip install 'mcp[cli]'")
        print("Then run: pip install -r requirements.txt")
