#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Portia Digest Bot Setup"
echo "=========================="

# Check if Python 3.10+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -e .

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Portia API Configuration
PORTIA_API_KEY=your-portia-api-key-here
PORTIA_ORG_ID=Personal
PORTIA_API_BASE=https://api.portialabs.ai/api/v0

# Email Configuration
GMAIL_TO=your-email@example.com
DIGEST_SUBJECT_PREFIX=Portia Daily Digest

# Optional Configuration
PORTIA_CLI_TIMEOUT=120
EOF
    echo "✅ .env file created"
    echo "⚠️  Please edit .env file with your actual API key and email"
else
    echo "✅ .env file already exists"
fi

# Test installation
echo "🧪 Testing installation..."
if command -v portia-fetch &> /dev/null; then
    echo "✅ portia-fetch command is available"
    echo ""
    echo "📋 Available commands:"
    echo "  portia-fetch --help"
    echo "  portia-fetch analyze --help"
    echo "  portia-fetch summarize --help"
    echo "  portia-fetch preview-mail --help"
else
    echo "❌ portia-fetch command not found"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Portia API key and email"
echo "2. Get your API key from: https://portialabs.ai/settings/api-keys"
echo "3. Test with: portia-fetch analyze --yesterday --with-tools"
echo "4. Run daily digest: ./bin/digest-send-daily"
echo ""
echo "For detailed configuration, see README.md"
