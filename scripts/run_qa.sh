#!/bin/bash

set -e

echo "======================================"
echo "NutriTrackPro QA Automation"
echo "======================================"

echo ""
echo "[1/2] Running pytest..."
pytest --junitxml=reports/test-results.xml

echo ""
echo "[2/2] Generating dashboard report..."
python scripts/generate_report.py

echo ""
echo "======================================"
echo "QA run completed successfully."
echo "======================================"