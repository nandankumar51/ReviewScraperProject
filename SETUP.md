# Setup Instructions

## Quick Start Guide

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Scraper

Basic command to scrape reviews from all sources for a company:

```bash
python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all
```

### 3. Check the Output

The reviews will be saved in `output/reviews.json` by default.

---

## Installation Details

### Requirements
- Python 3.7 or higher
- pip package manager
- Internet connection
- ~50-100MB disk space for dependencies

### Step-by-Step Installation

1. **Navigate to project directory**:
   ```bash
   cd ReviewScraperProject
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python main.py --help
   ```

---

## Usage Examples

### Example 1: Scrape G2 Only
```bash
python main.py --company "Monday" --start-date 2023-01-01 --end-date 2023-06-30 --source g2
```

### Example 2: Scrape All Sources for Salesforce
```bash
python main.py --company "Salesforce" --start-date 2023-03-01 --end-date 2023-09-30 --source all
```

### Example 3: Custom Output File
```bash
python main.py --company "Notion" --start-date 2023-01-01 --end-date 2023-12-31 --output my_custom_file.json
```

### Example 4: Trustpilot Only (Bonus Source)
```bash
python main.py --company "Asana" --start-date 2023-06-01 --end-date 2023-12-31 --source trustpilot
```

### Example 5: Capterra with Recent Reviews
```bash
python main.py --company "Jira" --start-date 2023-09-01 --end-date 2023-12-31 --source capterra
```

---

## Troubleshooting

### Issue: "No module named 'requests'"
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Company not found"
**Solution**: Try the exact company name as it appears on the platform

### Issue: Connection timeout
**Solution**: Check internet connection and try again. The script will retry automatically.

### Issue: Permission denied (on Linux/Mac)
**Solution**: Make the script executable
```bash
chmod +x main.py
python main.py --help
```

---

## Sample Output Structure

See `output/sample_output.json` for a complete example of the expected output format.

Each review includes:
- `title`: Review title
- `description`: Full review text
- `date`: Review date (YYYY-MM-DD format)
- `rating`: Numerical rating
- `reviewer_name`: Name of the reviewer
- `source`: Which platform (G2, Capterra, or Trustpilot)
- `url`: Link to the company's profile

---

## Performance Notes

- Scraping 100 reviews takes approximately 2-5 minutes depending on network speed
- The script includes automatic delays to respect server resources
- Larger date ranges may take longer to scrape
- Results are cached locally in JSON format

---

## Next Steps

1. Run a test scrape with a known company like "Slack"
2. Check the generated JSON file in `output/`
3. Analyze the reviews using your preferred tools
4. Integrate the output into your analysis pipeline

---

## Support

For issues:
1. Check the README.md for detailed information
2. Verify all dependencies are installed
3. Ensure date format is correct (YYYY-MM-DD)
4. Check internet connection
