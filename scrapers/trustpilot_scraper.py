"""
Trustpilot Review Scraper (Third Source for SaaS Reviews)
Trustpilot is a popular platform for collecting and displaying customer reviews
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List
import time
import re
import json
from scrapers.base_scraper import BaseScraper, Review


class TrustpilotScraper(BaseScraper):
    """Scraper for Trustpilot reviews"""
    
    BASE_URL = "https://www.trustpilot.com"
    
    def __init__(self, company_name: str, start_date: datetime, end_date: datetime):
        super().__init__(company_name, start_date, end_date, "Trustpilot")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _find_company_url(self) -> str:
        """Find the company URL on Trustpilot"""
        try:
            # Convert company name to URL format (lowercase, hyphens)
            company_slug = self.company_name.lower().replace(' ', '-')
            company_url = f"{self.BASE_URL}/review/{company_slug}"
            
            # Verify the URL exists
            response = requests.head(company_url, headers=self.headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return response.url
            
            # If direct URL doesn't work, try search
            search_url = f"{self.BASE_URL}/search?query={self.company_name}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find company link
            company_links = soup.find_all('a', href=re.compile(r'/review/'))
            if company_links:
                company_url = self.BASE_URL + company_links[0]['href']
                return company_url
            
            return None
        except Exception as e:
            print(f"Error finding company URL on Trustpilot: {str(e)}")
            return None
    
    def _parse_review_date(self, date_str: str) -> str:
        """Parse various date formats from Trustpilot"""
        try:
            # Handle relative dates
            if 'ago' in date_str.lower():
                match = re.search(r'(\d+)\s*(\w+)\s*ago', date_str, re.IGNORECASE)
                if match:
                    amount = int(match.group(1))
                    unit = match.group(2).lower()
                    
                    if 'month' in unit:
                        date = datetime.now() - timedelta(days=amount*30)
                        return date.strftime('%Y-%m-%d')
                    elif 'day' in unit:
                        date = datetime.now() - timedelta(days=amount)
                        return date.strftime('%Y-%m-%d')
                    elif 'week' in unit:
                        date = datetime.now() - timedelta(weeks=amount)
                        return date.strftime('%Y-%m-%d')
                    elif 'year' in unit:
                        date = datetime.now() - timedelta(days=amount*365)
                        return date.strftime('%Y-%m-%d')
                    elif 'hour' in unit:
                        date = datetime.now() - timedelta(hours=amount)
                        return date.strftime('%Y-%m-%d')
            
            # Handle explicit dates
            date_formats = ['%B %d, %Y', '%b %d, %Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
            for fmt in date_formats:
                try:
                    date = datetime.strptime(date_str.strip(), fmt)
                    return date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            return date_str
        except Exception as e:
            print(f"Error parsing date '{date_str}': {str(e)}")
            return date_str
    
    def scrape(self) -> List[Review]:
        """Scrape reviews from Trustpilot"""
        try:
            company_url = self._find_company_url()
            if not company_url:
                print(f"Could not find company '{self.company_name}' on Trustpilot")
                return []
            
            print(f"Found company URL: {company_url}")
            
            page = 1
            while len(self.reviews) < 100:
                if page == 1:
                    reviews_url = company_url
                else:
                    reviews_url = f"{company_url}?page={page}"
                
                try:
                    response = requests.get(reviews_url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page}: {str(e)}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review containers - Trustpilot uses different class names
                review_elements = soup.find_all('article', {'data-review-id': True})
                
                if not review_elements:
                    # Try alternative selector
                    review_elements = soup.find_all('div', {'class': re.compile(r'review', re.I)})
                
                if not review_elements:
                    print(f"No reviews found on page {page}")
                    break
                
                found_new_reviews = False
                for element in review_elements:
                    try:
                        # Extract review title
                        title_elem = element.find('h2', {'class': re.compile(r'reviewTitle', re.I)})
                        title = title_elem.get_text(strip=True) if title_elem else "No Title"
                        
                        # Extract review description
                        description_elem = element.find('p', {'class': re.compile(r'reviewBody', re.I)})
                        if not description_elem:
                            description_elem = element.find('p')
                        description = description_elem.get_text(strip=True) if description_elem else "No Description"
                        
                        # Extract date
                        date_elem = element.find('span', {'class': re.compile(r'reviewDate', re.I)})
                        if not date_elem:
                            date_elem = element.find('time')
                        date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y-%m-%d')
                        date = self._parse_review_date(date_str)
                        
                        # Extract rating
                        rating = None
                        rating_elem = element.find('span', {'class': re.compile(r'rating', re.I)})
                        if rating_elem:
                            try:
                                rating_text = rating_elem.get_text(strip=True)
                                rating = float(re.findall(r'\d+', rating_text)[0])
                            except:
                                pass
                        
                        # Extract reviewer name
                        reviewer_elem = element.find('span', {'class': re.compile(r'reviewer', re.I)})
                        reviewer_name = reviewer_elem.get_text(strip=True) if reviewer_elem else "Anonymous"
                        
                        # Check if we already have this review
                        existing = any(r.title == title and r.date == date for r in self.reviews)
                        if not existing and title != "No Title":
                            review = Review(
                                title=title,
                                description=description,
                                date=date,
                                rating=rating,
                                reviewer_name=reviewer_name,
                                source="Trustpilot",
                                url=company_url
                            )
                            self.reviews.append(review)
                            found_new_reviews = True
                    except Exception as e:
                        print(f"Error parsing review element: {str(e)}")
                        continue
                
                if not found_new_reviews:
                    print("No new reviews found, stopping pagination")
                    break
                
                page += 1
                time.sleep(2)
            
            # Filter by date range
            self.reviews = self.filter_by_date(self.reviews)
            
            return self.reviews
        
        except Exception as e:
            print(f"Error in Trustpilot scraper: {str(e)}")
            return []


if __name__ == "__main__":
    from datetime import datetime
    scraper = TrustpilotScraper("Slack", datetime(2023, 1, 1), datetime(2023, 12, 31))
    reviews = scraper.scrape()
    print(f"Found {len(reviews)} reviews")
    for review in reviews[:3]:
        print(f"- {review.title}")
