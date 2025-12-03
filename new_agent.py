import requests
import time

# ===========================================================
# CONFIGURATION
# ===========================================================

BASE_URL = "https://www.hackerrank.com/x/api/v3"

import os
from dotenv import load_dotenv

load_dotenv()

# Load tokens from environment variables
ACCESS_TOKEN      = os.getenv("ACCESS_TOKEN", "")
JWT_ACCESS_TOKEN  = os.getenv("JWT_ACCESS_TOKEN", "")
JWT_REFRESH_TOKEN = os.getenv("JWT_REFRESH_TOKEN", "")
API_TOKEN         = os.getenv("API_TOKEN", "")

# Load test configuration from environment or use defaults
TEST_A_ID = int(os.getenv("TEST_A_ID", "0")) or 356098       # Replace with your real screening test ID
TEST_B_ID = int(os.getenv("TEST_B_ID", "0")) or 2263157      # Replace with your next-round test ID

TEST_A_PASS_SCORE = int(os.getenv("TEST_A_PASS_SCORE", "70"))
TEST_B_PASS_SCORE = int(os.getenv("TEST_B_PASS_SCORE", "80"))

LIMIT = 50  # candidates per API page


# ===========================================================
# AUTH SESSION
# ===========================================================

def make_session():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Auth-Token": API_TOKEN,
        "x-jwt-token": JWT_ACCESS_TOKEN,
        "x-refresh-token": JWT_REFRESH_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    return session


# ===========================================================
# API HELPERS
# ===========================================================

def get_candidates_page(session, test_id, offset=0):
    """Fetches ONE PAGE of full candidate objects."""
    url = f"{BASE_URL}/tests/{test_id}/candidates"
    params = {"offset": offset, "limit": LIMIT}

    res = session.get(url, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed: {res.text}")

    return res.json()


def get_all_candidates(session, test_id):
    """Fetch all pages of full candidate objects."""
    all_candidates = []
    offset = 0

    while True:
        data = get_candidates_page(session, test_id, offset)
        batch = data.get("data", [])

        all_candidates.extend(batch)

        if not data.get("next"):
            break

        offset += LIMIT

    return all_candidates


def extract_score(candidate):
    """Gets score and handles None."""
    if isinstance(candidate.get("percentage_score"), (int, float)):
        return candidate["percentage_score"]

    if isinstance(candidate.get("score"), (int, float)):
        return candidate["score"]

    return 0


def filter_passed(candidates, threshold):
    passed = []
    for c in candidates:
        score = extract_score(c)
        # status values can be: -1, 1, 2, etc. depending on test state
        if score >= threshold:
            passed.append(c)
    return passed


def invite_to_test(session, test_id, candidate):
    """Invite candidate to next test."""
    email = candidate.get("email")
    name = candidate.get("full_name") or candidate.get("name") or "Candidate"

    if not email:
        print(f"Skipping candidate with no email: {candidate}")
        return

    url = f"{BASE_URL}/tests/{test_id}/invites"

    payload = {
        "email": email,
        "name": name,
        "send_email": True
    }

    res = session.post(url, json=payload)
    if res.status_code not in (200, 201):
        print(f"Failed to invite {email}: {res.text}")
    else:
        print(f"Invited {email} to Test {test_id}")


def send_recruiter_invite(candidate):
    """Your Calendly / email automation goes here."""
    email = candidate.get("email")
    name = candidate.get("full_name")
    print(f"[Recruiter Invite] Would send calendar link to {name} <{email}>")


# ===========================================================
# MAIN
# ===========================================================

def run_pipeline():
    session = make_session()

    print("Fetching Test A candidates...")
    candidates_a = get_all_candidates(session, TEST_A_ID)
    print(f"Test A candidates: {len(candidates_a)}")

    print("Filtering passed Test A...")
    passed_a = filter_passed(candidates_a, TEST_A_PASS_SCORE)
    print(f"Passed Test A: {len(passed_a)}")

    print("Inviting passed A → Test B...")
    for c in passed_a:
        invite_to_test(session, TEST_B_ID, c)
        time.sleep(0.2)

    print("\nFetching Test B candidates...")
    candidates_b = get_all_candidates(session, TEST_B_ID)
    print(f"Test B candidates: {len(candidates_b)}")

    print("Filtering passed Test B...")
    passed_b = filter_passed(candidates_b, TEST_B_PASS_SCORE)
    print(f"Passed Test B: {len(passed_b)}")

    print("\nSending recruiter invites...")
    for c in passed_b:
        send_recruiter_invite(c)


if __name__ == "__main__":
    run_pipeline()