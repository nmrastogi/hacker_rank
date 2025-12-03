# Using Mock Data with Claude Desktop

This guide shows you exactly how to use the mock candidates data with Claude Desktop.

## ✅ Step 1: Enable Mock Data (Already Done!)

You already have `USE_MOCK_DATA=true` in your `.env` file. Perfect!

## ✅ Step 2: Verify MCP Server Setup

Make sure Claude Desktop is configured to use the MCP server:

1. **Check your Claude Desktop config:**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **If not set up, run the setup script:**
   ```bash
   ./setup_claude_desktop.sh
   ```

## ✅ Step 3: Restart Claude Desktop

**Important:** Close Claude Desktop completely and reopen it for the `.env` changes to take effect.

## ✅ Step 4: Test with Claude

Open Claude Desktop and try these queries:

### Example 1: Get Candidates Who Passed

**Ask Claude:**
```
Get all candidates who passed test 356098 with a score above 70
```

**Expected Response:**
Claude will call the `get_test_candidates` tool and return:
- 9 candidates who passed (out of 12 total)
- Names and scores from mock data
- Response will include `"mock_data": true`

### Example 2: Run Screening Pipeline

**Ask Claude:**
```
Run the screening pipeline for test A (ID: 356098) and test B (ID: 2263157) with passing scores of 70 and 80
```

**Expected Response:**
- Test A: 9 candidates passed
- Test B: 7 candidates passed  
- Recruiter-ready candidates list
- All using mock data

### Example 3: Get All Scores

**Ask Claude:**
```
What are the scores for all candidates in test 356098?
```

**Expected Response:**
- All 12 candidates with their scores
- Names and email addresses
- Using mock data

### Example 4: Get Specific Candidate

**Ask Claude:**
```
Get the score for alice.wonderland@example.com in test 356098
```

**Expected Response:**
- Alice Wonderland's score: 85%
- Using mock data

### Example 5: List All Available Tests

**Ask Claude:**
```
List all available tests
```

**Expected Response:**
- Shows all tests (Test A and Test B)
- Test IDs, names, candidate counts
- Average scores and score ranges
- Using mock data

## What You'll See

When Claude uses the tools, you'll see:

1. **Tool calls** - Claude will show which tools it's calling
2. **Mock data indicator** - Responses include `"mock_data": true`
3. **Realistic results** - 12 candidates for Test A, 8 for Test B

## Mock Candidates Available

### Test A (356098) - 12 Candidates

| Name | Score | Status |
|------|-------|--------|
| Alice Wonderland | 85% | ✅ Pass (>=70%) |
| Bob Builder | 65% | ❌ Fail |
| Charlie Brown | 75% | ✅ Pass |
| Diana Prince | 90% | ✅ Pass |
| Emma Watson | 88% | ✅ Pass |
| Frank Sinatra | 72% | ✅ Pass |
| Grace Hopper | 95% | ✅ Pass |
| Henry Ford | 68% | ❌ Fail |
| Isabella Swan | 79% | ✅ Pass |
| Jack Sparrow | 55% | ❌ Fail |
| Katherine Johnson | 92% | ✅ Pass |
| Leonardo da Vinci | 87% | ✅ Pass |

**9 candidates pass with 70% threshold**

### Test B (2263157) - 8 Candidates

| Name | Score | Status |
|------|-------|--------|
| Alice Wonderland | 92% | ✅ Pass (>=80%) |
| Charlie Brown | 78% | ❌ Fail |
| Diana Prince | 95% | ✅ Pass |
| Emma Watson | 89% | ✅ Pass |
| Grace Hopper | 98% | ✅ Pass |
| Isabella Swan | 82% | ✅ Pass |
| Katherine Johnson | 96% | ✅ Pass |
| Leonardo da Vinci | 91% | ✅ Pass |

**7 candidates pass with 80% threshold**

## Troubleshooting

### Claude Doesn't See Mock Data

1. **Verify `.env` file:**
   ```bash
   cat .env | grep USE_MOCK_DATA
   ```
   Should show: `USE_MOCK_DATA=true`

2. **Check if Claude Desktop restarted:**
   - Fully quit Claude Desktop (Cmd+Q on Mac)
   - Reopen it

3. **Verify MCP server is connected:**
   - Look for MCP server status in Claude Desktop
   - Should show "hackerrank-agent" as connected

### Mock Data Not Working

1. **Test the server directly:**
   ```bash
   python test_mock_data.py
   ```
   This should show mock data working.

2. **Check environment variable:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('USE_MOCK_DATA:', os.getenv('USE_MOCK_DATA'))"
   ```
   Should print: `USE_MOCK_DATA: true`

### Want to Switch Back to Real API?

Simply change in `.env`:
```bash
USE_MOCK_DATA=false
```

Then restart Claude Desktop.

## Quick Test Commands

Try these exact queries in Claude:

```
Get all candidates who passed test 356098 with score above 70
```

```
Run the complete screening pipeline for tests 356098 and 2263157
```

```
Show me all candidate scores for test 356098
```

```
Who are the recruiter-ready candidates from the screening pipeline?
```

## Next Steps

1. ✅ Mock data is enabled (`USE_MOCK_DATA=true`)
2. ✅ Restart Claude Desktop
3. ✅ Ask Claude to use the tools
4. ✅ See mock candidates in action!

The mock data is ready to use. Just restart Claude Desktop and start asking!

