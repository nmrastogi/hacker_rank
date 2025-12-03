#!/usr/bin/env python3
"""
Test script for list_all_tests tool
"""
import os

# Enable mock data mode
os.environ["USE_MOCK_DATA"] = "true"

# Import after setting environment variable
import mcp_server

def test_list_all_tests():
    print("🧪 Testing List All Tests Tool\n")
    
    result = mcp_server.list_all_tests()
    
    print(f"✅ Total tests: {result['total_tests']}")
    print(f"✅ Using mock data: {result['mock_data']}")
    print("\n📋 Available Tests:")
    print("-" * 60)
    
    for test in result['tests']:
        print(f"\nTest ID: {test['id']}")
        print(f"  Name: {test['name']}")
        print(f"  Type: {test['type']}")
        print(f"  Candidates: {test['candidate_count']}")
        if 'average_score' in test and test['average_score']:
            print(f"  Average Score: {test['average_score']}%")
            print(f"  Score Range: {test['min_score']}% - {test['max_score']}%")
        print(f"  Description: {test['description']}")
    
    print("\n" + "-" * 60)
    print("✅ Test completed successfully!")

if __name__ == "__main__":
    test_list_all_tests()

