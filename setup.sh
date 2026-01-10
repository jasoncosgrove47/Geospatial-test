#!/bin/bash

# Setup script for Geospatial Land Coverage Analysis

echo "=== Geospatial Land Coverage Analysis Setup ==="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check Quarto installation
echo ""
if ! command -v quarto &> /dev/null; then
    echo "⚠ Quarto is not installed."
    echo "Please install Quarto from: https://quarto.org/docs/get-started/"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  wget https://quarto.org/download/latest/quarto-linux-amd64.deb"
    echo "  sudo dpkg -i quarto-linux-amd64.deb"
    echo ""
    echo "For macOS:"
    echo "  brew install quarto"
else
    echo "✓ Quarto found: $(quarto --version)"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To render the analysis, run:"
echo "  quarto render land_coverage_analysis.qmd"
echo ""
