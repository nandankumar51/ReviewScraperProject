"""
Capterra Review Scraper
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List
import time
import re
from scrapers.base_scraper import BaseScraper, Review


class CapterraScraper(BaseScraper):
    """Scraper for Capterra reviews"""
    
    BASE_URL = "https://www.capterra.com"
    
    def __init__(self, company_name: str, start_date: datetime, end_date: datetime):
        super().__init__(company_name, start_date, end_date, "Capterra")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _find_company_url(self) -> str:
        """Find the company URL on Capterra"""
        try:
            search_url = f"{self.BASE_URL}/search?q={self.company_name}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find the first product result
            product_results = soup.find_all('a', {'data-test': 'product_result_link'})
            if product_results:
                company_url = self.BASE_URL + product_results[0]['href']
                return company_url
            
            # Fallback: Look for product links
            links = soup.find_all('a', href=re.compile(r'/software/'))
            if links:
                company_url = self.BASE_URL + links[0]['href']
                return company_url
            
            return None
        except Exception as e:
            print(f"Error finding company URL on Capterra: {str(e)}")
            return None
    
    def _parse_review_date(self, date_str: str) -> str:
        """Parse various date formats from Capterra"""
        try:
            # Handle relative dates like "3 months ago"
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
            
            # Handle explicit dates
            date_formats = ['%B %d, %Y', '%b %d, %Y', '%Y-%m-%d', '%m/%d/%Y']
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
        """Scrape reviews from Capterra"""
        try:
            company_url = self._find_company_url()
            if not company_url:
                print(f"Could not find company '{self.company_name}' on Capterra")
                return []
            
            print(f"Found company URL: {company_url}")
            
            page = 1
            while len(self.reviews) < 100:
                reviews_url = f"{company_url}#reviews"
                if page > 1:
                    reviews_url = f"{company_url}?reviews_filter_json=%5B%5D&sort_type=most_recent&page={page}#reviews"
                
                try:
                    response = requests.get(reviews_url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page}: {str(e)}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review containers
                review_elements = soup.find_all('div', {'data-test': 'ReviewCard'})
                
                if not review_elements:
                    print(f"No reviews found on page {page}")
                    break
                
                for element in review_elements:
                    try:
                        # Extract review title
                        title_elem = element.find('h3')
                        title = title_elem.get_text(strip=True) if title_elem else "No Title"
                        
                        # Extract review description
                        description_elems = element.find_all('p')
                        description = ""
                        for desc_elem in description_elems:
                            text = desc_elem.get_text(strip=True)
                            if text and len(text) > 10:
                                description = text
                                break
                        if not description:
                            description = "No Description"
                        
                        # Extract date
                        date_elem = element.find('span', {'data-test': 'review_date'})
                        date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y-%m-%d')
                        date = self._parse_review_date(date_str)
                        
                        # Extract rating
                        rating_elem = element.find('span', {'data-test': 'star_rating'})
                        rating = None
                        if rating_elem:
                            try:
                                rating_text = rating_elem.get_text(strip=True)
                                rating = float(re.findall(r'\d+', rating_text)[0])
                            except:
                                pass
                        
                        # Extract reviewer name
                        reviewer_elem = element.find('span', {'data-test': 'reviewer_name'})
                        reviewer_name = reviewer_elem.get_text(strip=True) if reviewer_elem else "Anonymous"
                        
                        review = Review(
                            title=title,
                            description=description,
                            date=date,
                            rating=rating,
                            reviewer_name=reviewer_name,
                            source="Capterra",
                            url=company_url
                        )
                        
                        self.reviews.append(review)
                    except Exception as e:
                        print(f"Error parsing review element: {str(e)}")
                        continue
                
                page += 1
                time.sleep(2)
            
            # Filter by date range
            self.reviews = self.filter_by_date(self.reviews)
            
            return self.reviews
        
        except Exception as e:
            print(f"Error in Capterra scraper: {str(e)}")
            return []


if __name__ == "__main__":
    from datetime import datetime
    scraper = CapterraScraper("Slack", datetime(2023, 1, 1), datetime(2023, 12, 31))
    reviews = scraper.scrape()
    print(f"Found {len(reviews)} reviews")
    for review in reviews[:3]:
        print(f"- {review.title}")
