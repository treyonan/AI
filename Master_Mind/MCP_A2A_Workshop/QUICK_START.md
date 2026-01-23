# Quick Start Guide

**Workshop:** Advanced MCP and Agent to Agent Workshop  
**Status:** Day 1 ✅ Complete | Day 2 🚧 Coming Soon

---

## Prerequisites

- Python 3.10 or higher
- Claude Desktop installed
- Cursor IDE (recommended)
- Git
- Access credentials for:
  - HiveMQ broker (balancer.virtualfactory.online:1883)
  - MySQL database (proveit.virtualfactory.online:3306)

---

## 5-Minute Setup

### 1. Clone Repository
```bash
git clone https://github.com/iiot-university/MCP_A2A_Workshop.git
cd MCP_A2A_Workshop
```

### 2. Configure Credentials
```bash
cp .env.example .env
# Edit .env with your credentials:
# - MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD
# - MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD
```

### 3. Set Up MQTT Server (Session 2)
```bash
cd day1/mqtt_server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Set Up MySQL Server (Session 3)
```bash
cd ../mysql_server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Set Up MES Server (Session 4)
```bash
cd ../mes_server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configure Claude Desktop

### 1. Locate Config File

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

### 2. Add All Three Servers

```json
{
  "mcpServers": {
    "mqtt-uns": {
      "command": "/FULL/PATH/TO/day1/mqtt_server/venv/bin/python",
      "args": ["/FULL/PATH/TO/day1/mqtt_server/src/mqtt_mcp_server.py"]
    },
    "mysql-mes": {
      "command": "/FULL/PATH/TO/day1/mysql_server/venv/bin/python",
      "args": ["/FULL/PATH/TO/day1/mysql_server/src/mysql_mcp_server.py"]
    },
    "mes-press103": {
      "command": "/FULL/PATH/TO/day1/mes_server/venv/bin/python",
      "args": ["/FULL/PATH/TO/day1/mes_server/src/mes_mcp_server.py"]
    }
  }
}
```

**Important:** Replace `/FULL/PATH/TO/` with your actual path!

### 3. Restart Claude Desktop

- Quit Claude Desktop completely
- Relaunch
- Verify all 3 servers appear in the MCP server list (hammer icon)

---

## Test Your Setup

### Test MQTT Server
Open Claude Desktop and ask:
```
"What topics are available in the UNS?"
```

Expected: List of topics from the Flexible Packager

### Test MySQL Server
```
"What schemas are available in the database?"
```

Expected: List of 4 schemas (hivemq_ese_db, mes_custom, mes_lite, proveitdb)

### Test MES Server
```
"What is Press 103 doing right now?"
```

Expected: Equipment status with running state, speed, and shift

### Test Multi-Server Query
```
"Show me the current work order on Press 103 and its OEE breakdown"
```

Expected: Combined data from UNS and MySQL

---

## Troubleshooting

### Servers Don't Appear in Claude Desktop

**Problem:** Config file syntax error or wrong paths

**Solution:**
1. Validate JSON syntax (use jsonlint.com)
2. Verify full paths to venv Python interpreters
3. Check Claude Desktop logs for errors
4. Restart Claude Desktop after changes

### MQTT Connection Fails

**Problem:** Broker unreachable or wrong credentials

**Solution:**
1. Verify broker hostname: `balancer.virtualfactory.online`
2. Check credentials in `.env` file
3. Test connection with MQTT client (MQTT Explorer)
4. Check firewall/network access

### MySQL Connection Fails

**Problem:** Database unreachable or wrong credentials

**Solution:**
1. Verify host: `proveit.virtualfactory.online:3306`
2. Check credentials in `.env` file
3. Test connection with MySQL client
4. Verify schemas in MYSQL_SCHEMAS variable

### Tools Not Working

**Problem:** Server running but tools fail

**Solution:**
1. Check server logs (run manually to see stderr output)
2. Verify MQTT cache file exists and has data
3. Check MySQL connection pool initialized
4. Test individual tools with simple queries

---

## Session Guides

### Day 1 Sessions (All Complete ✅)

| Session | Guide | Duration |
|---------|-------|----------|
| Session 1 | Introduction (instructor-led) | 45 min |
| Session 2 | [MQTT Server](day1/mqtt_server/README.md) | 45 min |
| Session 3 | [MySQL Server](day1/mysql_server/README.md) | 45 min |
| Session 4 | [Use Cases](day1/use_cases/README.md) | 45 min |

### Recommended Learning Path

1. **Start Here:** [day1/mqtt_server/README.md](day1/mqtt_server/README.md)
2. **Then:** [day1/mysql_server/README.md](day1/mysql_server/README.md)
3. **Then:** [day1/mes_server/README.md](day1/mes_server/README.md)
4. **Finally:** [day1/use_cases/README.md](day1/use_cases/README.md)

---

## Key Files Reference

### Configuration
- `.env` - All credentials (root level, gitignored)
- `.env.example` - Template for credentials
- `claude_desktop_config.json` - MCP server configuration

### MQTT Server (Session 2)
- `day1/mqtt_server/src/mqtt_mcp_server.py` - Main server (826 lines)
- `day1/mqtt_server/src/mqtt_cache.json` - Runtime cache (auto-generated)
- `day1/mqtt_server/requirements.txt` - Dependencies

### MySQL Server (Session 3)
- `day1/mysql_server/src/mysql_mcp_server.py` - Main server (543 lines)
- `day1/mysql_server/schemas/*.md` - Database documentation
- `day1/mysql_server/requirements.txt` - Dependencies

### MES Server (Session 4)
- `day1/mes_server/src/mes_mcp_server.py` - Main server (872 lines)
- `day1/mes_server/src/mes_cache.json` - Runtime cache (auto-generated)
- `day1/mes_server/CURSOR_PROMPT.md` - Build instructions
- `day1/mes_server/requirements.txt` - Dependencies

---

## Common Commands

### Run Server Manually (for debugging)
```bash
cd day1/mqtt_server
source venv/bin/activate
python src/mqtt_mcp_server.py
# Watch stderr output for logs
```

### Test MQTT Connection
```bash
# Using mosquitto_sub (if installed)
mosquitto_sub -h balancer.virtualfactory.online -p 1883 \
  -u YOUR_USERNAME -P YOUR_PASSWORD -t '#' -v
```

### Test MySQL Connection
```bash
# Using mysql client (if installed)
mysql -h proveit.virtualfactory.online -P 3306 \
  -u YOUR_USERNAME -p -e "SHOW DATABASES;"
```

### Check Python Version
```bash
python --version  # Should be 3.10+
```

### List Installed Packages
```bash
source venv/bin/activate
pip list
```

---

## Example Queries for Claude

### MQTT Server Queries
```
"List all topics under Enterprise/Dallas/Press/Press 103/"
"What is the current value of Press 103 machine speed?"
"Search for all topics containing 'OEE'"
"Publish a test message to Enterprise/Dallas/Press/Press 103/Test"
```

### MySQL Server Queries
```
"Show me all tables in the mes_lite schema"
"Describe the structure of the mes_lite.run table"
"Get the last 10 production runs from mes_lite"
"Show me work orders that are currently open"
```

### MES Server Queries
```
"What is Press 103 doing right now?"
"Show me the active work order and progress"
"What's the OEE breakdown for Press 103?"
"What have been the main causes of downtime in the last 24 hours?"
"Analyze Press 103 and log an observation about what you find"
```

### Multi-Server Queries
```
"Compare the current Press 103 speed to its historical average"
"Show me the work order details and current OEE for Press 103"
"What's the relationship between downtime reasons and OEE performance?"
"Generate a status report for Press 103 including real-time and historical data"
```

---

## Getting Help

### Documentation
- **Root README:** [README.md](README.md) - Master overview
- **Day 1 Complete:** [day1/DAY1_COMPLETE.md](day1/DAY1_COMPLETE.md) - Completion summary
- **Session Guides:** Individual README files in each server directory

### Resources
- [MCP Documentation](https://modelcontextprotocol.io)
- [Claude API Docs](https://docs.anthropic.com)
- [Paho MQTT Python](https://eclipse.dev/paho/files/paho.mqtt.python/html/)

### Support
- **GitHub Issues:** https://github.com/iiot-university/MCP_A2A_Workshop/issues
- **Workshop Repository:** https://github.com/iiot-university/MCP_A2A_Workshop

---

## What's Next?

### After Day 1 ✅
- All 3 servers should be running
- You should be able to query industrial data via natural language
- You should understand multi-server architecture
- You should see the value of domain-specific servers

### Day 2 Preview 🚧
- Build specialized agents (Production, Quality, Maintenance)
- Implement agent-to-agent communication
- Create workflow orchestration
- Apply the A2A protocol
- Build collaborative intelligence systems

---

## Quick Reference Card

### Server Status Check
```bash
# Check if servers appear in Claude Desktop
# Look for hammer icon → should show 3 servers
```

### Common Issues
| Problem | Solution |
|---------|----------|
| Servers not in Claude Desktop | Check JSON syntax, restart Claude |
| MQTT connection fails | Verify credentials in .env |
| MySQL connection fails | Check host and credentials |
| Tools return errors | Run server manually to see logs |
| Cache file empty | Wait a moment for messages to arrive |

### Key Concepts
- **MCP Server:** Python program that exposes tools to Claude
- **Tool:** Function Claude can call (like get_topic_value)
- **Multi-Server:** Multiple MCP servers working together
- **Domain-Specific:** Tools mapped to business operations
- **UNS:** Unified Namespace (MQTT topic hierarchy)

---

**Status:** Day 1 Complete ✅ | Ready to Begin Day 2 🚧

For detailed guides, see individual session README files.

---

*Last Updated: December 17, 2025*
