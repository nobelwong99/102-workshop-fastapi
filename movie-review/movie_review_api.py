"""
Movie Review FastAPI Application

A comprehensive REST API for managing movies and reviews with CRUD operations.
This application provides endpoints to create, read, update, and delete movies
and reviews with strict validation and filtering capabilities.

Author: AI Assistant
Date: 2025-01-11
"""

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import json
import os

# Data file paths
MOVIES_FILE = "movies.json"
REVIEWS_FILE = "reviews.json"

# Error messages
MOVIE_NOT_FOUND_MESSAGE = "Movie not found"
REVIEW_NOT_FOUND_MESSAGE = "Review not found"

# Constants for query parameters
MIN_RATING_DESC = "Minimum rating"
MAX_RATING_DESC = "Maximum rating"
SORT_ORDER_DESC = "Sort order: asc or desc"


class GenreEnum(str, Enum):
    """Enumeration of movie genres"""

    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    HORROR = "horror"
    ROMANCE = "romance"
    THRILLER = "thriller"
    FANTASY = "fantasy"
    SCIENCE_FICTION = "science_fiction"
    DOCUMENTARY = "documentary"
    ANIMATION = "animation"


class Movie(BaseModel):
    """
    Movie model representing a movie item.

    Attributes:
        id (int): Unique identifier for the movie
        title (str): Title of the movie (3-200 characters)
        description (str): Description of the movie
        genre (GenreEnum): Genre of the movie
        release_year (int): Year the movie was released (1888-current year)
        director (str): Director of the movie (2-100 characters)
        duration_minutes (int): Duration in minutes (1-600)
        rating (Optional[float]): Average rating (calculated from reviews)
        review_count (Optional[int]): Number of reviews (calculated)
    """

    id: int
    title: str = Field(..., min_length=3, max_length=200, description="Movie title")
    description: str = Field(
        ..., min_length=10, max_length=1000, description="Movie description"
    )
    genre: GenreEnum = Field(..., description="Movie genre")
    release_year: int = Field(
        ..., ge=1888, le=datetime.now().year, description="Release year"
    )
    director: str = Field(
        ..., min_length=2, max_length=100, description="Director name"
    )
    duration_minutes: int = Field(..., ge=1, le=600, description="Duration in minutes")
    rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="Average rating")
    review_count: Optional[int] = Field(None, ge=0, description="Number of reviews")

    @validator("title")
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        return v.strip()

    @validator("director")
    def validate_director(cls, v):
        if not v.strip():
            raise ValueError("Director name cannot be empty or only whitespace")
        return v.strip()


class MovieCreate(BaseModel):
    """Model for creating a new movie (without computed fields)"""

    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=1000)
    genre: GenreEnum
    release_year: int = Field(..., ge=1888, le=datetime.now().year)
    director: str = Field(..., min_length=2, max_length=100)
    duration_minutes: int = Field(..., ge=1, le=600)

    @validator("title", "director")
    def validate_strings(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty or only whitespace")
        return v.strip()


class Review(BaseModel):
    """
    Review model representing a movie review.

    Attributes:
        id (int): Unique identifier for the review
        movie_id (int): ID of the movie being reviewed
        reviewer_name (str): Name of the reviewer (2-50 characters)
        rating (float): Rating given (1.0-10.0)
        comment (str): Review comment (10-500 characters)
        created_at (datetime): Timestamp when review was created
    """

    id: int
    movie_id: int = Field(..., gt=0, description="ID of the movie being reviewed")
    reviewer_name: str = Field(
        ..., min_length=2, max_length=50, description="Reviewer name"
    )
    rating: float = Field(..., ge=1.0, le=10.0, description="Rating from 1.0 to 10.0")
    comment: str = Field(
        ..., min_length=10, max_length=500, description="Review comment"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )

    @validator("reviewer_name")
    def validate_reviewer_name(cls, v):
        if not v.strip():
            raise ValueError("Reviewer name cannot be empty or only whitespace")
        return v.strip()

    @validator("comment")
    def validate_comment(cls, v):
        if not v.strip():
            raise ValueError("Comment cannot be empty or only whitespace")
        return v.strip()


class ReviewCreate(BaseModel):
    """Model for creating a new review"""

    movie_id: int = Field(..., gt=0)
    reviewer_name: str = Field(..., min_length=2, max_length=50)
    rating: float = Field(..., ge=1.0, le=10.0)
    comment: str = Field(..., min_length=10, max_length=500)

    @validator("reviewer_name", "comment")
    def validate_strings(cls, v):
        if not v.strip():
            raise ValueError("Field cannot be empty or only whitespace")
        return v.strip()


# Initialize FastAPI application
app = FastAPI(
    title="Movie Review API",
    description="A comprehensive API for managing movies and reviews",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Utility functions for data persistence
def load_data_from_json(file_path: str) -> List[dict]:
    """Load data from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error reading data from {file_path}: {e}")
        return []


def save_data_to_json(data: List[dict], file_path: str):
    """Save data to JSON file"""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def calculate_movie_stats(movie_id: int) -> tuple[Optional[float], int]:
    """Calculate average rating and review count for a movie"""
    reviews = load_data_from_json(REVIEWS_FILE)
    movie_reviews = [r for r in reviews if r["movie_id"] == movie_id]

    if not movie_reviews:
        return None, 0

    avg_rating = sum(r["rating"] for r in movie_reviews) / len(movie_reviews)
    return round(avg_rating, 2), len(movie_reviews)


def update_movie_stats(movie_id: int):
    """Update movie statistics after review changes"""
    movies = load_data_from_json(MOVIES_FILE)

    for movie in movies:
        if movie["id"] == movie_id:
            avg_rating, review_count = calculate_movie_stats(movie_id)
            movie["rating"] = avg_rating
            movie["review_count"] = review_count
            save_data_to_json(movies, MOVIES_FILE)
            break


def get_movie_by_id(movie_id: int) -> Optional[dict]:
    """Get movie by ID"""
    movies = load_data_from_json(MOVIES_FILE)
    return next((movie for movie in movies if movie["id"] == movie_id), None)


# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint that returns API information.

    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Movie Review API",
        "version": "1.0.0",
        "endpoints": {"movies": "/movies", "reviews": "/reviews", "docs": "/docs"},
    }


# Movie CRUD endpoints
@app.get("/movies", status_code=status.HTTP_200_OK)
def get_movies(
    genre: Optional[GenreEnum] = Query(None, description="Filter by genre"),
    release_year: Optional[int] = Query(None, description="Filter by release year"),
    director: Optional[str] = Query(
        None, description="Filter by director (case-insensitive)"
    ),
    min_rating: Optional[float] = Query(
        None, ge=0.0, le=10.0, description=MIN_RATING_DESC
    ),
    max_rating: Optional[float] = Query(
        None, ge=0.0, le=10.0, description=MAX_RATING_DESC
    ),
    min_duration: Optional[int] = Query(
        None, ge=1, description="Minimum duration in minutes"
    ),
    max_duration: Optional[int] = Query(
        None, ge=1, description="Maximum duration in minutes"
    ),
    sort_by: Optional[str] = Query(
        "id", description="Sort by: id, title, release_year, rating, duration"
    ),
    order: Optional[str] = Query("asc", description=SORT_ORDER_DESC),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Limit number of results"
    ),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Retrieve all movies with optional filtering, sorting, and pagination.

    Returns:
        dict: Dictionary containing filtered and sorted movies
    """
    movies = load_data_from_json(MOVIES_FILE)

    # Update movie stats
    for movie in movies:
        avg_rating, review_count = calculate_movie_stats(movie["id"])
        movie["rating"] = avg_rating
        movie["review_count"] = review_count

    # Apply filters
    filtered_movies = movies.copy()

    if genre:
        filtered_movies = [m for m in filtered_movies if m["genre"] == genre.value]

    if release_year:
        filtered_movies = [
            m for m in filtered_movies if m["release_year"] == release_year
        ]

    if director:
        filtered_movies = [
            m for m in filtered_movies if director.lower() in m["director"].lower()
        ]

    if min_rating is not None:
        filtered_movies = [
            m
            for m in filtered_movies
            if m["rating"] is not None and m["rating"] >= min_rating
        ]

    if max_rating is not None:
        filtered_movies = [
            m
            for m in filtered_movies
            if m["rating"] is not None and m["rating"] <= max_rating
        ]

    if min_duration:
        filtered_movies = [
            m for m in filtered_movies if m["duration_minutes"] >= min_duration
        ]

    if max_duration:
        filtered_movies = [
            m for m in filtered_movies if m["duration_minutes"] <= max_duration
        ]

    # Sorting
    valid_sort_fields = ["id", "title", "release_year", "rating", "duration_minutes"]
    if sort_by in valid_sort_fields:
        reverse = order.lower() == "desc"
        if sort_by == "rating":
            # Handle None ratings for sorting
            filtered_movies.sort(
                key=lambda x: x[sort_by] if x[sort_by] is not None else 0,
                reverse=reverse,
            )
        else:
            filtered_movies.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_count = len(filtered_movies)
    if offset:
        filtered_movies = filtered_movies[offset:]
    if limit:
        filtered_movies = filtered_movies[:limit]

    return {
        "movies": filtered_movies,
        "total_count": total_count,
        "returned_count": len(filtered_movies),
        "offset": offset,
        "limit": limit,
    }


@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie(movie_id: int):
    """
    Retrieve a specific movie by its ID.

    Args:
        movie_id (int): The unique identifier of the movie

    Returns:
        dict: Movie data with updated statistics

    Raises:
        HTTPException: 404 if movie not found
    """
    movie = get_movie_by_id(movie_id)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MOVIE_NOT_FOUND_MESSAGE
        )

    # Update movie stats
    avg_rating, review_count = calculate_movie_stats(movie_id)
    movie["rating"] = avg_rating
    movie["review_count"] = review_count

    return {"message": "Movie found", "movie": movie}


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieCreate,
    auto_id: bool = Query(False, description="Automatically generate movie ID"),
):
    """
    Create a new movie.

    Args:
        movie (MovieCreate): Movie object containing movie details
        auto_id (bool): If True, automatically generates a unique ID

    Returns:
        dict: Confirmation message and created movie data
    """
    movies = load_data_from_json(MOVIES_FILE)

    # Generate ID (always auto-generate to avoid conflicts)
    max_id = max([m["id"] for m in movies], default=0)
    movie_id = max_id + 1

    # Create movie dict with computed fields
    movie_dict = movie.model_dump()
    movie_dict["id"] = movie_id
    movie_dict["rating"] = None
    movie_dict["review_count"] = 0

    movies.append(movie_dict)
    save_data_to_json(movies, MOVIES_FILE)

    return {"message": "Movie created", "movie": movie_dict}


@app.put("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, updated_movie: MovieCreate):
    """
    Update an existing movie by its ID.

    Args:
        movie_id (int): The unique identifier of the movie to update
        updated_movie (MovieCreate): Updated movie data

    Returns:
        dict: Confirmation message and updated movie data

    Raises:
        HTTPException: 404 if movie not found
    """
    movies = load_data_from_json(MOVIES_FILE)

    for movie in movies:
        if movie["id"] == movie_id:
            # Update movie fields but preserve ID and stats
            updated_dict = updated_movie.model_dump()
            movie.update(updated_dict)
            movie["id"] = movie_id  # Preserve original ID

            # Recalculate stats
            avg_rating, review_count = calculate_movie_stats(movie_id)
            movie["rating"] = avg_rating
            movie["review_count"] = review_count

            save_data_to_json(movies, MOVIES_FILE)
            return {"message": "Movie updated", "movie": movie}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=MOVIE_NOT_FOUND_MESSAGE
    )


@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int):
    """
    Delete a movie by its ID. Also deletes all associated reviews.

    Args:
        movie_id (int): The unique identifier of the movie to delete

    Returns:
        dict: Confirmation message and deleted movie data

    Raises:
        HTTPException: 404 if movie not found
    """
    movies = load_data_from_json(MOVIES_FILE)
    reviews = load_data_from_json(REVIEWS_FILE)

    for movie in movies:
        if movie["id"] == movie_id:
            # Remove the movie
            movies.remove(movie)
            save_data_to_json(movies, MOVIES_FILE)

            # Remove all reviews for this movie
            remaining_reviews = [r for r in reviews if r["movie_id"] != movie_id]
            deleted_reviews_count = len(reviews) - len(remaining_reviews)
            save_data_to_json(remaining_reviews, REVIEWS_FILE)

            return {
                "message": "Movie and associated reviews deleted",
                "movie": movie,
                "deleted_reviews_count": deleted_reviews_count,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=MOVIE_NOT_FOUND_MESSAGE
    )


# Review CRUD endpoints
@app.get("/reviews", status_code=status.HTTP_200_OK)
def get_reviews(
    movie_id: Optional[int] = Query(None, description="Filter by movie ID"),
    reviewer_name: Optional[str] = Query(
        None, description="Filter by reviewer name (case-insensitive)"
    ),
    min_rating: Optional[float] = Query(
        None, ge=1.0, le=10.0, description=MIN_RATING_DESC
    ),
    max_rating: Optional[float] = Query(
        None, ge=1.0, le=10.0, description=MAX_RATING_DESC
    ),
    sort_by: Optional[str] = Query(
        "created_at", description="Sort by: id, movie_id, rating, created_at"
    ),
    order: Optional[str] = Query("desc", description=SORT_ORDER_DESC),
    limit: Optional[int] = Query(
        None, ge=1, le=100, description="Limit number of results"
    ),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Retrieve all reviews with optional filtering, sorting, and pagination.

    Returns:
        dict: Dictionary containing filtered and sorted reviews
    """
    reviews = load_data_from_json(REVIEWS_FILE)

    # Apply filters
    filtered_reviews = reviews.copy()

    if movie_id:
        filtered_reviews = [r for r in filtered_reviews if r["movie_id"] == movie_id]

    if reviewer_name:
        filtered_reviews = [
            r
            for r in filtered_reviews
            if reviewer_name.lower() in r["reviewer_name"].lower()
        ]

    if min_rating is not None:
        filtered_reviews = [r for r in filtered_reviews if r["rating"] >= min_rating]

    if max_rating is not None:
        filtered_reviews = [r for r in filtered_reviews if r["rating"] <= max_rating]

    # Sorting
    valid_sort_fields = ["id", "movie_id", "rating", "created_at"]
    if sort_by in valid_sort_fields:
        reverse = order.lower() == "desc"
        if sort_by == "created_at":
            # Sort by datetime
            filtered_reviews.sort(
                key=lambda x: (
                    datetime.fromisoformat(x[sort_by].replace("Z", "+00:00"))
                    if isinstance(x[sort_by], str)
                    else x[sort_by]
                ),
                reverse=reverse,
            )
        else:
            filtered_reviews.sort(key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_count = len(filtered_reviews)
    if offset:
        filtered_reviews = filtered_reviews[offset:]
    if limit:
        filtered_reviews = filtered_reviews[:limit]

    return {
        "reviews": filtered_reviews,
        "total_count": total_count,
        "returned_count": len(filtered_reviews),
        "offset": offset,
        "limit": limit,
    }


@app.get("/reviews/{review_id}", status_code=status.HTTP_200_OK)
def get_review(review_id: int):
    """
    Retrieve a specific review by its ID.

    Args:
        review_id (int): The unique identifier of the review

    Returns:
        dict: Review data if found

    Raises:
        HTTPException: 404 if review not found
    """
    reviews = load_data_from_json(REVIEWS_FILE)

    for review in reviews:
        if review["id"] == review_id:
            return {"message": "Review found", "review": review}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=REVIEW_NOT_FOUND_MESSAGE
    )


@app.post("/reviews", status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    auto_id: bool = Query(False, description="Automatically generate review ID"),
):
    """
    Create a new review for an existing movie.

    Args:
        review (ReviewCreate): Review object containing review details
        auto_id (bool): If True, automatically generates a unique ID

    Returns:
        dict: Confirmation message and created review data

    Raises:
        HTTPException: 404 if movie not found
    """
    # Validate that the movie exists
    if not get_movie_by_id(review.movie_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {review.movie_id} not found",
        )

    reviews = load_data_from_json(REVIEWS_FILE)

    # Generate ID (always auto-generate to avoid conflicts)
    max_id = max([r["id"] for r in reviews], default=0)
    review_id = max_id + 1

    # Create review dict
    review_dict = review.model_dump()
    review_dict["id"] = review_id
    review_dict["created_at"] = datetime.now()

    reviews.append(review_dict)
    save_data_to_json(reviews, REVIEWS_FILE)

    # Update movie statistics
    update_movie_stats(review.movie_id)

    return {"message": "Review created", "review": review_dict}


@app.put("/reviews/{review_id}", status_code=status.HTTP_200_OK)
def update_review(review_id: int, updated_review: ReviewCreate):
    """
    Update an existing review by its ID.

    Args:
        review_id (int): The unique identifier of the review to update
        updated_review (ReviewCreate): Updated review data

    Returns:
        dict: Confirmation message and updated review data

    Raises:
        HTTPException: 404 if review not found or movie not found
    """
    # Validate that the movie exists
    if not get_movie_by_id(updated_review.movie_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {updated_review.movie_id} not found",
        )

    reviews = load_data_from_json(REVIEWS_FILE)

    for review in reviews:
        if review["id"] == review_id:
            old_movie_id = review["movie_id"]

            # Update review fields but preserve ID and created_at
            updated_dict = updated_review.model_dump()
            review.update(updated_dict)
            review["id"] = review_id  # Preserve original ID

            save_data_to_json(reviews, REVIEWS_FILE)

            # Update movie statistics for both old and new movies (if changed)
            update_movie_stats(old_movie_id)
            if old_movie_id != updated_review.movie_id:
                update_movie_stats(updated_review.movie_id)

            return {"message": "Review updated", "review": review}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=REVIEW_NOT_FOUND_MESSAGE
    )


@app.delete("/reviews/{review_id}", status_code=status.HTTP_200_OK)
def delete_review(review_id: int):
    """
    Delete a review by its ID.

    Args:
        review_id (int): The unique identifier of the review to delete

    Returns:
        dict: Confirmation message and deleted review data

    Raises:
        HTTPException: 404 if review not found
    """
    reviews = load_data_from_json(REVIEWS_FILE)

    for review in reviews:
        if review["id"] == review_id:
            movie_id = review["movie_id"]
            reviews.remove(review)
            save_data_to_json(reviews, REVIEWS_FILE)

            # Update movie statistics
            update_movie_stats(movie_id)

            return {"message": "Review deleted", "review": review}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=REVIEW_NOT_FOUND_MESSAGE
    )


# Additional useful endpoints
@app.get("/movies/{movie_id}/reviews", status_code=status.HTTP_200_OK)
def get_movie_reviews(
    movie_id: int,
    min_rating: Optional[float] = Query(
        None, ge=1.0, le=10.0, description=MIN_RATING_DESC
    ),
    max_rating: Optional[float] = Query(
        None, ge=1.0, le=10.0, description=MAX_RATING_DESC
    ),
    sort_by: Optional[str] = Query(
        "created_at", description="Sort by: rating, created_at"
    ),
    order: Optional[str] = Query("desc", description=SORT_ORDER_DESC),
):
    """
    Get all reviews for a specific movie.

    Args:
        movie_id (int): The unique identifier of the movie

    Returns:
        dict: Movie information and its reviews

    Raises:
        HTTPException: 404 if movie not found
    """
    if not get_movie_by_id(movie_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MOVIE_NOT_FOUND_MESSAGE
        )

    reviews = load_data_from_json(REVIEWS_FILE)
    movie_reviews = [r for r in reviews if r["movie_id"] == movie_id]

    # Apply filters
    if min_rating is not None:
        movie_reviews = [r for r in movie_reviews if r["rating"] >= min_rating]

    if max_rating is not None:
        movie_reviews = [r for r in movie_reviews if r["rating"] <= max_rating]

    # Sorting
    if sort_by in ["rating", "created_at"]:
        reverse = order.lower() == "desc"
        if sort_by == "created_at":
            movie_reviews.sort(
                key=lambda x: (
                    datetime.fromisoformat(x[sort_by].replace("Z", "+00:00"))
                    if isinstance(x[sort_by], str)
                    else x[sort_by]
                ),
                reverse=reverse,
            )
        else:
            movie_reviews.sort(key=lambda x: x[sort_by], reverse=reverse)

    return {
        "movie_id": movie_id,
        "reviews": movie_reviews,
        "total_reviews": len(movie_reviews),
    }


@app.get("/stats", status_code=status.HTTP_200_OK)
def get_stats():
    """
    Get general statistics about movies and reviews.

    Returns:
        dict: Statistics about the database
    """
    movies = load_data_from_json(MOVIES_FILE)
    reviews = load_data_from_json(REVIEWS_FILE)

    # Calculate stats
    total_movies = len(movies)
    total_reviews = len(reviews)

    if reviews:
        avg_rating_all = sum(r["rating"] for r in reviews) / len(reviews)
        avg_rating_all = round(avg_rating_all, 2)
    else:
        avg_rating_all = None

    # Genre distribution
    genre_counts = {}
    for movie in movies:
        genre = movie["genre"]
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Movies with most reviews
    movie_review_counts = {}
    for review in reviews:
        movie_id = review["movie_id"]
        movie_review_counts[movie_id] = movie_review_counts.get(movie_id, 0) + 1

    return {
        "total_movies": total_movies,
        "total_reviews": total_reviews,
        "average_rating_overall": avg_rating_all,
        "genre_distribution": genre_counts,
        "movies_by_review_count": dict(
            sorted(movie_review_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ),
    }
