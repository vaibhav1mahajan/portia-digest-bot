# 📊 Portia Digest Bot

> **AI-Powered Daily Digest Generator for Portia Plan Runs**  
> A hackathon project that analyzes your Portia plan runs, generates intelligent summaries, and sends beautiful daily digest emails.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🎯 What This Does

Portia Digest Bot automatically:
- 🔍 **Analyzes** your daily Portia plan runs
- 🤖 **Generates** AI-powered summaries using Portia's LLM
- 📧 **Sends** beautiful daily digest emails
- 📊 **Tracks** metrics like success rates, tool usage, and performance trends

Perfect for developers who want to stay on top of their Portia automation workflows!

## 🚀 Quick Start

### Option 1: Local Development (Recommended for Hackers)

```bash
# Clone and setup in 30 seconds
git clone https://github.com/your-username/portia-digest-bot.git
cd portia-digest-bot
chmod +x setup.sh && ./setup.sh

# Configure your API keys
cp .env.example .env
# Edit .env with your Portia API key

# Test it works
portia-fetch analyze --yesterday
```

### Option 2: GitHub Actions (Zero Maintenance)

```bash
# 1. Fork this repository
# 2. Add secrets in Settings → Secrets and variables → Actions:
#    - PORTIA_API_KEY: prt-your-key-here
#    - GMAIL_TO: your-email@example.com
# 3. Workflow runs daily at 9 AM UTC automatically
```

### Option 3: Docker (Production Ready)

```bash
# Build and run
docker build -t portia-digest-bot .
docker run --rm -e PORTIA_API_KEY=prt-your-key portia-digest-bot python -m portia_fetch.cli analyze --yesterday
```

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🛠️ Local Development Setup](#️-local-development-setup)
- [☁️ Remote Deployment](#️-remote-deployment)
- [🔧 Configuration](#-configuration)
- [📖 Usage Guide](#-usage-guide)
- [🖥️ CLI Commands](#️-cli-commands)
- [📧 Email Automation](#-email-automation)
- [🔐 Authentication](#-authentication)
- [🏗️ Architecture](#️-architecture)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

---

## 🛠️ Local Development Setup

### Prerequisites

- **Python 3.10+** (check with `python3 --version`)
- **Git** (check with `git --version`)
- **Portia API Key** (get from [Portia Labs Settings](https://portialabs.ai/settings/api-keys))

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-username/portia-digest-bot.git
cd portia-digest-bot

# Quick setup (recommended)
chmod +x setup.sh
./setup.sh
```

**What `setup.sh` does:**
- Creates Python virtual environment
- Installs all dependencies
- Sets up the CLI tool
- Creates `.env.example` file

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your actual values
nano .env  # or use your favorite editor
```

**Required `.env` file contents:**
```env
# Portia API Configuration
PORTIA_API_KEY=prt-your-actual-api-key-here
PORTIA_ORG_ID=Personal

# Email Configuration
GMAIL_TO=your-email@example.com
DIGEST_SUBJECT_PREFIX=Portia Daily Digest

# Optional Settings (these are fixed for everyone)
PORTIA_API_BASE=https://api.portialabs.ai/api/v0
PORTIA_CLI_TIMEOUT=120
```

**Where to get your API key:**
1. Go to [Portia Labs Settings](https://portialabs.ai/settings/api-keys)
2. Click "Create API Key"
3. Copy the key (starts with `prt-`)
4. Paste it in your `.env` file

### Step 3: Test Your Setup

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Test analysis
portia-fetch analyze --yesterday

# Test summarization
portia-fetch summarize --yesterday

# Test complete workflow
./bin/digest-send-daily
```

### Step 4: Verify Installation

```bash
# Check if CLI tool is installed
portia-fetch --help

# Check environment variables
python -c "import os; print('API Key:', os.getenv('PORTIA_API_KEY', 'Not set')[:10] + '...')"
```

---

## ☁️ Remote Deployment

### GitHub Actions (Recommended - Free)

**Perfect for**: Automated daily runs, zero server maintenance

#### Setup:

1. **Fork this repository** to your GitHub account

2. **Add secrets** in your repository:
   - Go to `Settings` → `Secrets and variables` → `Actions`
   - Click `New repository secret`
   - Add these secrets:
     ```
     PORTIA_API_KEY: prt-your-key-here
     PORTIA_ORG_ID: Personal
     GMAIL_TO: your-email@example.com
     DIGEST_SUBJECT_PREFIX: Portia Daily Digest
     ```

3. **Workflow runs automatically**:
   - Daily at 9 AM UTC
   - Can be triggered manually
   - Results uploaded as artifacts

#### Monitor Results:

```bash
# Check workflow runs
# Go to: https://github.com/your-username/portia-digest-bot/actions

# Download results
# Click on any workflow run → Artifacts → Download digest-results
```

### Docker Deployment

**Perfect for**: Consistent environment, production deployment

#### Setup:

1. **Build the Docker image**:
   ```bash
   docker build -t portia-digest-bot .
   ```

2. **Create `.env` file**:
   ```bash
   echo "PORTIA_API_KEY=prt-your-key-here" > .env
   echo "PORTIA_ORG_ID=Personal" >> .env
   echo "GMAIL_TO=your-email@example.com" >> .env
   echo "DIGEST_SUBJECT_PREFIX=Portia Daily Digest" >> .env
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up portia-digest
   ```

4. **Or run manually**:
   ```bash
   docker run --rm \
     --env-file .env \
     portia-digest-bot \
     python -m portia_fetch.cli analyze --yesterday
   ```

### Remote Server Deployment

**Perfect for**: Full control, custom scheduling

#### Setup:

1. **SSH to your server**:
   ```bash
   ssh user@your-server.com
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/your-username/portia-digest-bot.git
   cd portia-digest-bot
   
   # Setup environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   
   # Configure environment
   cp .env.example .env
   nano .env  # Add your API keys
   ```

3. **Run manually**:
   ```bash
   # Run once
   ./bin/digest-send-daily
   
   # Or run individual commands
   portia-fetch analyze --yesterday
   portia-fetch summarize --yesterday
   ```

4. **Setup cron for automation**:
   ```bash
   crontab -e
   
   # Add this line to run daily at 9 AM UTC
   0 9 * * * cd /path/to/portia-digest-bot && source venv/bin/activate && ./bin/digest-send-daily
   ```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORTIA_API_KEY` | ✅ | - | Your Portia API key (starts with `prt-`) |
| `PORTIA_ORG_ID` | ✅ | `Personal` | Organization ID (use `Personal` for personal accounts) |
| `GMAIL_TO` | ✅ | - | Email address to send digests to |
| `DIGEST_SUBJECT_PREFIX` | ❌ | `Portia Daily Digest` | Prefix for email subjects |
| `PORTIA_API_BASE` | ❌ | `https://api.portialabs.ai/api/v0` | Fixed API URL (don't change) |
| `PORTIA_CLI_TIMEOUT` | ❌ | `120` | API request timeout in seconds |

### Where to Set Environment Variables

#### Local Development:
```bash
# In .env file
PORTIA_API_KEY=prt-your-key-here
PORTIA_ORG_ID=Personal
GMAIL_TO=your-email@example.com
```

#### GitHub Actions:
```yaml
# In repository secrets
PORTIA_API_KEY: prt-your-key-here
PORTIA_ORG_ID: Personal
GMAIL_TO: your-email@example.com
```

#### Docker:
```bash
# In .env file or command line
docker run -e PORTIA_API_KEY=prt-key -e PORTIA_ORG_ID=Personal -e GMAIL_TO=email@example.com portia-digest-bot
```

#### Remote Server:
```bash
# In .env file
echo "PORTIA_API_KEY=prt-your-key" > .env
echo "PORTIA_ORG_ID=Personal" >> .env
echo "GMAIL_TO=your-email@example.com" >> .env
```

---

## 📖 Usage Guide

### Basic Commands

```bash
# Analyze yesterday's plan runs
portia-fetch analyze --yesterday

# Analyze today's plan runs
portia-fetch analyze --today

# Analyze custom date range
portia-fetch analyze --since 2024-01-15 --until 2024-01-16

# Generate AI summary
portia-fetch summarize --yesterday

# Run complete daily workflow
./bin/digest-send-daily
```

### Advanced Usage

```bash
# Include tool usage analysis
portia-fetch analyze --yesterday --with-tools

# Generate summary for email format
portia-fetch summarize --yesterday --format email

# Analyze specific organization
PORTIA_ORG_ID=your-org-id portia-fetch analyze --yesterday

# Run with custom timeout
PORTIA_CLI_TIMEOUT=300 portia-fetch analyze --yesterday
```

### Output Files

The bot generates these files:
- `analysis_YYYY-MM-DD.json` - Raw analysis data
- `summary_YYYY-MM-DD.txt` - AI-generated summary
- `body_YYYY-MM-DD.txt` - Formatted email body

---

## 🖥️ CLI Commands

### `portia-fetch analyze`

Analyzes plan runs and generates metrics.

```bash
portia-fetch analyze [OPTIONS]

Options:
  --since TEXT     Start date (YYYY-MM-DD)
  --until TEXT     End date (YYYY-MM-DD)
  --yesterday      Analyze yesterday's runs
  --today          Analyze today's runs
  --with-tools     Include tool usage analysis
  --json           Output in JSON format
  --help           Show help message
```

**Examples:**
```bash
# Analyze yesterday
portia-fetch analyze --yesterday

# Analyze last week
portia-fetch analyze --since 2024-01-08 --until 2024-01-15

# Include tool usage
portia-fetch analyze --yesterday --with-tools
```

### `portia-fetch summarize`

Generates AI-powered summaries using Portia's LLM.

```bash
portia-fetch summarize [OPTIONS]

Options:
  --since TEXT     Start date (YYYY-MM-DD)
  --until TEXT     End date (YYYY-MM-DD)
  --yesterday      Summarize yesterday's runs
  --today          Summarize today's runs
  --format TEXT    Output format (text/email) [default: text]
  --help           Show help message
```

**Examples:**
```bash
# Generate text summary
portia-fetch summarize --yesterday

# Generate email-formatted summary
portia-fetch summarize --yesterday --format email
```

---

## 📧 Email Automation

### Daily Email Setup

#### Local Cron Job:
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM UTC
0 9 * * * cd /path/to/portia-digest-bot && source venv/bin/activate && ./bin/digest-send-daily
```

#### GitHub Actions (Automatic):
The workflow runs daily at 9 AM UTC automatically.

#### Docker Cron:
```bash
# Start cron service
docker-compose up portia-cron
```

### Email Content

The bot sends emails with:
- 📊 **Key Metrics**: Total runs, success rate, tool usage
- 🤖 **AI Summary**: Intelligent analysis of your workflows
- 📈 **Trends**: Performance insights and recommendations
- 🔧 **Tool Usage**: Most used tools and patterns

### Gmail Authentication

To send emails, you need to authenticate Gmail:

1. **Go to Portia Web Interface**: [app.portialabs.ai](https://app.portialabs.ai)
2. **Find Gmail tool setup**: Look for Gmail authentication/setup
3. **Follow OAuth flow**: Complete the Google OAuth process
4. **Test authentication**: Run `./bin/digest-send-daily`

---

## 🔐 Authentication

### Portia API Key

1. **Get your API key**:
   - Visit [Portia Labs Settings](https://portialabs.ai/settings/api-keys)
   - Click "Create API Key"
   - Copy the key (starts with `prt-`)

2. **Set in environment**:
   ```bash
   # Local development
   echo "PORTIA_API_KEY=prt-your-key-here" >> .env
   
   # GitHub Actions
   # Add as repository secret
   
   # Docker
   docker run -e PORTIA_API_KEY=prt-your-key-here portia-digest-bot
   ```

### Gmail OAuth

Required for sending emails:

1. **Authenticate in Portia**:
   - Go to [Portia Web Interface](https://app.portialabs.ai)
   - Find Gmail tool authentication
   - Complete OAuth flow

2. **Test authentication**:
   ```bash
   ./bin/digest-send-daily
   ```

---

## 🏗️ Architecture

```
portia-digest-bot/
├── portia_fetch/           # Core application
│   ├── client.py          # Portia API client
│   ├── analyzer.py        # Plan run analysis
│   ├── summarizer.py      # AI summarization
│   ├── email_sender.py    # Email sending
│   ├── email_formatter.py # Email formatting
│   └── cli.py            # Command-line interface
├── bin/
│   └── digest-send-daily # Daily automation script
├── .github/workflows/     # GitHub Actions
├── Dockerfile            # Docker container
├── docker-compose.yml    # Docker orchestration

└── requirements.txt      # Python dependencies
```

### Data Flow

```
Portia API → Analysis → AI Summary → Email Formatting → Gmail → Daily Digest
```

### Key Components

- **PortiaClient**: Handles API communication
- **PlanRunAnalyzer**: Processes plan run data
- **DigestSummarizer**: Generates AI summaries
- **PortiaEmailSender**: Sends emails via Portia
- **EmailFormatter**: Formats clean email content

---

## 🐛 Troubleshooting

### Common Issues

#### API Key Issues
```bash
# Check if API key is set
python -c "import os; print('API Key:', os.getenv('PORTIA_API_KEY', 'Not set')[:10] + '...')"

# Test API connection
portia-fetch analyze --yesterday
```

#### Gmail Authentication Issues
```bash
# Check if Gmail is authenticated
./bin/digest-send-daily

# If OAuth required, go to Portia Web Interface
# https://app.portialabs.ai
```

#### Permission Issues
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x bin/digest-send-daily
```

#### Virtual Environment Issues
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -e .
```

### Debug Mode

```bash
# Run with verbose output
PORTIA_CLI_TIMEOUT=300 portia-fetch analyze --yesterday --json

# Check logs
tail -f /var/log/cron  # For cron job logs
```

### Getting Help

1. **Check logs**: Look for error messages
2. **Verify environment**: Ensure all variables are set
3. **Test API**: Try simple commands first
4. **Check authentication**: Verify Gmail OAuth

---

## 🤝 Contributing

This is a hackathon project! Feel free to:

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** via GitHub Discussions
- 🔧 **Submit PRs** for improvements
- 📖 **Improve documentation**

### Development Setup

```bash
# Fork and clone
git clone https://github.com/your-username/portia-digest-bot.git
cd portia-digest-bot

# Setup development environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest

# Format code
black portia_fetch/
isort portia_fetch/
```

### Code Style

- **Python**: Follow PEP 8
- **CLI**: Use Typer for command-line interface
- **Documentation**: Include docstrings for all functions
- **Tests**: Add tests for new features

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Portia Labs** for the amazing API and LLM capabilities
- **Hackathon organizers** for the opportunity
- **Open source community** for the tools and libraries

---

**Made with ❤️ during a hackathon**  
*Built for developers, by developers*
