#!/usr/bin/env python3
"""
Test script for Google Meet invites tool
"""
import os

# Enable mock data mode
os.environ["USE_MOCK_DATA"] = "true"

# Import after setting environment variable
import mcp_server

def test_google_meet_invites():
    print("🧪 Testing Google Meet Invites Tool\n")
    
    # Test candidates with different scores
    candidates = [
        {"email": "alice@example.com", "name": "Alice Wonderland", "score": 95},
        {"email": "bob@example.com", "name": "Bob Builder", "score": 85},
        {"email": "charlie@example.com", "name": "Charlie Brown", "score": 90},
        {"email": "diana@example.com", "name": "Diana Prince", "score": 80},
        {"email": "emma@example.com", "name": "Emma Watson", "score": 88}
    ]
    
    result = mcp_server.send_google_meet_invites_to_top_candidates(candidates, top_n=3)
    
    print(f"✅ Total candidates: {result['total_candidates']}")
    print(f"✅ Top N selected: {result['top_n']}")
    print(f"✅ Invites sent: {result['invites_sent']}")
    print(f"✅ Using mock data: {result['mock_data']}")
    print("\n📅 Google Meet Invites:")
    print("-" * 70)
    
    for invite in result['successful']:
        print(f"\n👤 {invite['name']}")
        print(f"   Email: {invite['email']}")
        print(f"   Score: {invite['score']}%")
        print(f"   Meeting: {invite['meeting_title']}")
        print(f"   Date: {invite['meeting_date']}")
        print(f"   Duration: {invite['duration_minutes']} minutes")
        print(f"   🔗 Meet Link: {invite['meet_link']}")
    if 'calendar_link' in invite:
        print(f"   📅 Calendar Link: {invite['calendar_link']}")
    if 'event_id' in invite:
        print(f"   🆔 Event ID: {invite['event_id']}")
    if 'invite_sent' in invite:
        print(f"   ✅ Invite Sent: {invite['invite_sent']}")
    
    if result['failed']:
        print("\n❌ Failed Invites:")
        for failed in result['failed']:
            print(f"   - {failed.get('name', 'Unknown')}: {failed.get('error', 'Unknown error')}")
    
    print("\n" + "-" * 70)
    print("✅ Test completed successfully!")

if __name__ == "__main__":
    test_google_meet_invites()

