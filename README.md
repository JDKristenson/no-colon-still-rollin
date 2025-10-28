# Cancer Fighting Foods Protocol Generator

A research-backed tool for generating personalized anti-cancer food protocols compatible with ketogenic diet.

## Purpose

This tool helps cancer patients:
- Identify foods with demonstrated anti-cancer properties
- Calculate therapeutic doses based on research (human, animal, in-vitro studies)
- Ensure keto compatibility
- Track compliance
- Generate reports for oncology teams
- Check medication interactions

## Features

- **PubMed Integration**: Live research updates from medical literature
- **Weight-Based Dosing**: Calculates doses based on current body weight
- **Weekly Tracking**: Monday morning weigh-ins with compliance monitoring
- **Daily Protocols**: Specific amounts, timing, and preparation methods
- **Safety Checks**: Maximum doses, side effects, drug interactions
- **Medical Reports**: Export compliance and protocols for healthcare providers

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your email for PubMed API
```

## Quick Start

```bash
# Initialize the database
python src/init_database.py

# Update research from PubMed
python src/update_research.py

# Generate protocol for user
python src/generate_protocol.py --weight 179 --user jesse

# Track daily compliance
python src/track_compliance.py

# Generate report for oncology team
python src/generate_report.py --user jesse --weeks 4
```

## Usage

### Weekly Weigh-In Protocol
- **When**: Monday morning, first thing upon waking
- **How**: Naked, before food or water
- **Record**: Update weight in system

### Daily Protocol
The system generates:
- Specific foods and amounts
- Timing throughout the day
- Preparation methods (raw, cooked, pickled, etc.)
- Keto macro tracking

### Compliance Tracking
- Simple daily check-ins
- Track what was actually consumed
- Flag missed doses
- Generate adherence metrics

## Research Sources

- PubMed/MEDLINE (primary peer-reviewed research)
- Clinical trials databases
- Nutritional databases (USDA)

## Safety

⚠️ **Medical Disclaimer**: This tool is for informational purposes and should be used alongside, not instead of, professional medical advice. Always consult with your oncology team before making dietary changes.

## License

Private use only.

## Author

Built for Jesse Mills by JD Kristenson
October 2025
