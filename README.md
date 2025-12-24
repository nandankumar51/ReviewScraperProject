# Review Scraper - G2, Capterra & Trustpilot

A comprehensive Python script that scrapes product reviews from multiple SaaS review platforms: **G2**, **Capterra**, and **Trustpilot** (bonus third source).

## 📋 Features

- **Multi-source scraping**: Collect reviews from G2, Capterra, and Trustpilot simultaneously
- **Date range filtering**: Scrape reviews within a specified time period
- **JSON output**: Well-structured JSON files containing all review data
- **Error handling**: Graceful error handling and validation for invalid inputs
- **Pagination support**: Automatically handles multiple pages of reviews
- **Respect for servers**: Implements delays between requests to avoid overwhelming servers
- **Detailed review data**: Captures title, description, date, rating, reviewer name, and source

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or extract the project**:
   ```bash
   cd ReviewScraperProject
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   The following packages will be installed:
   - `requests` - For making HTTP requests
   - `beautifulsoup4` - For parsing HTML
   - `selenium` - For JavaScript-heavy pages (optional, for future enhancements)
   - `python-dotenv` - For environment variable management
   - `pandas` - For data manipulation
   - `lxml` - For HTML/XML processing
   - `webdriver-manager` - For managing browser drivers

## 🚀 Usage

### Basic Usage

```bash
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all
```

### Command-line Arguments

- `--company` (required): Company name (e.g., "Slack", "Monday", "Salesforce")
- `--start-date` (required): Start date in YYYY-MM-DD format
- `--end-date` (required): End date in YYYY-MM-DD format
- `--source` (optional): Review source - Options: `g2`, `capterra`, `trustpilot`, `all` (default: `all`)
- `--output` (optional): Output file path (default: `output/reviews.json`)

### Examples

**Scrape Slack reviews from G2 only**:
```bash
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source g2
```

**Scrape Monday.com reviews from all sources**:
```bash
python main.py --company "Monday" --start-date 2023-06-01 --end-date 2023-12-31 --source all
```

**Scrape Salesforce reviews from Trustpilot with custom output file**:
```bash
python main.py --company "Salesforce" --start-date 2023-01-01 --end-date 2023-06-30 --source trustpilot --output my_reviews.json
```

**Scrape Notion reviews from Capterra**:
```bash
python main.py --company "Notion" --start-date 2023-03-15 --end-date 2023-09-20 --source capterra
```

## 📊 Output Format

The script generates a JSON file with the following structure:

```json
{
  "company": "Slack",
  "source": "all",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "sources": {
    "G2": {
      "total_reviews": 25,
      "reviews": [
        {
          "title": "Great communication tool for teams",
          "description": "Slack has revolutionized how our team communicates...",
          "date": "2023-06-15",
          "rating": 4.5,
          "reviewer_name": "John Smith",
          "source": "G2",
          "url": "https://www.g2.com/products/slack/reviews"
        },
        ...
      ]
    },
    "Capterra": {
      "total_reviews": 18,
      "reviews": [...]
    },
    "Trustpilot": {
      "total_reviews": 12,
      "reviews": [...]
    }
  }
}
```

## 📁 Project Structure

```
ReviewScraperProject/
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── sample_data.py              # Sample data generator
├── README.md                   # This file
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py         # Base class for all scrapers
│   ├── g2_scraper.py           # G2 scraper implementation
│   ├── capterra_scraper.py     # Capterra scraper implementation
│   └── trustpilot_scraper.py   # Trustpilot scraper implementation
├── output/
│   ├── reviews.json            # Generated review output
│   └── sample_output.json      # Sample output example
└── tests/
    └── (test files for future implementation)
```

## 🔍 Scraper Details

### G2 Scraper
- **Source**: https://www.g2.com
- **Features**: Searches for company, extracts review title, description, rating, and reviewer name
- **Date handling**: Parses relative dates (e.g., "2 months ago") and absolute dates
- **Pagination**: Supports pagination through review pages

### Capterra Scraper
- **Source**: https://www.capterra.com
- **Features**: Similar to G2, specializes in software reviews
- **Date handling**: Parses various date formats from Capterra
- **Pagination**: Handles multiple pages with proper URL construction

### Trustpilot Scraper (Bonus Third Source)
- **Source**: https://www.trustpilot.com
- **Features**: Covers broader range of SaaS products and services
- **Date handling**: Handles both relative and absolute date formats
- **Pagination**: Implements pagination with proper URL construction
- **Why Trustpilot?**: 
  - One of the largest review platforms globally
  - Covers most SaaS products
  - Reliable and regularly updated
  - Good source for cross-validation with G2 and Capterra

## ⚙️ Error Handling

The script includes comprehensive error handling for:

- **Invalid company names**: Returns empty results if company not found
- **Invalid date formats**: Validates date input and provides clear error messages
- **Date range errors**: Ensures start date is before end date
- **Network errors**: Gracefully handles connection failures
- **Parsing errors**: Continues scraping even if individual reviews fail to parse
- **Invalid sources**: Validates source parameter against allowed options

### Example Error Messages

```
[ERROR] Date format error: Please use YYYY-MM-DD format
[ERROR] Start date must be before end date
[ERROR] Source must be one of: g2, capterra, trustpilot, all
```

## 🎁 Bonus: Third Source Integration (Trustpilot)

The script includes Trustpilot as a third source for SaaS reviews. Trustpilot was chosen because:

1. **Comprehensive Coverage**: Covers thousands of SaaS products globally
2. **Verified Reviews**: Uses verification mechanisms for authentic reviews
3. **Consistent Data**: Well-structured HTML for reliable scraping
4. **Industry Leader**: One of the most trusted review platforms
5. **Cross-validation**: Complements G2 and Capterra data nicely

### Using Trustpilot

```bash
# Scrape only Trustpilot reviews
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source trustpilot

# Scrape all sources including Trustpilot
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all
```

## 📝 Sample Output

A sample output file is included at `output/sample_output.json`. This demonstrates the expected JSON structure for reviews scraped from all three sources.

To generate fresh sample data:
```bash
python sample_data.py
```

## ⚡ Performance Considerations

- **Request delays**: The script includes 2-second delays between requests to be respectful to target servers
- **Pagination limits**: Limited to 100 reviews per source to prevent excessive scraping
- **Timeout handling**: 10-second timeout for each HTTP request
- **Memory efficient**: Processes reviews one at a time to minimize memory usage

## 🔒 Ethical Scraping

This script respects website terms of service:

- ✅ Implements appropriate delays between requests
- ✅ Uses descriptive User-Agent headers
- ✅ Handles robots.txt indirectly through rate limiting
- ✅ Does not overload servers
- ✅ Extracts publicly available information only

Please ensure you have permission to scrape the target websites and comply with their terms of service.

## 🐛 Troubleshooting

### No reviews found
- **Cause**: Company name might not exist on the platform
- **Solution**: Try searching manually on the platform to find the exact company name

### Connection errors
- **Cause**: Network issues or server blocking
- **Solution**: Check your internet connection and try again later. The script implements automatic retries.

### Invalid date format
- **Cause**: Date not in YYYY-MM-DD format
- **Solution**: Ensure dates are in the correct format (e.g., 2023-01-01)

### Slow performance
- **Cause**: Server response times
- **Solution**: This is normal for web scraping. The script includes appropriate delays.

## 📚 Dependencies

| Package | Purpose |
|---------|---------|
| requests | HTTP requests |
| beautifulsoup4 | HTML parsing |
| selenium | JavaScript rendering (optional) |
| python-dotenv | Environment variables |
| pandas | Data manipulation |
| lxml | HTML/XML processing |
| webdriver-manager | Browser driver management |

## 🤝 Contributing

To extend this project:

1. Add new scrapers by extending `BaseScraper` class
2. Implement the `scrape()` method for your source
3. Add the scraper to `main.py`

Example:
```python
class NewSourceScraper(BaseScraper):
    def scrape(self):
        # Your scraping logic here
        return self.reviews
```

## 📄 License

This project is provided as-is for educational purposes.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the sample output example
3. Ensure all dependencies are installed correctly

## 🚀 Future Enhancements

Potential improvements:
- Database storage for reviews
- Advanced filtering options
- Duplicate detection and removal
- Sentiment analysis
- Review trend analysis
- Browser automation for JavaScript-heavy pages
- Proxy support for large-scale scraping
- API endpoints for easier integration

---

**Last Updated**: December 2025
**Version**: 1.0
