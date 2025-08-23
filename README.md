# 🤖 Portia Digest Bot

Automated daily digest bot that analyzes Portia plan runs, generates AI summaries, and sends concise email reports via Gmail integration.

## 🎯 What & Why

**What**: A CLI tool that automatically analyzes your daily Portia plan runs, generates intelligent AI summaries, and sends beautiful digest emails to keep you informed about your automation workflows.

**Why**: As a developer using Portia for automation, you need to stay on top of your plan runs, understand performance trends, and get insights into your workflows. This bot eliminates the manual work by:
- 📊 **Automatically tracking** success rates, tool usage, and performance metrics
- 🤖 **Generating AI summaries** that highlight key insights and trends  
- 📧 **Sending daily emails** so you never miss important workflow updates
- ⚡ **Saving time** - no more manual checking of Portia dashboard

Perfect for developers, teams, and anyone using Portia who wants automated insights into their automation workflows!

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Pull and run with environment variables
docker run --rm \
  -e PORTIA_API_KEY=your-api-key \
  -e PORTIA_ORG_ID=Personal \
  -e GMAIL_TO=your-email@example.com \
  vaibhavmahajan2257/portia-digest-bot:latest

# Or use environment file
docker run --rm --env-file .env vaibhavmahajan2257/portia-digest-bot:latest
```

### Option 2: Local Setup
```bash
# Clone and setup
git clone https://github.com/vaibhav1mahajan/portia-digest-bot.git
cd portia-digest-bot
python3 -m venv venv && source venv/bin/activate
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## ⚙️ Configuration

Create `.env` file with:
```bash
PORTIA_API_KEY=prt-your-api-key-here
PORTIA_ORG_ID=Personal
GMAIL_TO=your-email@example.com
```

**Get API Key**: [Portia Labs Dashboard](https://app.portialabs.ai/)

## 📖 Usage

### Basic Commands
```bash
# Analyze yesterday's runs
portia-fetch analyze --yesterday

# Generate AI summary
portia-fetch summarize --yesterday

# Run complete daily workflow
./bin/digest-send-daily
```

### Docker Commands
```bash
# Run analysis
docker run --rm --env-file .env vaibhavmahajan2257/portia-digest-bot:latest portia-fetch analyze --yesterday

# Generate summary
docker run --rm --env-file .env vaibhavmahajan2257/portia-digest-bot:latest portia-fetch summarize --yesterday
```

## 🔄 Automation

### GitHub Actions (Free)
1. Fork this repository
2. Add secrets: `PORTIA_API_KEY`, `PORTIA_ORG_ID`, `GMAIL_TO`
3. Enable GitHub Actions

### Cron Job (Local/Server)
```bash
# Add to crontab -e
0 9 * * * cd /path/to/portia-digest-bot && ./bin/digest-send-daily
```

## 🐳 Docker Hub

**Image**: `vaibhavmahajan2257/portia-digest-bot:latest`

**Pull**: `docker pull vaibhavmahajan2257/portia-digest-bot:latest`

**Hub**: https://hub.docker.com/r/vaibhavmahajan2257/portia-digest-bot

## 📧 Email Setup

1. **Gmail Authentication**: First run will prompt for OAuth setup
2. **Follow the link** provided in the output
3. **Authorize** the application
4. **Copy the code** back to the terminal

## 🛠️ CLI Commands

```bash
portia-fetch analyze [--yesterday|--today|--since DATE|--until DATE]
portia-fetch summarize [--yesterday|--today|--since DATE|--until DATE]
portia-fetch --help
```

## 📁 Project Structure

```
portia-digest-bot/
├── portia_fetch/          # Core application
├── bin/digest-send-daily  # Daily automation script
├── Dockerfile            # Docker container
├── docker-compose.yml    # Docker orchestration
└── README.md            # This file
```

## 🔧 Troubleshooting

- **API Key Issues**: Ensure `PORTIA_API_KEY` starts with `prt-`
- **Gmail Auth**: Follow OAuth prompts on first run
- **Docker Issues**: Use `--env-file .env` for environment variables

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for the Portia community**
