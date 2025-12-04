# HackerRank Candidate Screening Agent

An AI agent that automates the candidate screening workflow using the HackerRank API. It identifies candidates who pass initial tests, assigns them to advanced assessments, sends congratulatory emails, and creates Google Calendar invites for top performers.

## Features

- ✅ Automated test result processing
- ✅ Dynamic test creation and assignment
- ✅ Candidate filtering and scoring
- ✅ Email notifications to candidates who pass
- ✅ Google Calendar invites for top candidates
- ✅ MCP server for Claude Desktop integration
- ✅ Mock data mode for testing
- ✅ Comprehensive error handling
- ✅ Full test coverage with pytest

## Prerequisites

- Python 3.8 or higher
- HackerRank for Work account with API access
- HackerRank API key (generated from Settings > Integrations)
- (Optional) Google Calendar API credentials for calendar invites

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
# HackerRank API
ACCESS_TOKEN=your_access_token
API_TOKEN=your_api_token
JWT_ACCESS_TOKEN=your_jwt_access_token
JWT_REFRESH_TOKEN=your_jwt_refresh_token

# Test Configuration
TEST_A_ID=356098
TEST_B_ID=2263157
TEST_A_PASS_SCORE=70
TEST_B_PASS_SCORE=80

# Mock Data (for testing without real API)
USE_MOCK_DATA=false

# Google Calendar (optional - for real calendar invites)
GOOGLE_CALENDAR_TOKEN_PATH=token.pickle
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
GOOGLE_CALENDAR_TIMEZONE=America/New_York
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
5. **Send emails** - Sends congratulatory emails to all candidates who passed Test B
6. **Send calendar invites** - Creates Google Calendar invites for top 3 candidates
7. **Generate recruiter list** - Creates a list of candidates ready for recruiter calls

## MCP Server & Claude Desktop Integration

This project includes an **MCP (Model Context Protocol) server** that exposes the agent's functionality as tools that AI assistants can call, including **Claude Desktop**.

### Quick Setup for Claude Desktop

**Option 1: Automated Setup (Recommended)**
```bash
./setup_claude_desktop.sh
```
Then restart Claude Desktop.

**Option 2: Manual Setup**

1. **Install MCP package:**
   ```bash
   pip install "mcp[cli]"
   ```

2. **Configure Claude Desktop:**
   
   **macOS:**
   ```bash
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   **Windows:**
   ```bash
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

3. **Add MCP server configuration:**
   ```json
   {
     "mcpServers": {
       "hackerrank-agent": {
         "command": "python3",
         "args": [
           "/path/to/hacker_rank/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/path/to/hacker_rank"
         }
       }
     }
   }
   ```
   **Important:** Replace `/path/to/hacker_rank` with your actual project path!

4. **Restart Claude Desktop** completely for changes to take effect.

### Mock Data Mode

The MCP server includes **20 mock candidates** with test scores for testing and demos without real API access.

**Enable mock mode:**
```env
USE_MOCK_DATA=true
```

**Mock Data:**
- Test A (356098): 12 candidates with scores 55-95%
- Test B (2263157): 8 candidates with scores 78-98%

### Available Tools in Claude

Once integrated, you can ask Claude to:
- "Get all candidates who passed test 356098 with score above 70"
- "Run the screening pipeline for tests 356098 and 2263157" (automatically sends emails and Google Calendar invites to top 3)
- "Invite these candidates to test 2263157: [emails]"
- "What are the scores for test 356098?"
- "Send congratulatory emails to these candidates: [list]"
- "Send Google Calendar invites to the top 3 candidates from test 2263157"
- "List all available tests"

### Available MCP Tools

- `list_all_tests` - List all available tests with statistics
- `get_test_candidates` - Get candidates who passed a test
- `invite_candidates_to_test` - Invite candidates to a test
- `run_screening_pipeline` - Run complete screening workflow (includes email sending and Google Calendar invites)
- `get_candidate_scores` - Get candidate scores
- `send_email_to_candidates` - Send congratulatory emails to candidates
- `send_google_meet_invites_to_top_candidates` - Send Google Calendar invites with Meet links to top N candidates

### Troubleshooting Claude Integration

**MCP Server Not Appearing:**
1. Check the config file path and verify Python path is correct
2. Verify MCP is installed: `python3 -c "from mcp.server.fastmcp import FastMCP; print('OK')"`
3. Check Python version: `python3 --version` (should be 3.8+)

**Server Crashes:**
1. Check environment variables in `.env` file
2. Test the server directly: `python3 mcp_server.py`
3. Check Claude Desktop logs for error messages

**Tools Not Working:**
1. Verify API credentials are valid
2. Check test IDs exist in your HackerRank account
3. Ensure `.env` file has correct configuration

## Google Calendar Integration

The agent can send Google Calendar invites with Google Meet links to top candidates.

### Setup

1. **Install Google Calendar API libraries:**
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

2. **Set up Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Google Calendar API
   - Create OAuth 2.0 credentials (Desktop app type)
   - Download credentials as `credentials.json`

3. **Configure environment variables:**
   ```env
   GOOGLE_CALENDAR_TOKEN_PATH=token.pickle
   GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json
   GOOGLE_CALENDAR_TIMEZONE=America/New_York
   ```

4. **First-time authentication:**
   - Run the tool once - it will open a browser for OAuth
   - Grant permissions and save the token

### Features

- Creates actual Google Calendar events
- Sends calendar invites via email
- Automatically includes Google Meet links
- Customizable meeting titles and descriptions
- Email reminders (1 day before, 15 minutes before)

## Testing

This project uses pytest for comprehensive unit testing.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_new_agent.py

# Run with coverage report
pytest --cov=new_agent --cov-report=html
```

### Test Structure

- `tests/test_new_agent.py` - Unit tests for all agent functions
- `tests/test_mcp_server.py` - Unit tests for MCP server tools
- `tests/conftest.py` - Shared fixtures and test configuration

### Test Coverage

The tests cover:
- Score extraction from candidates
- Filtering passed candidates
- API pagination handling
- Candidate invitation logic
- Email sending functionality
- Google Calendar invite creation
- Error handling
- Edge cases (missing emails, no scores, etc.)

## Project Structure

```
hacker_rank/
├── new_agent.py              # Main agent implementation
├── mcp_server.py             # MCP server exposing agent as tools
├── setup_claude_desktop.sh   # Automated Claude Desktop setup script
├── requirements.txt          # Python dependencies
├── env.example               # Environment variables template
├── pytest.ini                # Pytest configuration
├── tests/                    # Test suite
│   ├── test_new_agent.py    # Agent function tests
│   ├── test_mcp_server.py   # MCP server tests
│   └── conftest.py          # Shared test fixtures
└── README.md                 # This file
```

## Configuration

### Test IDs and Scores

Edit in `new_agent.py` or set via environment variables:
```python
TEST_A_ID = 356098       # Your initial screening test ID
TEST_B_ID = 2263157     # Your advanced test ID
TEST_A_PASS_SCORE = 70  # Minimum score to pass Test A
TEST_B_PASS_SCORE = 80  # Minimum score to pass Test B
```

### API Authentication

The agent uses multiple authentication methods:
- Bearer token (ACCESS_TOKEN)
- API token (API_TOKEN)
- JWT tokens (JWT_ACCESS_TOKEN, JWT_REFRESH_TOKEN)

Set these in your `.env` file.

## Security

⚠️ **Never commit your `.env` file or hardcode API keys in the code.**

The `.gitignore` file is configured to exclude:
- `.env` files
- `credentials.json` and `token.pickle` (Google Calendar)
- `__pycache__/` directories
- Other sensitive files

## License

This project is provided as-is for educational and business use.

## Support

For HackerRank API documentation:
- [HackerRank API Docs](https://www.hackerrank.com/work/apidocs)

For issues or questions:
1. Check the troubleshooting sections above
2. Verify your `.env` file has correct credentials
3. Test the agent directly: `python3 new_agent.py`
4. Check Claude Desktop logs for error messages
