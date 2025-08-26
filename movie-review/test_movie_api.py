#!/usr/bin/env python3
"""
Test script for the Movie Review API

This script demonstrates the main functionality of the API including:
- Creating movies and reviews
- Retrieving data with filters
- Updating and deleting records
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"


def test_api():
    """Test the Movie Review API endpoints"""
    print("🎬 Testing Movie Review API")
    print("=" * 50)

    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test getting all movies
    print("\n2. Getting all movies...")
    response = requests.get(f"{BASE_URL}/movies")
    print(f"Status: {response.status_code}")
    movies_data = response.json()
    print(f"Total movies: {movies_data['total_count']}")
    if movies_data["movies"]:
        print(f"First movie: {movies_data['movies'][0]['title']}")

    # Test getting all reviews
    print("\n3. Getting all reviews...")
    response = requests.get(f"{BASE_URL}/reviews")
    print(f"Status: {response.status_code}")
    reviews_data = response.json()
    print(f"Total reviews: {reviews_data['total_count']}")

    # Test creating a new movie
    print("\n4. Creating a new movie...")
    new_movie = {
        "title": "Pulp Fiction",
        "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
        "genre": "drama",
        "release_year": 1994,
        "director": "Quentin Tarantino",
        "duration_minutes": 154,
    }
    response = requests.post(f"{BASE_URL}/movies?auto_id=true", json=new_movie)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        created_movie = response.json()["movie"]
        movie_id = created_movie["id"]
        print(f"Created movie with ID: {movie_id}")

        # Test creating a review for the new movie
        print("\n5. Creating a review for the new movie...")
        new_review = {
            "movie_id": movie_id,
            "reviewer_name": "Film Critic",
            "rating": 9.2,
            "comment": "A masterpiece of storytelling with incredible dialogue and memorable characters. Tarantino's best work.",
        }
        response = requests.post(f"{BASE_URL}/reviews?auto_id=true", json=new_review)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("Review created successfully!")

    # Test filtering movies by genre
    print("\n6. Filtering movies by science fiction genre...")
    response = requests.get(f"{BASE_URL}/movies?genre=science_fiction")
    print(f"Status: {response.status_code}")
    sf_movies = response.json()
    print(f"Science fiction movies found: {sf_movies['total_count']}")

    # Test filtering reviews by rating
    print("\n7. Filtering reviews with rating >= 9.0...")
    response = requests.get(f"{BASE_URL}/reviews?min_rating=9.0")
    print(f"Status: {response.status_code}")
    high_rated_reviews = response.json()
    print(f"High-rated reviews found: {high_rated_reviews['total_count']}")

    # Test getting movie with reviews
    print("\n8. Getting reviews for The Matrix (movie ID 1)...")
    response = requests.get(f"{BASE_URL}/movies/1/reviews")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        movie_reviews = response.json()
        print(f"Reviews for movie: {movie_reviews['total_reviews']}")

    # Test getting statistics
    print("\n9. Getting API statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total movies: {stats['total_movies']}")
        print(f"Total reviews: {stats['total_reviews']}")
        print(f"Average rating: {stats['average_rating_overall']}")

    print("\n✅ API test completed!")


if __name__ == "__main__":
    try:
        test_api()
    except requests.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the server is running with:")
        print("uvicorn movie_review_api:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
