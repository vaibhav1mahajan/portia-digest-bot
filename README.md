# 🤖 Portia Digest Bot

> **Automated Daily Digest Bot for Portia Plan Runs**  
> *Get intelligent insights into your automation workflows via email*

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://hub.docker.com/r/vaibhavmahajan2257/portia-digest-bot)
[![Python](https://img.shields.io/badge/Python-3.12+-green?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Problem Statement

**The Challenge**: As a developer using [Portia](https://portialabs.ai/) for automation, you need to:
- 📊 **Track performance** of your plan runs and workflows
- 🔍 **Monitor tool usage** and identify optimization opportunities  
- 📈 **Understand trends** in success rates and execution times
- ⏰ **Stay informed** without manually checking the dashboard daily
- 📧 **Get actionable insights** delivered to your inbox

**Current Pain Points**:
- Manual dashboard checking is time-consuming
- No automated way to track tool performance
- Missing insights into workflow optimization opportunities
- No daily summaries of automation health

## 💡 Our Solution

**Portia Digest Bot** is a CLI tool that automatically:
1. **📊 Analyzes** your daily Portia plan runs
2. **🤖 Generates AI summaries** with key insights
3. **📧 Sends beautiful digest emails** via Gmail integration
4. **🛠️ Tracks tool usage** and performance metrics
5. **⚡ Provides actionable insights** for workflow optimization

### ✨ Key Features

- **🔍 Comprehensive Analysis**: Success rates, duration stats, tool usage, failure analysis
- **🤖 AI-Powered Summaries**: Intelligent insights using OpenAI GPT
- **📧 Email Integration**: Beautiful HTML emails via Portia's Gmail tool
- **🛠️ Tool Performance**: Track which tools are used most and their success rates
- **⚡ Easy Automation**: Docker support, cron jobs, GitHub Actions
- **📊 Rich Metrics**: P95 durations, fastest/slowest plans, daily distributions

## 🚀 Quick Start (5 minutes)

### Option 1: Docker (Recommended - No Setup Required)

```bash
# 1. Create environment file
cat > .env << EOF
PORTIA_API_KEY=prt-your-api-key-here
PORTIA_ORG_ID=Personal
OPENAI_API_KEY=sk-your-openai-api-key-here
GMAIL_TO=your-email@example.com
EOF

# 2. Run complete digest workflow
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli digest --yesterday

# 3. Preview email without sending
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli digest --yesterday --preview-only
```

### Option 2: Local Setup

```bash
# 1. Clone and setup
git clone https://github.com/vaibhav1mahajan/portia-digest-bot.git
cd portia-digest-bot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -e .

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run digest
portia-fetch digest --yesterday
```

## 🔑 API Keys Required

### Get Your API Keys

1. **Portia API Key**: [Portia Labs Dashboard](https://app.portialabs.ai/)
   - Sign up/login to Portia
   - Go to Settings → API Keys
   - Create new key (starts with `prt-`)

2. **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/api-keys)
   - Sign up/login to OpenAI
   - Go to API Keys section
   - Create new key (starts with `sk-`)

### Environment Configuration

Create `.env` file:
```bash
# Required
PORTIA_API_KEY=prt-your-portia-api-key-here
PORTIA_ORG_ID=Personal
OPENAI_API_KEY=sk-your-openai-api-key-here
GMAIL_TO=your-email@example.com

# Optional (defaults shown)
PORTIA_API_BASE=https://api.portialabs.ai/api/v0
```

## 📖 Complete Usage Guide

### 🎯 Main Commands

#### 1. Complete Digest Workflow
```bash
# Analyze + Summarize + Send Email
portia-fetch digest --yesterday

# Preview email without sending
portia-fetch digest --yesterday --preview-only

# Custom time window
portia-fetch digest --since 2025-08-20T00:00:00Z --until 2025-08-24T23:59:59Z

# Include tool usage analysis
portia-fetch digest --yesterday --with-tools
```

#### 2. Individual Commands
```bash
# Analyze plan runs
portia-fetch analyze --yesterday --with-tools --json

# Generate AI summary
portia-fetch summarize --yesterday

# Preview email content
portia-fetch preview-mail --yesterday
```

#### 3. Plan Management
```bash
# List all plans
portia-fetch plans list

# Get specific plan details
portia-fetch plans get plan-12345
```

#### 4. Plan Run Management
```bash
# List plan runs
portia-fetch plan-runs list --since 2025-08-20T00:00:00Z

# Get specific run details
portia-fetch plan-runs get prun-12345
```

### 🐳 Docker Commands

```bash
# Complete workflow
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli digest --yesterday

# Individual commands
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli analyze --yesterday --with-tools --json

# Custom time window
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli digest \
  --since 2025-08-20T00:00:00Z \
  --until 2025-08-24T23:59:59Z \
  --with-tools
```

### 📅 Time Window Options

```bash
# Predefined windows
--today          # Today (00:00 to now)
--yesterday      # Yesterday (00:00 to 23:59)

# Custom ISO format
--since 2025-08-20T00:00:00Z
--until 2025-08-24T23:59:59Z

# Examples
--since 2025-08-20T09:00:00Z --until 2025-08-20T17:00:00Z  # Work hours
--since 2025-08-01T00:00:00Z --until 2025-08-31T23:59:59Z  # Full month
```

## 🔄 Automation Setup

### Option 1: Cron Job (Local/Server)

```bash
# Edit crontab
crontab -e

# Add daily digest at 9 AM
0 9 * * * cd /path/to/portia-digest-bot && ./bin/digest-send-daily

# Or using Docker
0 9 * * * docker run --rm --env-file /path/to/.env vaibhavmahajan2257/portia-digest-bot:latest python -m portia_fetch.cli digest --yesterday
```

### Option 2: GitHub Actions (Free)

1. **Fork this repository**
2. **Add secrets** in Settings → Secrets and variables → Actions:
   - `PORTIA_API_KEY`
   - `PORTIA_ORG_ID` 
   - `OPENAI_API_KEY`
   - `GMAIL_TO`

3. **Enable GitHub Actions** - workflow will run daily at 9 AM UTC

### Option 3: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  portia-digest:
    image: vaibhavmahajan2257/portia-digest-bot:latest
    env_file: .env
    command: python -m portia_fetch.cli digest --yesterday
    restart: unless-stopped
```

## 📧 Email Setup & Authentication

### First Time Setup

1. **Run the digest command**:
   ```bash
   portia-fetch digest --yesterday
   ```

2. **Follow OAuth flow**:
   - Click the provided Gmail authorization link
   - Sign in with your Google account
   - Grant permissions to the application
   - Copy the authorization code back to terminal

3. **Email will be sent** to the address specified in `GMAIL_TO`

### Email Content Preview

The digest email includes:
- 📊 **Executive Summary** with key metrics
- 📋 **Plan Performance Analysis** 
- 🏃‍♂️ **Run Performance Analysis**
- 🛠️ **Tool Usage Analysis** (when `--with-tools` is used)
- ⚡ **Tool Performance** metrics
- 🔍 **Failure Analysis** for debugging
- 📈 **Temporal Analysis** patterns
- 🤖 **AI Insights** for optimization

## 🛠️ Tool Usage Analysis

When using `--with-tools`, the bot analyzes:

- **Total tool invocations** across all runs
- **Unique tools used** and their frequency
- **Top 5 most used tools** with success rates
- **Tool performance metrics** (avg duration, success rate)
- **Tool distribution** across different plan types

**Example Output**:
```
🛠️ Tool Usage Analysis
📊 Tool Statistics:
- Total Tool Invocations: 15
- Unique Tools Used: 8

🔝 Top 5 Most Used Tools:
1. LLM Tool - 5 uses, ✅ 100.0% success
2. Portia Google Send Email Tool - 3 uses, ✅ 100.0% success
3. Search Tool - 2 uses, ✅ 100.0% success
4. File writer tool - 2 uses, ✅ 100.0% success
5. Zendesk Create Ticket Tool - 1 uses, ✅ 100.0% success
```

## 🐳 Docker Hub

**Image**: `vaibhavmahajan2257/portia-digest-bot:latest`

```bash
# Pull image
docker pull vaibhavmahajan2257/portia-digest-bot:latest

# View on Docker Hub
https://hub.docker.com/r/vaibhavmahajan2257/portia-digest-bot
```

## 📁 Project Structure

```
portia-digest-bot/
├── portia_fetch/              # Core application
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── client.py              # Portia API client
│   ├── analyzer.py            # Plan run analysis
│   ├── summarizer.py          # AI summary generation
│   ├── email_sender.py        # Email sending via Portia
│   ├── email_formatter.py     # Email content formatting
│   └── mail_preview.py        # Email preview
├── bin/
│   └── digest-send-daily      # Daily automation script
├── Dockerfile                 # Docker container
├── docker-compose.yml         # Docker orchestration
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## 🔧 Troubleshooting

### Common Issues

**API Key Issues**:
```bash
# Ensure Portia API key starts with 'prt-'
PORTIA_API_KEY=prt-your-key-here

# Ensure OpenAI API key starts with 'sk-'
OPENAI_API_KEY=sk-your-key-here
```

**Gmail Authentication**:
- Follow the OAuth flow when prompted
- Use the same Google account as `GMAIL_TO`
- Grant all requested permissions

**Docker Issues**:
```bash
# Use environment file
docker run --rm --env-file .env vaibhavmahajan2257/portia-digest-bot:latest ...

# Or pass environment variables directly
docker run --rm \
  -e PORTIA_API_KEY=prt-your-key \
  -e PORTIA_ORG_ID=Personal \
  -e OPENAI_API_KEY=sk-your-key \
  -e GMAIL_TO=your-email@example.com \
  vaibhavmahajan2257/portia-digest-bot:latest ...
```

**No Plan Runs Found**:
- Check your time window (`--since`/`--until`)
- Ensure you have plan runs in the specified period
- Try a broader time range for testing

### Debug Commands

```bash
# Test API connection
portia-fetch plans list

# Test with verbose output
portia-fetch analyze --yesterday --json

# Preview without sending
portia-fetch digest --yesterday --preview-only
```

## 🧪 Testing Examples

### Quick Test (1 minute)
```bash
# Test with Docker
docker run --rm --env-file .env \
  vaibhavmahajan2257/portia-digest-bot:latest \
  python -m portia_fetch.cli digest --yesterday --preview-only
```

### Full Test (5 minutes)
```bash
# 1. Test analysis
portia-fetch analyze --yesterday --with-tools --json

# 2. Test summary generation
portia-fetch summarize --yesterday

# 3. Test complete workflow
portia-fetch digest --yesterday --preview-only

# 4. Test email sending (requires Gmail auth)
portia-fetch digest --yesterday
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Portia SDK](https://github.com/portialabs/portia-sdk-python)
- AI summaries powered by [OpenAI](https://openai.com/)
- Email integration via [Gmail API](https://developers.google.com/gmail/api)

---

**Made with ❤️ for the Portia community**

*Questions? Issues? [Open an issue](https://github.com/vaibhav1mahajan/portia-digest-bot/issues) or [start a discussion](https://github.com/vaibhav1mahajan/portia-digest-bot/discussions)!*
