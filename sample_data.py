"""
Sample Data Generator for Testing
Generates realistic sample review data for demonstration purposes
"""
import json
from datetime import datetime, timedelta
import random


def generate_sample_reviews():
    """Generate sample review data"""
    companies = {
        "Slack": {
            "g2": [
                {
                    "title": "Great communication tool for teams",
                    "description": "Slack has revolutionized how our team communicates. The integration with other tools is seamless and the interface is very user-friendly.",
                    "date": "2023-06-15",
                    "rating": 4.5,
                    "reviewer_name": "John Smith"
                },
                {
                    "title": "Expensive but worth it",
                    "description": "The pricing is a bit high, but the value it brings to team collaboration makes up for it. Highly recommended.",
                    "date": "2023-07-20",
                    "rating": 4.0,
                    "reviewer_name": "Sarah Johnson"
                }
            ],
            "capterra": [
                {
                    "title": "Best team chat solution",
                    "description": "Slack is the industry standard for a reason. Excellent customer support and constant updates.",
                    "date": "2023-05-10",
                    "rating": 4.8,
                    "reviewer_name": "Mike Davis"
                }
            ],
            "trustpilot": [
                {
                    "title": "Transformed our workflow",
                    "description": "Since implementing Slack, our team productivity has increased by 40%. The bot ecosystem is particularly impressive.",
                    "date": "2023-08-05",
                    "rating": 5.0,
                    "reviewer_name": "Emily Brown"
                }
            ]
        },
        "Monday.com": {
            "g2": [
                {
                    "title": "Powerful project management tool",
                    "description": "Monday.com offers a great visual interface for project management. The automation features are a game-changer.",
                    "date": "2023-04-12",
                    "rating": 4.3,
                    "reviewer_name": "Robert Wilson"
                }
            ],
            "capterra": [
                {
                    "title": "Excellent for agile teams",
                    "description": "The flexibility and customization options are outstanding. Perfect for teams using agile methodologies.",
                    "date": "2023-06-22",
                    "rating": 4.6,
                    "reviewer_name": "Jennifer Lee"
                }
            ],
            "trustpilot": [
                {
                    "title": "Steep learning curve but worth it",
                    "description": "Takes some time to master, but once you do, Monday.com becomes an indispensable tool.",
                    "date": "2023-09-01",
                    "rating": 4.0,
                    "reviewer_name": "David Martinez"
                }
            ]
        }
    }
    
    return companies


def create_sample_output():
    """Create a sample JSON output file"""
    sample_data = {
        "company": "Slack",
        "source": "all",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "sources": {
            "G2": {
                "total_reviews": 2,
                "reviews": [
                    {
                        "title": "Great communication tool for teams",
                        "description": "Slack has revolutionized how our team communicates. The integration with other tools is seamless and the interface is very user-friendly.",
                        "date": "2023-06-15",
                        "rating": 4.5,
                        "reviewer_name": "John Smith",
                        "source": "G2",
                        "url": "https://www.g2.com/products/slack/reviews"
                    },
                    {
                        "title": "Expensive but worth it",
                        "description": "The pricing is a bit high, but the value it brings to team collaboration makes up for it. Highly recommended.",
                        "date": "2023-07-20",
                        "rating": 4.0,
                        "reviewer_name": "Sarah Johnson",
                        "source": "G2",
                        "url": "https://www.g2.com/products/slack/reviews"
                    }
                ]
            },
            "Capterra": {
                "total_reviews": 1,
                "reviews": [
                    {
                        "title": "Best team chat solution",
                        "description": "Slack is the industry standard for a reason. Excellent customer support and constant updates.",
                        "date": "2023-05-10",
                        "rating": 4.8,
                        "reviewer_name": "Mike Davis",
                        "source": "Capterra",
                        "url": "https://www.capterra.com/p/127896/Slack/"
                    }
                ]
            },
            "Trustpilot": {
                "total_reviews": 1,
                "reviews": [
                    {
                        "title": "Transformed our workflow",
                        "description": "Since implementing Slack, our team productivity has increased by 40%. The bot ecosystem is particularly impressive.",
                        "date": "2023-08-05",
                        "rating": 5.0,
                        "reviewer_name": "Emily Brown",
                        "source": "Trustpilot",
                        "url": "https://www.trustpilot.com/review/slack.com"
                    }
                ]
            }
        }
    }
    
    return sample_data


if __name__ == "__main__":
    import os
    
    # Create sample output directory
    os.makedirs("output", exist_ok=True)
    
    # Generate and save sample data
    sample_output = create_sample_output()
    
    with open("output/sample_output.json", "w", encoding="utf-8") as f:
        json.dump(sample_output, f, indent=2, ensure_ascii=False)
    
    print("Sample output generated: output/sample_output.json")
