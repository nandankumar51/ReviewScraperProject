"""
Test and validation utilities for the Review Scraper
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path


def validate_json_structure(json_file: str) -> bool:
    """
    Validate the structure of the output JSON file
    
    Args:
        json_file: Path to the JSON file to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required top-level keys
        required_keys = ['company', 'start_date', 'end_date', 'sources']
        for key in required_keys:
            if key not in data:
                print(f"[ERROR] Missing required key: {key}")
                return False
        
        # Validate date format
        try:
            datetime.strptime(data['start_date'], '%Y-%m-%d')
            datetime.strptime(data['end_date'], '%Y-%m-%d')
        except ValueError:
            print("[ERROR] Invalid date format")
            return False
        
        # Validate sources
        if not isinstance(data['sources'], dict):
            print("[ERROR] 'sources' must be a dictionary")
            return False
        
        # Validate each source
        for source_name, source_data in data['sources'].items():
            if 'total_reviews' not in source_data:
                print(f"[ERROR] Missing 'total_reviews' in {source_name}")
                return False
            
            if 'reviews' not in source_data:
                print(f"[ERROR] Missing 'reviews' in {source_name}")
                return False
            
            if not isinstance(source_data['reviews'], list):
                print(f"[ERROR] 'reviews' must be a list in {source_name}")
                return False
            
            # Validate each review
            for i, review in enumerate(source_data['reviews']):
                required_review_keys = ['title', 'description', 'date', 'rating', 'reviewer_name']
                for key in required_review_keys:
                    if key not in review:
                        print(f"[ERROR] Review {i} in {source_name} missing key: {key}")
                        return False
        
        print("[SUCCESS] JSON structure is valid")
        return True
    
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON file: {str(e)}")
        return False
    except FileNotFoundError:
        print(f"[ERROR] File not found: {json_file}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return False


def count_reviews(json_file: str) -> dict:
    """
    Count reviews by source from JSON file
    
    Args:
        json_file: Path to the JSON file
    
    Returns:
        Dictionary with review counts
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        counts = {}
        total = 0
        
        for source_name, source_data in data['sources'].items():
            count = len(source_data.get('reviews', []))
            counts[source_name] = count
            total += count
        
        counts['total'] = total
        return counts
    
    except Exception as e:
        print(f"[ERROR] Failed to count reviews: {str(e)}")
        return {}


def print_statistics(json_file: str) -> None:
    """
    Print statistics about the scraped reviews
    
    Args:
        json_file: Path to the JSON file
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n" + "="*50)
        print("SCRAPE STATISTICS")
        print("="*50)
        print(f"Company: {data['company']}")
        print(f"Date Range: {data['start_date']} to {data['end_date']}")
        print("-"*50)
        
        total_reviews = 0
        for source_name, source_data in data['sources'].items():
            count = len(source_data.get('reviews', []))
            total_reviews += count
            
            # Calculate average rating
            ratings = [r.get('rating', 0) for r in source_data.get('reviews', []) if r.get('rating')]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            print(f"{source_name}: {count} reviews (avg rating: {avg_rating:.1f})")
        
        print("-"*50)
        print(f"Total Reviews: {total_reviews}")
        print("="*50 + "\n")
    
    except Exception as e:
        print(f"[ERROR] Failed to print statistics: {str(e)}")


def test_environment() -> bool:
    """
    Test if the environment is properly set up
    
    Returns:
        True if environment is ready, False otherwise
    """
    print("\n[INFO] Testing environment setup...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required")
        return False
    print("[OK] Python version: " + ".".join(map(str, sys.version_info[:3])))
    
    # Check required packages
    required_packages = ['requests', 'bs4', 'selenium', 'dotenv', 'pandas', 'lxml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"[MISSING] {package}")
    
    if missing_packages:
        print(f"\n[ERROR] Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check directories
    directories = ['scrapers', 'output', 'tests']
    for directory in directories:
        if os.path.exists(directory):
            print(f"[OK] Directory exists: {directory}")
        else:
            print(f"[WARNING] Directory missing: {directory}")
    
    print("[SUCCESS] Environment is ready!\n")
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test and validate the Review Scraper")
    parser.add_argument('--test-env', action='store_true', help='Test environment setup')
    parser.add_argument('--validate', type=str, help='Validate JSON file structure')
    parser.add_argument('--stats', type=str, help='Print statistics from JSON file')
    parser.add_argument('--count', type=str, help='Count reviews in JSON file')
    
    args = parser.parse_args()
    
    if args.test_env:
        test_environment()
    elif args.validate:
        validate_json_structure(args.validate)
    elif args.stats:
        print_statistics(args.stats)
    elif args.count:
        counts = count_reviews(args.count)
        print(json.dumps(counts, indent=2))
    else:
        print("Use --help to see available options")
