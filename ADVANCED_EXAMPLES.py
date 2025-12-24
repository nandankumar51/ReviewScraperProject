"""
Advanced Examples for Review Scraper
Demonstrates various use cases and integration patterns
"""

# Example 1: Using the scrapers programmatically
# ================================================
"""
from scrapers.g2_scraper import G2Scraper
from scrapers.capterra_scraper import CapterraScraper
from scrapers.trustpilot_scraper import TrustpilotScraper
from datetime import datetime

# Create a scraper instance
scraper = G2Scraper("Slack", datetime(2023, 1, 1), datetime(2023, 12, 31))

# Scrape reviews
reviews = scraper.scrape()

# Save to file
scraper.save_to_json("slack_reviews.json")

# Print reviews
for review in reviews[:5]:
    print(f"Title: {review.title}")
    print(f"Rating: {review.rating}")
    print(f"Date: {review.date}")
    print("---")
"""

# Example 2: Batch scraping multiple companies
# ==============================================
"""
from scrapers.g2_scraper import G2Scraper
from datetime import datetime
import json

companies = ["Slack", "Asana", "Monday", "Notion", "Figma"]
all_reviews = {}

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

for company in companies:
    print(f"Scraping {company}...")
    scraper = G2Scraper(company, start_date, end_date)
    reviews = scraper.scrape()
    all_reviews[company] = [r.to_dict() for r in reviews]

# Save all reviews
with open("all_companies_reviews.json", "w") as f:
    json.dump(all_reviews, f, indent=2)
"""

# Example 3: Analyzing reviews
# =============================
"""
import json
from datetime import datetime

with open("reviews.json", "r") as f:
    data = json.load(f)

# Calculate statistics
for source, source_data in data['sources'].items():
    reviews = source_data['reviews']
    
    if reviews:
        ratings = [r['rating'] for r in reviews if r['rating']]
        avg_rating = sum(ratings) / len(ratings)
        
        print(f"{source}:")
        print(f"  Total reviews: {len(reviews)}")
        print(f"  Average rating: {avg_rating:.2f}")
        print(f"  Rating range: {min(ratings):.1f} - {max(ratings):.1f}")
"""

# Example 4: Compare reviews across sources
# ==========================================
"""
import json

with open("reviews.json", "r") as f:
    data = json.load(f)

company = data['company']

print(f"Review Comparison for {company}")
print("=" * 60)

sources_summary = {}

for source, source_data in data['sources'].items():
    reviews = source_data['reviews']
    
    if reviews:
        ratings = [r['rating'] for r in reviews if r['rating']]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        sources_summary[source] = {
            'count': len(reviews),
            'avg_rating': avg_rating
        }

# Display comparison
for source, summary in sources_summary.items():
    print(f"{source:15} - Reviews: {summary['count']:3} | Avg Rating: {summary['avg_rating']:4.1f}")
"""

# Example 5: Export to CSV
# ========================
"""
import json
import csv

with open("reviews.json", "r") as f:
    data = json.load(f)

# Flatten reviews from all sources
all_reviews = []

for source, source_data in data['sources'].items():
    for review in source_data['reviews']:
        review['source'] = source
        all_reviews.append(review)

# Write to CSV
with open("reviews_export.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_reviews[0].keys())
    writer.writeheader()
    writer.writerows(all_reviews)

print(f"Exported {len(all_reviews)} reviews to reviews_export.csv")
"""

# Example 6: Find high and low rated reviews
# ===========================================
"""
import json

with open("reviews.json", "r") as f:
    data = json.load(f)

print(f"Review Analysis for {data['company']}")
print("=" * 60)

for source, source_data in data['sources'].items():
    reviews = source_data['reviews']
    
    if reviews:
        sorted_reviews = sorted(reviews, key=lambda x: x['rating'], reverse=True)
        
        print(f"\n{source}:")
        print(f"\\nHighest Rated:")
        for r in sorted_reviews[:2]:
            print(f"  - {r['title']} ({r['rating']} stars)")
        
        print(f"\\nLowest Rated:")
        for r in sorted_reviews[-2:]:
            print(f"  - {r['title']} ({r['rating']} stars)")
"""

# Example 7: Command line batch processing
# =========================================
"""
# Create a script named 'batch_scrape.py'

import subprocess
import json
from datetime import datetime

companies = [
    ("Slack", "2023-01-01", "2023-12-31"),
    ("Asana", "2023-01-01", "2023-12-31"),
    ("Notion", "2023-06-01", "2023-12-31"),
]

for company, start_date, end_date in companies:
    cmd = [
        "python", "main.py",
        "--company", company,
        "--start-date", start_date,
        "--end-date", end_date,
        "--source", "all",
        "--output", f"output/{company.lower()}_reviews.json"
    ]
    
    print(f"Processing {company}...")
    subprocess.run(cmd)
    print(f"Completed {company}\\n")
"""

# Example 8: Sentiment Analysis Integration
# ===========================================
"""
# Install TextBlob first: pip install textblob

import json
from textblob import TextBlob

with open("reviews.json", "r") as f:
    data = json.load(f)

print(f"Sentiment Analysis for {data['company']}")
print("=" * 60)

for source, source_data in data['sources'].items():
    reviews = source_data['reviews']
    
    sentiments = []
    for review in reviews:
        blob = TextBlob(review['description'])
        sentiment = blob.sentiment.polarity
        sentiments.append(sentiment)
    
    if sentiments:
        avg_sentiment = sum(sentiments) / len(sentiments)
        print(f"{source}: Average sentiment = {avg_sentiment:.3f}")
"""

# Example 9: Track review trends over time
# ========================================
"""
import json
from datetime import datetime
from collections import defaultdict

with open("reviews.json", "r") as f:
    data = json.load(f)

# Group reviews by month
monthly_data = defaultdict(list)

for source, source_data in data['sources'].items():
    for review in source_data['reviews']:
        date_obj = datetime.strptime(review['date'], '%Y-%m-%d')
        month_key = date_obj.strftime('%Y-%m')
        monthly_data[month_key].append({
            'rating': review['rating'],
            'source': source
        })

# Print trends
print(f"Review Trends for {data['company']}")
print("=" * 60)

for month in sorted(monthly_data.keys()):
    reviews = monthly_data[month]
    avg_rating = sum(r['rating'] for r in reviews if r['rating']) / len(reviews)
    print(f"{month}: {len(reviews)} reviews, avg rating: {avg_rating:.1f}")
"""

# Example 10: Filter reviews by rating
# ====================================
"""
import json

with open("reviews.json", "r") as f:
    data = json.load(f)

# Find reviews with rating >= 4.5
high_rated = []
low_rated = []

for source, source_data in data['sources'].items():
    for review in source_data['reviews']:
        if review['rating'] >= 4.5:
            high_rated.append(review)
        elif review['rating'] < 3:
            low_rated.append(review)

print(f"High Rated Reviews (>= 4.5): {len(high_rated)}")
for review in high_rated[:3]:
    print(f"  - {review['title']} ({review['rating']} stars)")

print(f"\\nLow Rated Reviews (< 3): {len(low_rated)}")
for review in low_rated[:3]:
    print(f"  - {review['title']} ({review['rating']} stars)")
"""

if __name__ == "__main__":
    print("Review Scraper - Advanced Examples")
    print("=" * 60)
    print("See the source code for 10 advanced usage examples:")
    print("1. Using scrapers programmatically")
    print("2. Batch scraping multiple companies")
    print("3. Analyzing reviews")
    print("4. Comparing reviews across sources")
    print("5. Export to CSV")
    print("6. Finding high/low rated reviews")
    print("7. Command line batch processing")
    print("8. Sentiment analysis integration")
    print("9. Tracking review trends over time")
    print("10. Filter reviews by rating")
    print("=" * 60)
