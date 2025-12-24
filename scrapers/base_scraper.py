"""
Base Scraper Class - Provides abstract interface for all scrapers
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import json


class Review:
    """Data class representing a single review"""
    def __init__(self, title: str, description: str, date: str, 
                 rating: Optional[float] = None, reviewer_name: Optional[str] = None,
                 source: Optional[str] = None, url: Optional[str] = None):
        self.title = title
        self.description = description
        self.date = date
        self.rating = rating
        self.reviewer_name = reviewer_name
        self.source = source
        self.url = url

    def to_dict(self) -> Dict:
        """Convert review to dictionary"""
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'rating': self.rating,
            'reviewer_name': self.reviewer_name,
            'source': self.source,
            'url': self.url
        }


class BaseScraper(ABC):
    """Abstract base class for all review scrapers"""
    
    def __init__(self, company_name: str, start_date: datetime, 
                 end_date: datetime, source_name: str):
        self.company_name = company_name
        self.start_date = start_date
        self.end_date = end_date
        self.source_name = source_name
        self.reviews: List[Review] = []
        
    @abstractmethod
    def scrape(self) -> List[Review]:
        """Scrape reviews from the source. Must be implemented by subclasses."""
        pass
    
    def filter_by_date(self, reviews: List[Review]) -> List[Review]:
        """Filter reviews by date range"""
        filtered = []
        for review in reviews:
            try:
                review_date = datetime.strptime(review.date, '%Y-%m-%d')
                if self.start_date <= review_date <= self.end_date:
                    filtered.append(review)
            except ValueError:
                # If date parsing fails, include the review
                filtered.append(review)
        return filtered
    
    def save_to_json(self, filename: str) -> bool:
        """Save reviews to JSON file"""
        try:
            data = {
                'company': self.company_name,
                'source': self.source_name,
                'start_date': self.start_date.strftime('%Y-%m-%d'),
                'end_date': self.end_date.strftime('%Y-%m-%d'),
                'total_reviews': len(self.reviews),
                'reviews': [review.to_dict() for review in self.reviews]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")
            return False
    
    def get_reviews(self) -> List[Review]:
        """Get the list of reviews"""
        return self.reviews
