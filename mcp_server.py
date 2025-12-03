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
                ]
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
            session = new_agent.make_session()
            results = {
                "test_id": test_id,
                "total_invited": 0,
                "successful": [],
                "failed": []
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
                "recruiter_ready_candidates": recruiter_ready
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
                "candidates": scores
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
                ]
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
            "api_configured": bool(os.getenv("ACCESS_TOKEN") or os.getenv("API_TOKEN"))
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
