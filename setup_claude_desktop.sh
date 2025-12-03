#!/bin/bash

# Setup script for Claude Desktop MCP integration
# This script helps configure Claude Desktop to use the HackerRank MCP server

set -e

echo "🚀 Setting up Claude Desktop MCP integration..."

# Get the absolute path of the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_SERVER_PATH="$SCRIPT_DIR/mcp_server.py"

# Claude Desktop config location (macOS)
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Check if Claude Desktop config directory exists
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo "⚠️  Claude Desktop config directory not found."
    echo "   Creating: $CLAUDE_CONFIG_DIR"
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

# Check if config file exists
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "📄 Existing Claude Desktop config found."
    echo "   Backing up to: ${CLAUDE_CONFIG_FILE}.backup"
    cp "$CLAUDE_CONFIG_FILE" "${CLAUDE_CONFIG_FILE}.backup"
    
    # Check if hackerrank-agent already exists
    if grep -q "hackerrank-agent" "$CLAUDE_CONFIG_FILE"; then
        echo "⚠️  hackerrank-agent already exists in config."
        echo "   You may need to manually update it."
        read -p "   Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Setup cancelled."
            exit 1
        fi
    fi
fi

# Detect Python executable (prefer anaconda if available)
if [ -f "/Users/namanrastogi/anaconda3/bin/python" ]; then
    PYTHON_CMD="/Users/namanrastogi/anaconda3/bin/python"
    echo "✅ Using Anaconda Python: $PYTHON_CMD"
else
    PYTHON_CMD="python3"
    echo "✅ Using system Python: $PYTHON_CMD"
fi

# Create the MCP server configuration
MCP_CONFIG=$(cat <<EOF
{
  "mcpServers": {
    "hackerrank-agent": {
      "command": "$PYTHON_CMD",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "PYTHONPATH": "$SCRIPT_DIR"
      }
    }
  }
}
EOF
)

# If config file exists, merge with existing config
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "📝 Merging with existing config..."
    # Use Python to merge JSON (more reliable than shell)
    python3 <<PYTHON_SCRIPT
import json
import sys
import os

config_file = "$CLAUDE_CONFIG_FILE"
python_cmd = "$PYTHON_CMD"
new_config = {
    "mcpServers": {
        "hackerrank-agent": {
            "command": python_cmd,
            "args": ["$MCP_SERVER_PATH"],
            "env": {
                "PYTHONPATH": "$SCRIPT_DIR"
            }
        }
    }
}

# Read existing config
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        try:
            existing = json.load(f)
            if "mcpServers" in existing:
                existing["mcpServers"]["hackerrank-agent"] = new_config["mcpServers"]["hackerrank-agent"]
            else:
                existing["mcpServers"] = new_config["mcpServers"]
            config = existing
        except json.JSONDecodeError:
            config = new_config
else:
    config = new_config

# Write merged config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Config updated successfully")
PYTHON_SCRIPT
else
    echo "📝 Creating new config file..."
    echo "$MCP_CONFIG" > "$CLAUDE_CONFIG_FILE"
fi

# Verify Python and MCP installation
echo ""
echo "🔍 Verifying setup..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check MCP installation
if ! python3 -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null; then
    echo "⚠️  MCP package not installed."
    echo ""
    echo "   Please install MCP using one of these methods:"
    echo "   1. Using anaconda: /Users/namanrastogi/anaconda3/bin/pip install 'mcp[cli]'"
    echo "   2. Upgrade pip first: python3 -m pip install --upgrade pip"
    echo "   3. Then install: pip3 install 'mcp[cli]'"
    echo ""
    echo "   See INSTALL_MCP.md for detailed instructions."
    echo ""
    read -p "   Attempt to install now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Try anaconda pip first
        if [ -f "/Users/namanrastogi/anaconda3/bin/pip" ]; then
            echo "   Trying anaconda pip..."
            /Users/namanrastogi/anaconda3/bin/pip install "mcp[cli]" || {
                echo "   Trying system pip..."
                pip3 install "mcp[cli]" || {
                    echo "❌ Failed to install MCP automatically."
                    echo "   Please install manually. See INSTALL_MCP.md"
                    exit 1
                }
            }
        else
            pip3 install "mcp[cli]" || {
                echo "❌ Failed to install MCP. Please install manually."
                echo "   See INSTALL_MCP.md for instructions"
                exit 1
            }
        fi
    else
        echo "⚠️  Skipping MCP installation. Please install manually."
        echo "   See INSTALL_MCP.md for instructions"
        exit 1
    fi
fi
echo "✅ MCP package installed"

# Check if mcp_server.py exists
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ mcp_server.py not found at: $MCP_SERVER_PATH"
    exit 1
fi
echo "✅ MCP server found: $MCP_SERVER_PATH"

# Test server import
if python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); import mcp_server" 2>/dev/null; then
    echo "✅ MCP server module loads successfully"
else
    echo "⚠️  MCP server module has import warnings (this may be OK if MCP isn't installed yet)"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Restart Claude Desktop"
echo "   2. Open Claude Desktop and check if 'hackerrank-agent' appears in the MCP servers list"
echo "   3. Try asking Claude: 'Get candidates who passed test 356098'"
echo ""
echo "📄 Config file location: $CLAUDE_CONFIG_FILE"
echo ""

