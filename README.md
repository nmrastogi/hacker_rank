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
- `mcp_server.py` - MCP server exposing agent as tools for AI assistants
- `create_test.py` - Helper script for creating tests
- `try.py` - Example API usage

## MCP Server & Claude Integration

This project includes an **MCP (Model Context Protocol) server** that exposes the agent's functionality as tools that AI assistants can call, including **Claude Desktop**.

### Mock Data Mode

The MCP server includes **20 mock candidates** with test scores for testing and demos without real API access.

**Enable mock mode:**
```bash
# In .env file
USE_MOCK_DATA=true
```

**Mock Data:**
- Test A (356098): 12 candidates with scores 55-95%
- Test B (2263157): 8 candidates with scores 78-98%

See [MOCK_DATA_GUIDE.md](MOCK_DATA_GUIDE.md) for detailed usage instructions.

### Quick Setup for Claude Desktop

**Option 1: Automated Setup (Recommended)**
```bash
./setup_claude_desktop.sh
```
Then restart Claude Desktop.

**Option 2: Manual Setup**
See [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) for step-by-step instructions.

### Available Tools in Claude

Once integrated, you can ask Claude to:
- "Get all candidates who passed test 356098 with score above 70"
- "Run the screening pipeline for tests 356098 and 2263157"
- "Invite these candidates to test 2263157: [emails]"
- "What are the scores for test 356098?"

### Available Tools

The MCP server exposes these tools:
- `get_test_candidates` - Get candidates who passed a test
- `invite_candidates_to_test` - Invite candidates to a test
- `run_screening_pipeline` - Run complete screening workflow
- `get_candidate_scores` - Get candidate scores

### Documentation

- **[CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md)** - Complete Claude Desktop setup and integration guide
- **[TESTING.md](TESTING.md)** - Testing guide with pytest

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
