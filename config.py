"""
Configuration and constants for the Review Scraper
"""

# Supported review sources
SUPPORTED_SOURCES = ['g2', 'capterra', 'trustpilot', 'all']

# Source configurations
SOURCE_CONFIG = {
    'g2': {
        'name': 'G2',
        'url': 'https://www.g2.com',
        'enabled': True,
        'description': 'Business software reviews'
    },
    'capterra': {
        'name': 'Capterra',
        'url': 'https://www.capterra.com',
        'enabled': True,
        'description': 'Software reviews and comparisons'
    },
    'trustpilot': {
        'name': 'Trustpilot',
        'url': 'https://www.trustpilot.com',
        'enabled': True,
        'description': 'General consumer and business reviews'
    }
}

# Scraping configuration
SCRAPING_CONFIG = {
    'max_reviews_per_source': 100,  # Maximum reviews to scrape per source
    'request_timeout': 10,  # Timeout for HTTP requests in seconds
    'request_delay': 2,  # Delay between requests in seconds
    'max_pages': 50,  # Maximum number of pages to scrape
}

# HTTP headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Date formats to try when parsing
DATE_FORMATS = [
    '%B %d, %Y',      # January 01, 2023
    '%b %d, %Y',      # Jan 01, 2023
    '%Y-%m-%d',       # 2023-01-01
    '%m/%d/%Y',       # 01/01/2023
    '%d/%m/%Y',       # 01/01/2023
    '%Y/%m/%d',       # 2023/01/01
]

# Output configuration
OUTPUT_CONFIG = {
    'default_output_file': 'output/reviews.json',
    'output_directory': 'output',
    'ensure_directory': True
}

# Error messages
ERROR_MESSAGES = {
    'invalid_date_format': 'Date format error: Please use YYYY-MM-DD format',
    'invalid_date_range': 'Start date must be before end date',
    'invalid_source': 'Source must be one of: {}',
    'empty_company_name': 'Company name cannot be empty',
    'company_not_found': 'Could not find company {} on {}',
}

# Success messages
SUCCESS_MESSAGES = {
    'scraping_started': '[START] Review Scraper',
    'company_found': '[INFO] Company: {}',
    'date_range': '[INFO] Date Range: {} to {}',
    'source_info': '[INFO] Source(s): {}',
    'scraping_complete': '[DONE] Scraping completed successfully!',
}
