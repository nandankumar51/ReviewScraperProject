# Installation & Verification Checklist

## Pre-Installation Requirements

- [ ] Python 3.7 or higher installed
- [ ] pip package manager available
- [ ] Internet connection active
- [ ] ~50-100MB free disk space

## Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\kunda\OneDrive\Desktop\ReviewScraperProject
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests beautifulsoup4 selenium python-dotenv pandas lxml webdriver-manager
```

### Step 3: Verify Installation
```bash
python test_utils.py --test-env
```

Expected output:
```
[INFO] Testing environment setup...
[OK] Python version: 3.x.x
[OK] requests is installed
[OK] bs4 is installed
[OK] selenium is installed
[OK] dotenv is installed
[OK] pandas is installed
[OK] lxml is installed
[OK] Directory exists: scrapers
[OK] Directory exists: output
[SUCCESS] Environment is ready!
```

## Verification Checklist

After installation, verify:

- [ ] Python version 3.7+ (`python --version`)
- [ ] All dependencies installed (`pip list`)
- [ ] Main script executable (`python main.py --help`)
- [ ] Sample output readable (`cat output/sample_output.json`)
- [ ] Scrapers importable (`python -c "from scrapers import *"`)

## Quick Functionality Test

### Test 1: View Help
```bash
python main.py --help
```
Expected: Shows help message with all options

### Test 2: View Environment
```bash
python test_utils.py --test-env
```
Expected: Confirms environment is ready

### Test 3: Validate Sample Output
```bash
python test_utils.py --validate output/sample_output.json
```
Expected: Confirms sample output structure is valid

### Test 4: Count Reviews in Sample
```bash
python test_utils.py --count output/sample_output.json
```
Expected: Shows review counts by source

## Common Installation Issues & Solutions

### Issue 1: "No module named 'requests'"
**Solution:**
```bash
pip install requests beautifulsoup4 selenium python-dotenv pandas lxml webdriver-manager
```

### Issue 2: Permission denied (Windows)
**Solution:** Run command prompt as Administrator

### Issue 3: Python not found
**Solution:** Ensure Python is installed and added to PATH
```bash
python --version
```

### Issue 4: Pip not found
**Solution:** Reinstall Python with pip included

## Installation Verification Commands

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list | grep -E "(requests|beautifulsoup4|selenium|pandas|lxml|python-dotenv|webdriver-manager)"

# Test import
python -c "import requests, bs4, selenium, dotenv, pandas, lxml; print('All imports successful!')"

# Check project files
ls -la main.py config.py requirements.txt
ls -la scrapers/
ls -la output/sample_output.json

# Test help
python main.py --help
```

## Platform-Specific Notes

### Windows
- Use `cmd` or PowerShell
- Path separator: `\` or `/`
- Environment: May need Administrator privileges

### macOS/Linux
- Use Terminal
- Path separator: `/`
- Environment: May need `sudo` for system-wide install

## Dependencies Overview

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.31.0 | HTTP requests |
| beautifulsoup4 | 4.12.2 | HTML parsing |
| selenium | 4.15.2 | Browser automation |
| python-dotenv | 1.0.0 | Environment variables |
| pandas | 2.1.3 | Data manipulation |
| lxml | 4.9.3 | XML/HTML processing |
| webdriver-manager | 4.0.1 | Browser driver management |

## Post-Installation

After successful installation:

1. **Read Documentation**
   - Start with `00_START_HERE.md`
   - Review `README.md`
   - Check `SETUP.md`

2. **Run First Command**
   ```bash
   python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source all
   ```

3. **Check Output**
   ```bash
   cat output/reviews.json
   ```

4. **Explore Examples**
   - View `QUICK_REFERENCE.py`
   - Review `ADVANCED_EXAMPLES.py`
   - Check `sample_output.json`

## Troubleshooting

### Scraper Not Finding Companies
- Check exact company name on the platform
- Try with quotes: `--company "Company Name"`

### Date Range Issues
- Use format: YYYY-MM-DD
- Start date must be before end date

### Network Errors
- Check internet connection
- Try again later if server is down
- Check if websites are accessible

### Performance Issues
- Normal delays built-in (2 seconds between requests)
- Large date ranges take longer
- Try smaller date ranges first

## Support Resources

| Resource | Content |
|----------|---------|
| 00_START_HERE.md | Quick overview |
| README.md | Complete guide |
| SETUP.md | Setup help |
| QUICK_REFERENCE.py | Commands |
| ADVANCED_EXAMPLES.py | Usage patterns |
| test_utils.py | Validation tools |

## Final Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed via pip
- [ ] Environment test passes
- [ ] Help command works
- [ ] Sample output validates
- [ ] First scrape command ready
- [ ] Documentation reviewed

## Next Steps

1. ✅ Installation complete
2. 👉 Run your first command
3. 📊 Check the results
4. 📖 Read the documentation
5. 🚀 Explore advanced features

---

**Installation Status**: Ready to Begin ✅

For questions, refer to README.md or SETUP.md
