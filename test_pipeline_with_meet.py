#!/usr/bin/env python3
"""
Test the full pipeline with Google Meet invites
"""
import os

# Enable mock data mode
os.environ["USE_MOCK_DATA"] = "true"

# Import after setting environment variable
import mcp_server

def test_full_pipeline():
    print("🧪 Testing Full Pipeline with Google Meet Invites\n")
    
    result = mcp_server.run_screening_pipeline(356098, 2263157, 70.0, 80.0)
    
    print("✅ Pipeline Results:")
    print(f"   Recruiter ready candidates: {result['recruiter_ready_count']}")
    print(f"   Emails sent: {result['emails_sent']}")
    print(f"   Google Meet invites sent: {result.get('google_meet_invites_sent', 0)}")
    
    print("\n📅 Top 3 Candidates with Google Calendar Invites:")
    print("-" * 70)
    
    meet_invites = result.get('google_meet_invites', {}).get('successful', [])
    for i, invite in enumerate(meet_invites[:3], 1):
        print(f"\n{i}. {invite['name']}")
        print(f"   Email: {invite['email']}")
        print(f"   Score: {invite['score']}%")
        print(f"   Meeting: {invite['meeting_title']}")
        print(f"   Date: {invite['meeting_date']}")
        if 'meeting_end' in invite:
            print(f"   End: {invite['meeting_end']}")
        print(f"   🔗 Meet Link: {invite['meet_link']}")
        if 'calendar_link' in invite:
            print(f"   📅 Calendar Link: {invite['calendar_link']}")
        if 'event_id' in invite:
            print(f"   🆔 Event ID: {invite['event_id']}")
        if 'invite_sent' in invite:
            print(f"   ✅ Invite Sent: {invite['invite_sent']}")
    
    print("\n" + "-" * 70)
    print("✅ Full pipeline test completed successfully!")

if __name__ == "__main__":
    test_full_pipeline()

