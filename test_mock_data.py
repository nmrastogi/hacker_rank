#!/usr/bin/env python3
"""
Quick test script to demonstrate mock data usage in MCP server
"""
import os

# Enable mock data mode
os.environ["USE_MOCK_DATA"] = "true"

# Import after setting environment variable
import mcp_server

def test_mock_data():
    print("🧪 Testing Mock Data Mode\n")
    
    # Test 1: Get candidates who passed Test A
    print("Test 1: Get candidates who passed Test A (score >= 70%)")
    result = mcp_server.get_test_candidates(356098, 70.0)
    print(f"  Total candidates: {result['total_candidates']}")
    print(f"  Passed (>=70%): {result['passed_count']}")
    print(f"  Using mock data: {result['mock_data']}")
    print(f"  Top 3 candidates:")
    for c in result['passed_candidates'][:3]:
        print(f"    - {c['name']}: {c['score']}%")
    print()
    
    # Test 2: Get all scores for Test A
    print("Test 2: Get all candidate scores for Test A")
    scores_result = mcp_server.get_candidate_scores(356098)
    print(f"  Total candidates: {scores_result['total_candidates']}")
    print(f"  Using mock data: {scores_result['mock_data']}")
    print()
    
    # Test 3: Run screening pipeline
    print("Test 3: Run screening pipeline (Test A -> Test B)")
    pipeline_result = mcp_server.run_screening_pipeline(356098, 2263157, 70.0, 80.0)
    print(f"  Test A - Passed: {pipeline_result['test_a']['passed_count']}")
    print(f"  Test B - Passed: {pipeline_result['test_b']['passed_count']}")
    print(f"  Recruiter Ready: {pipeline_result['recruiter_ready_count']}")
    print(f"  Using mock data: {pipeline_result['mock_data']}")
    print()
    
    print("✅ All tests completed successfully!")

if __name__ == "__main__":
    test_mock_data()

