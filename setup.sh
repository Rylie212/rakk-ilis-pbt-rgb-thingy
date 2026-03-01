#!/bin/bash
# Quick setup script for Rakk Ilis RGB Controller
# Linux/macOS only - Windows users, run the commands manually

echo "🎮 Rakk Ilis RGB Setup"
echo "===================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Find keyboard
echo ""
echo "Scanning for Rakk Ilis keyboard..."
echo "(This might need sudo permission)"
echo ""

python3 find_keyboard.py

echo ""
echo "===================="
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run the test suite:  python3 test.py"
echo "2. Start RGB sync:      python3 main.py"
echo ""
echo "If you get permission errors, use:"
echo "  sudo python3 find_keyboard.py"
echo "  sudo python3 test.py"
echo "  sudo python3 main.py"
