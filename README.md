# HackerRank Candidate Screening Agent

An AI agent that automates the candidate screening workflow using the HackerRank API. It identifies candidates who pass initial tests, assigns them to advanced assessments, and generates a list of candidates ready for recruiter calls.

## Features

- ✅ Automated test result processing
- ✅ Dynamic test creation and assignment
- ✅ Candidate filtering and scoring
- ✅ JSON export of recruiter-ready candidates
- ✅ Comprehensive error handling

## Prerequisites

- Python 3.8 or higher
- HackerRank for Work account with API access
- HackerRank API key (generated from Settings > Integrations)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd hacker_rank
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
```

Edit `.env` with your credentials:
```env
HACKERRANK_API_KEY=your_api_key_here
HACKERRANK_PARTNER=ashby  # Your integration type (ashby, greenhouse, etc.)
TEST_A_ID=your_initial_test_id
TEST_B_ID=your_advanced_test_id
TEST_A_PASS_SCORE=70
TEST_B_PASS_SCORE=80
```

## Usage

### Basic Usage

Run the main agent:
```bash
python new_agent.py
```

### Programmatic Usage

```python
from new_agent import run_pipeline

# Run the complete workflow
run_pipeline()
```

## Workflow

1. **Fetch Test A candidates** - Gets all candidates who took the initial screening test
2. **Filter passed candidates** - Identifies candidates who scored above the threshold
3. **Invite to Test B** - Automatically invites passed candidates to the advanced test
4. **Filter Test B results** - Identifies candidates who passed the advanced test
5. **Generate recruiter list** - Creates a list of candidates ready for recruiter calls

## Configuration

Edit the configuration section in `new_agent.py`:

```python
TEST_A_ID = 356098       # Your initial screening test ID
TEST_B_ID = 2263157     # Your advanced test ID
TEST_A_PASS_SCORE = 70  # Minimum score to pass Test A
TEST_B_PASS_SCORE = 80  # Minimum score to pass Test B
LIMIT = 50              # Candidates per API page
```

## API Authentication

The agent uses multiple authentication methods:
- Bearer token (ACCESS_TOKEN)
- API token (API_TOKEN)
- JWT tokens (JWT_ACCESS_TOKEN, JWT_REFRESH_TOKEN)

Set these in your `.env` file or update the configuration in the code.

## Files

- `new_agent.py` - Main agent implementation
- `create_test.py` - Helper script for creating tests
- `try.py` - Example API usage

## Security

⚠️ **Never commit your `.env` file or hardcode API keys in the code.**

The `.gitignore` file is configured to exclude:
- `.env` files
- `__pycache__/` directories
- Other sensitive files

## Testing

This project uses pytest for testing. All tests are located in the `tests/` directory.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_new_agent.py

# Run specific test
pytest tests/test_new_agent.py::TestExtractScore::test_extract_percentage_score

# Run with coverage report
pytest --cov=new_agent --cov-report=html
```

### Test Structure

- `tests/test_new_agent.py` - Unit tests for all agent functions
- `tests/conftest.py` - Shared fixtures and test configuration

### Test Coverage

The tests cover:
- Score extraction from candidates
- Filtering passed candidates
- API pagination handling
- Candidate invitation logic
- Error handling
- Edge cases (missing emails, no scores, etc.)

## License

This project is provided as-is for educational and business use.

## Support

For HackerRank API documentation:
- [HackerRank API Docs](https://www.hackerrank.com/work/apidocs)
