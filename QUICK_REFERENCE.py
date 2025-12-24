"""
Quick Reference Guide for Review Scraper
"""

# ============================================================================
# INSTALLATION
# ============================================================================

"""
1. Navigate to project directory:
   cd ReviewScraperProject

2. Install dependencies:
   pip install -r requirements.txt

3. Verify installation:
   python test_utils.py --test-env
"""

# ============================================================================
# BASIC USAGE
# ============================================================================

"""
Command Format:
python main.py --company "NAME" --start-date YYYY-MM-DD --end-date YYYY-MM-DD [--source SOURCE] [--output FILE]

Examples:
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all
python main.py --company "Monday" --start-date 2023-01-01 --end-date 2023-06-30
python main.py --company "Salesforce" --start-date 2023-03-01 --end-date 2023-09-30 --source g2 --output slack_reviews.json
"""

# ============================================================================
# COMMAND OPTIONS
# ============================================================================

"""
--company (REQUIRED)
  Description: Company name to scrape reviews for
  Example: "Slack", "Asana", "Notion", "Monday"

--start-date (REQUIRED)
  Description: Start date for review collection
  Format: YYYY-MM-DD
  Example: 2023-01-01

--end-date (REQUIRED)
  Description: End date for review collection
  Format: YYYY-MM-DD
  Example: 2023-12-31

--source (OPTIONAL, default: all)
  Description: Review source to scrape from
  Options: g2, capterra, trustpilot, all
  Example: --source g2

--output (OPTIONAL, default: output/reviews.json)
  Description: Output file path
  Example: --output my_results.json
"""

# ============================================================================
# COMMON WORKFLOWS
# ============================================================================

"""
Workflow 1: Get all reviews for a company
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all

Workflow 2: Compare single source (G2 only)
python main.py --company "Asana" --start-date 2023-01-01 --end-date 2023-06-30 --source g2

Workflow 3: Get recent reviews
python main.py --company "Notion" --start-date 2023-09-01 --end-date 2023-12-31

Workflow 4: Custom filename
python main.py --company "Figma" --start-date 2023-01-01 --end-date 2023-12-31 --output figma_2023.json

Workflow 5: Check specific platform (Bonus Trustpilot)
python main.py --company "Salesforce" --start-date 2023-01-01 --end-date 2023-12-31 --source trustpilot
"""

# ============================================================================
# OUTPUT STRUCTURE
# ============================================================================

"""
The JSON output contains:

{
  "company": "Company Name",
  "source": "all/g2/capterra/trustpilot",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "sources": {
    "G2": {
      "total_reviews": NUMBER,
      "reviews": [
        {
          "title": "Review Title",
          "description": "Full review text",
          "date": "YYYY-MM-DD",
          "rating": 4.5,
          "reviewer_name": "Name",
          "source": "G2",
          "url": "https://..."
        }
      ]
    }
  }
}
"""

# ============================================================================
# FILE LOCATIONS
# ============================================================================

"""
Main Entry Point:
  main.py

Scrapers:
  scrapers/base_scraper.py         - Base class
  scrapers/g2_scraper.py           - G2 implementation
  scrapers/capterra_scraper.py     - Capterra implementation
  scrapers/trustpilot_scraper.py   - Trustpilot (bonus)

Utilities:
  config.py                        - Configuration
  test_utils.py                    - Testing tools
  sample_data.py                   - Sample generator

Documentation:
  README.md                        - Main guide
  SETUP.md                         - Setup guide
  ADVANCED_EXAMPLES.py             - Advanced patterns
  DELIVERABLES.md                  - Project summary
  requirements.txt                 - Dependencies

Output:
  output/reviews.json              - Generated reviews
  output/sample_output.json        - Example output
"""

# ============================================================================
# TESTING & VALIDATION
# ============================================================================

"""
Test environment setup:
  python test_utils.py --test-env

Validate JSON output:
  python test_utils.py --validate output/reviews.json

Print statistics:
  python test_utils.py --stats output/reviews.json

Count reviews:
  python test_utils.py --count output/reviews.json

Generate sample data:
  python sample_data.py
"""

# ============================================================================
# PROGRAMMATIC USAGE (Python)
# ============================================================================

"""
from scrapers.g2_scraper import G2Scraper
from datetime import datetime

# Create scraper
scraper = G2Scraper("Slack", datetime(2023, 1, 1), datetime(2023, 12, 31))

# Scrape reviews
reviews = scraper.scrape()

# Save to JSON
scraper.save_to_json("slack_reviews.json")

# Iterate reviews
for review in reviews:
    print(f"{review.title} - {review.rating} stars")
"""

# ============================================================================
# SOURCES INFORMATION
# ============================================================================

"""
G2 (https://www.g2.com)
- Leading SaaS review platform
- Business software focused
- Large review database
- Well-structured data

Capterra (https://www.capterra.com)
- Software reviews and comparisons
- Good for project management tools
- Detailed user reviews
- Reliable source

Trustpilot (https://www.trustpilot.com) [BONUS]
- General consumer and business reviews
- Covers most SaaS products
- Verified reviews
- Good for cross-validation
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Problem: "Company not found"
Solution: Check exact company name on the platform

Problem: Date format error
Solution: Use YYYY-MM-DD format (e.g., 2023-01-01)

Problem: No reviews found
Solution: Try different date range or check company name

Problem: Timeout/Connection errors
Solution: Check internet connection, try again later

Problem: Missing dependencies
Solution: pip install -r requirements.txt

For more help, see README.md and SETUP.md
"""

# ============================================================================
# SAMPLE COMMANDS
# ============================================================================

"""
# Scrape Slack reviews for 2023
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31

# Scrape Asana from G2 only
python main.py --company "Asana" --start-date 2023-01-01 --end-date 2023-12-31 --source g2

# Scrape Notion from Capterra for H2 2023
python main.py --company "Notion" --start-date 2023-07-01 --end-date 2023-12-31 --source capterra

# Scrape Salesforce from all sources, save to custom file
python main.py --company "Salesforce" --start-date 2023-01-01 --end-date 2023-12-31 --source all --output salesforce_all_sources.json

# Scrape Figma from Trustpilot (bonus source)
python main.py --company "Figma" --start-date 2023-01-01 --end-date 2023-12-31 --source trustpilot

# Get recent reviews (last 3 months)
python main.py --company "Jira" --start-date 2023-10-01 --end-date 2023-12-31

# Validate output
python test_utils.py --validate output/reviews.json

# Show statistics
python test_utils.py --stats output/reviews.json
"""

# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
1. Use proper date ranges for accurate results
2. Start with all sources, then narrow down if needed
3. Use meaningful output filenames
4. Keep backups of important results
5. Validate output before using it
6. Check sample_output.json for expected format
7. Use test_utils.py for validation
8. Review README.md for detailed information
9. Test with known companies first
10. Use appropriate delays between requests
"""

if __name__ == "__main__":
    print("Review Scraper - Quick Reference Guide")
    print("=" * 70)
    print("For full documentation, see README.md")
    print("For setup help, see SETUP.md")
    print("For advanced examples, see ADVANCED_EXAMPLES.py")
    print("=" * 70)
