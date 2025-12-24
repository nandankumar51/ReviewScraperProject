"""
Scrapers module for Review Scraper
"""
from scrapers.base_scraper import BaseScraper, Review
from scrapers.g2_scraper import G2Scraper
from scrapers.capterra_scraper import CapterraScraper
from scrapers.trustpilot_scraper import TrustpilotScraper

__all__ = [
    'BaseScraper',
    'Review',
    'G2Scraper',
    'CapterraScraper',
    'TrustpilotScraper'
]
