# Claude Desktop Integration Guide

This guide will help you integrate the HackerRank MCP server with Claude Desktop so you can use the agent's tools directly through Claude.

## Quick Setup (Automated)

Run the setup script:

```bash
./setup_claude_desktop.sh
```

This script will:
- Create/update Claude Desktop configuration
- Verify Python and MCP installation
- Set up the MCP server path
- Test the configuration

**Then restart Claude Desktop** for changes to take effect.

## Manual Setup

If you prefer to set it up manually:

### Step 1: Install Dependencies

```bash
# Install MCP package
pip3 install "mcp[cli]"

# Or install all dependencies
pip3 install -r requirements.txt
```

### Step 2: Find Your Project Path

Get the absolute path to your project:

```bash
cd /Users/namanrastogi/Documents/hacker_rank
pwd
# This will show: /Users/namanrastogi/Documents/hacker_rank
```

### Step 3: Configure Claude Desktop

1. **Open Claude Desktop config file:**

   **macOS:**
   ```bash
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   **Windows:**
   ```bash
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Add or update the MCP server configuration:**

   If the file doesn't exist or is empty, use this:
   ```json
   {
     "mcpServers": {
       "hackerrank-agent": {
         "command": "python3",
         "args": [
           "/Users/namanrastogi/Documents/hacker_rank/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/Users/namanrastogi/Documents/hacker_rank"
         }
       }
     }
   }
   ```

   **Important:** Replace `/Users/namanrastogi/Documents/hacker_rank` with your actual project path!

   If the file already has other MCP servers, add `"hackerrank-agent"` to the existing `mcpServers` object:

   ```json
   {
     "mcpServers": {
       "existing-server": { ... },
       "hackerrank-agent": {
         "command": "python3",
         "args": [
           "/Users/namanrastogi/Documents/hacker_rank/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/Users/namanrastogi/Documents/hacker_rank"
         }
       }
     }
   }
   ```

3. **Save the file**

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop completely for the changes to take effect.

### Step 5: Verify Connection

1. Open Claude Desktop
2. Look for MCP server status (usually in settings or status bar)
3. You should see "hackerrank-agent" listed as connected

## Using the Tools in Claude

Once connected, you can ask Claude to use the tools:

### Example Queries

**Get candidates who passed a test:**
```
Get all candidates who passed test 356098 with a score above 70
```

**Run the screening pipeline:**
```
Run the screening pipeline for test A (ID: 356098) and test B (ID: 2263157)
```

**Get candidate scores:**
```
What are the scores for all candidates in test 356098?
```

**Invite candidates:**
```
Invite these candidates to test 2263157: alice@example.com, bob@example.com
```

**Analyze test results:**
```
Analyze the results for test 356098 with a passing score of 70
```

Claude will automatically call the appropriate MCP tools to fulfill your requests.

## Available Tools

The MCP server exposes these tools to Claude:

1. **`get_test_candidates`**
   - Get candidates who passed a specific test
   - Parameters: `test_id`, `passing_score` (optional)

2. **`invite_candidates_to_test`**
   - Invite candidates to a test by email
   - Parameters: `test_id`, `candidate_emails`

3. **`run_screening_pipeline`**
   - Run the complete screening workflow
   - Parameters: `test_a_id`, `test_b_id`, `test_a_pass_score` (optional), `test_b_pass_score` (optional)

4. **`get_candidate_scores`**
   - Get candidate scores for a test
   - Parameters: `test_id`, `email` (optional)

## Troubleshooting

### MCP Server Not Appearing

1. **Check the config file path:**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Verify the Python path is correct:**
   - Make sure the path in `args` is absolute (starts with `/`)
   - Check that `mcp_server.py` exists at that path

3. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8+
   ```

4. **Verify MCP is installed:**
   ```bash
   python3 -c "from mcp.server.fastmcp import FastMCP; print('OK')"
   ```

### "Command not found" Error

- Make sure `python3` is in your PATH
- Try using full path: `/usr/bin/python3` or `/usr/local/bin/python3`
- Check with: `which python3`

### Server Crashes or Errors

1. **Check environment variables:**
   - Make sure `.env` file exists with your HackerRank credentials
   - Verify `ACCESS_TOKEN`, `API_TOKEN`, etc. are set

2. **Test the server directly:**
   ```bash
   python3 mcp_server.py
   ```
   (It should start and wait for stdio input)

3. **Check logs:**
   - Claude Desktop may show error messages in its console
   - Look for Python error traces

### Tools Not Working

1. **Verify API credentials:**
   - Test with the original `new_agent.py` first
   - Make sure your HackerRank API keys are valid

2. **Check test IDs:**
   - Verify the test IDs exist in your HackerRank account
   - Use valid test IDs in your queries

### Permission Issues

If you get permission errors:

```bash
# Make sure the script is executable
chmod +x setup_claude_desktop.sh

# Check file permissions
ls -la mcp_server.py
```

## Advanced Configuration

### Using Virtual Environment

If you're using a virtual environment:

```json
{
  "mcpServers": {
    "hackerrank-agent": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/Users/namanrastogi/Documents/hacker_rank/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/namanrastogi/Documents/hacker_rank"
      }
    }
  }
}
```

### Custom Environment Variables

You can add environment variables to the config:

```json
{
  "mcpServers": {
    "hackerrank-agent": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project",
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

## Testing the Integration

After setup, test with a simple query in Claude:

```
What tools are available from the hackerrank-agent?
```

Or:

```
Get the configuration from hackerrank-agent
```

Claude should be able to list the available tools and resources.

## Next Steps

1. ✅ Set up the integration (using script or manual)
2. ✅ Restart Claude Desktop
3. ✅ Test with a simple query
4. ✅ Start using the tools for your screening workflow!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your `.env` file has correct credentials
3. Test the agent directly: `python3 new_agent.py`
4. Check Claude Desktop logs for error messages

