"""
G2 Review Scraper
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import time
import re
from scrapers.base_scraper import BaseScraper, Review


class G2Scraper(BaseScraper):
    """Scraper for G2 reviews"""
    
    BASE_URL = "https://www.g2.com"
    
    def __init__(self, company_name: str, start_date: datetime, end_date: datetime):
        super().__init__(company_name, start_date, end_date, "G2")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _find_company_url(self) -> str:
        """Find the company URL on G2"""
        try:
            search_url = f"{self.BASE_URL}/products?utf8=%E2%9C%93&search={self.company_name}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find product link
            product_link = soup.find('a', {'data-test': 'product-link'})
            if product_link:
                company_url = self.BASE_URL + product_link['href']
                return company_url
            
            # Fallback: Look for any link containing the company name
            links = soup.find_all('a', href=re.compile(r'/products/'))
            if links:
                return self.BASE_URL + links[0]['href']
            
            return None
        except Exception as e:
            print(f"Error finding company URL on G2: {str(e)}")
            return None
    
    def _parse_review_date(self, date_str: str) -> str:
        """Parse various date formats from G2"""
        try:
            # Handle "X months ago" format
            if 'ago' in date_str.lower():
                if 'month' in date_str.lower():
                    months = int(re.findall(r'\d+', date_str)[0])
                    from dateutil.relativedelta import relativedelta
                    date = datetime.now() - relativedelta(months=months)
                    return date.strftime('%Y-%m-%d')
                elif 'day' in date_str.lower():
                    days = int(re.findall(r'\d+', date_str)[0])
                    date = datetime.now() - timedelta(days=days)
                    return date.strftime('%Y-%m-%d')
                elif 'week' in date_str.lower():
                    weeks = int(re.findall(r'\d+', date_str)[0])
                    date = datetime.now() - timedelta(weeks=weeks)
                    return date.strftime('%Y-%m-%d')
            
            # Handle explicit dates
            date_formats = ['%B %d, %Y', '%b %d, %Y', '%Y-%m-%d']
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
        """Scrape reviews from G2"""
        try:
            company_url = self._find_company_url()
            if not company_url:
                print(f"Could not find company '{self.company_name}' on G2")
                return []
            
            print(f"Found company URL: {company_url}")
            
            page = 1
            while len(self.reviews) < 100:  # Limit to prevent excessive scraping
                reviews_url = f"{company_url}/reviews?page={page}"
                
                try:
                    response = requests.get(reviews_url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching page {page}: {str(e)}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all review containers
                review_elements = soup.find_all('div', {'data-test': 'review-card'})
                
                if not review_elements:
                    print(f"No reviews found on page {page}")
                    break
                
                for element in review_elements:
                    try:
                        # Extract review information
                        title_elem = element.find('h3')
                        title = title_elem.get_text(strip=True) if title_elem else "No Title"
                        
                        description_elem = element.find('p', {'data-test': 'review-body'})
                        description = description_elem.get_text(strip=True) if description_elem else "No Description"
                        
                        date_elem = element.find('time')
                        date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y-%m-%d')
                        date = self._parse_review_date(date_str)
                        
                        # Extract rating
                        rating_elem = element.find('span', {'data-test': 'star-rating'})
                        rating = None
                        if rating_elem:
                            try:
                                rating = float(rating_elem.get_text(strip=True).split('/')[0])
                            except:
                                pass
                        
                        # Extract reviewer name
                        reviewer_elem = element.find('div', {'data-test': 'reviewer-name'})
                        reviewer_name = reviewer_elem.get_text(strip=True) if reviewer_elem else "Anonymous"
                        
                        review = Review(
                            title=title,
                            description=description,
                            date=date,
                            rating=rating,
                            reviewer_name=reviewer_name,
                            source="G2",
                            url=company_url
                        )
                        
                        self.reviews.append(review)
                    except Exception as e:
                        print(f"Error parsing review element: {str(e)}")
                        continue
                
                page += 1
                time.sleep(2)  # Be respectful to the server
            
            # Filter by date range
            self.reviews = self.filter_by_date(self.reviews)
            
            return self.reviews
        
        except Exception as e:
            print(f"Error in G2 scraper: {str(e)}")
            return []


if __name__ == "__main__":
    from datetime import datetime
    scraper = G2Scraper("Slack", datetime(2023, 1, 1), datetime(2023, 12, 31))
    reviews = scraper.scrape()
    print(f"Found {len(reviews)} reviews")
    for review in reviews[:3]:
        print(f"- {review.title}")
