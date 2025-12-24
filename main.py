"""
Review Scraper Main Script
Scrapes product reviews from G2, Capterra, and Trustpilot
"""
import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path
from scrapers.g2_scraper import G2Scraper
from scrapers.capterra_scraper import CapterraScraper
from scrapers.trustpilot_scraper import TrustpilotScraper


def validate_inputs(company_name: str, start_date: str, end_date: str, source: str) -> tuple:
    """
    Validate input parameters
    
    Args:
        company_name: Name of the company
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        source: Source (G2, Capterra, Trustpilot, or all)
    
    Returns:
        Tuple of (company_name, start_date_obj, end_date_obj, source)
    
    Raises:
        ValueError: If inputs are invalid
    """
    # Validate company name
    if not company_name or not company_name.strip():
        raise ValueError("Company name cannot be empty")
    
    company_name = company_name.strip()
    
    # Validate dates
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Date format error: {str(e)}. Please use YYYY-MM-DD format")
    
    if start > end:
        raise ValueError("Start date must be before end date")
    
    # Validate source
    valid_sources = ['g2', 'capterra', 'trustpilot', 'all']
    if source.lower() not in valid_sources:
        raise ValueError(f"Source must be one of: {', '.join(valid_sources)}")
    
    return company_name, start, end, source.lower()


def scrape_reviews(company_name: str, start_date: datetime, end_date: datetime, 
                   source: str) -> dict:
    """
    Scrape reviews from specified source(s)
    
    Args:
        company_name: Name of the company
        start_date: Start date object
        end_date: End date object
        source: Source to scrape from
    
    Returns:
        Dictionary containing reviews from all sources
    """
    results = {
        'company': company_name,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'sources': {}
    }
    
    sources_to_scrape = []
    if source == 'all':
        sources_to_scrape = ['g2', 'capterra', 'trustpilot']
    else:
        sources_to_scrape = [source]
    
    # Scrape from G2
    if 'g2' in sources_to_scrape:
        print(f"\n[INFO] Scraping G2 for '{company_name}'...")
        try:
            g2_scraper = G2Scraper(company_name, start_date, end_date)
            reviews = g2_scraper.scrape()
            results['sources']['G2'] = {
                'total_reviews': len(reviews),
                'reviews': [r.to_dict() for r in reviews]
            }
            print(f"[SUCCESS] Found {len(reviews)} reviews from G2")
        except Exception as e:
            print(f"[ERROR] G2 scraping failed: {str(e)}")
            results['sources']['G2'] = {'error': str(e), 'total_reviews': 0}
    
    # Scrape from Capterra
    if 'capterra' in sources_to_scrape:
        print(f"\n[INFO] Scraping Capterra for '{company_name}'...")
        try:
            capterra_scraper = CapterraScraper(company_name, start_date, end_date)
            reviews = capterra_scraper.scrape()
            results['sources']['Capterra'] = {
                'total_reviews': len(reviews),
                'reviews': [r.to_dict() for r in reviews]
            }
            print(f"[SUCCESS] Found {len(reviews)} reviews from Capterra")
        except Exception as e:
            print(f"[ERROR] Capterra scraping failed: {str(e)}")
            results['sources']['Capterra'] = {'error': str(e), 'total_reviews': 0}
    
    # Scrape from Trustpilot
    if 'trustpilot' in sources_to_scrape:
        print(f"\n[INFO] Scraping Trustpilot for '{company_name}'...")
        try:
            trustpilot_scraper = TrustpilotScraper(company_name, start_date, end_date)
            reviews = trustpilot_scraper.scrape()
            results['sources']['Trustpilot'] = {
                'total_reviews': len(reviews),
                'reviews': [r.to_dict() for r in reviews]
            }
            print(f"[SUCCESS] Found {len(reviews)} reviews from Trustpilot")
        except Exception as e:
            print(f"[ERROR] Trustpilot scraping failed: {str(e)}")
            results['sources']['Trustpilot'] = {'error': str(e), 'total_reviews': 0}
    
    return results


def save_results(results: dict, output_file: str) -> bool:
    """
    Save results to JSON file
    
    Args:
        results: Dictionary containing scraped reviews
        output_file: Path to output file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n[SUCCESS] Results saved to {output_file}")
        return True
    except Exception as e:
        print(f"\n[ERROR] Failed to save results: {str(e)}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Scrape product reviews from multiple sources (G2, Capterra, Trustpilot)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --company "Slack" --start-date 2023-01-01 --end-date 2023-12-31 --source g2
  python main.py --company "Monday" --start-date 2023-06-01 --end-date 2023-12-31 --source all
  python main.py --company "Salesforce" --start-date 2023-01-01 --end-date 2023-06-30 --source trustpilot --output results.json
        """
    )
    
    parser.add_argument(
        '--company',
        required=True,
        help='Company name (e.g., "Slack", "Monday", "Salesforce")'
    )
    parser.add_argument(
        '--start-date',
        required=True,
        help='Start date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--end-date',
        required=True,
        help='End date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--source',
        default='all',
        help='Source to scrape from: g2, capterra, trustpilot, or all (default: all)'
    )
    parser.add_argument(
        '--output',
        default='output/reviews.json',
        help='Output file path (default: output/reviews.json)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        company_name, start_date, end_date, source = validate_inputs(
            args.company,
            args.start_date,
            args.end_date,
            args.source
        )
        
        print(f"[START] Review Scraper")
        print(f"[INFO] Company: {company_name}")
        print(f"[INFO] Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"[INFO] Source(s): {source.upper()}")
        
        # Scrape reviews
        results = scrape_reviews(company_name, start_date, end_date, source)
        
        # Calculate total reviews
        total_reviews = sum(
            src.get('total_reviews', 0) 
            for src in results['sources'].values()
        )
        
        print(f"\n[SUMMARY] Total reviews scraped: {total_reviews}")
        
        # Save results
        success = save_results(results, args.output)
        
        if success:
            print(f"[DONE] Scraping completed successfully!")
            return 0
        else:
            return 1
    
    except ValueError as e:
        print(f"[ERROR] {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\n[CANCELLED] Scraping cancelled by user")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
